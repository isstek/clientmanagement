from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from urllib.parse import quote, unquote
from django.conf import settings
#from django.core.files.storage import default_storage
from wsgiref.util import FileWrapper
from django.urls import reverse
import uuid, os, random, pytz


def upload_to_file_tool(instance, filename):
    return os.path.join(instance.get_file_folder(), filename)

TOOL_TYPE_FIELD = {'l': {'class': 'LinkTool', 'inst': 'linktool'}, 
                    'f': {'class': 'FileTool', 'inst': 'filetool'}}


class MainTool(models.Model):

    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    name = models.CharField('Tool name', max_length=80, null=False)
    public = models.BooleanField("Public tool", default=False, unique=False, blank=False)
    unid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField('Description', null=True, default='', blank=True)
    tool_type_field = models.CharField(max_length=1, null=False, default='')

    def createtime(self):
        return self.createdon.astimezone(pytz.timezone('America/New_York'))

    def tool_type(self):
        if self.tool_type_field in TOOL_TYPE_FIELD:
            return self.__getattribute__(TOOL_TYPE_FIELD[self.tool_type_field]['inst']).tool_type()
        return ''

    def get_link(self):
        if self.tool_type_field in TOOL_TYPE_FIELD:
            return self.__getattribute__(TOOL_TYPE_FIELD[self.tool_type_field]['inst']).get_link()
        return ''

    def get_link_text(self):
        if self.tool_type_field in TOOL_TYPE_FIELD:
            return self.__getattribute__(TOOL_TYPE_FIELD[self.tool_type_field]['inst']).get_link_text()
        return ''

    def get_file_folder(self):
        folder_path = os.path.join(settings.TOOLS_FILES, self.unid.hex)
        return folder_path

    def get_full_name(self):
        if self.tool_type_field in TOOL_TYPE_FIELD:
            return self.__getattribute__(TOOL_TYPE_FIELD[self.tool_type_field]['inst']).get_full_name()
        return "Tool " + self.name

    def get_name_for_user(self):
        if self.tool_type_field in TOOL_TYPE_FIELD:
            return self.__getattribute__(TOOL_TYPE_FIELD[self.tool_type_field]['inst']).get_name_for_user()
        return self.name

    def __str__(self): 
        return self.get_full_name()


class LinkTool(MainTool):
    url = models.URLField("Link", max_length=255)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('tool_type_field').default = 'l'
        super(LinkTool, self).__init__(*args, **kwargs)

    def get_link(self):
        return self.url

    def get_link_text(self):
        return self.url

    def get_full_name(self):
        return "Link tool " + self.name
    
    def get_name_for_user(self):
        return self.name

    def tool_type(self):
        return 'l'


class FileTool(MainTool):
    filename = models.CharField("Filename", max_length=100, null=True)
    uplfile = models.FileField("File", upload_to=upload_to_file_tool, max_length=255, null=True)
    version = models.CharField("Version", max_length=50, null=False, blank=True, default="")

    def __init__(self, *args, **kwargs):
        self._meta.get_field('tool_type_field').default = 'f'
        super(FileTool, self).__init__(*args, **kwargs)

    def get_full_name(self):
        return "File tool " + self.name + " (v. " + self.version + ")"
    
    def get_name_for_user(self):
        return self.name + " (v. " + self.version + ")"

    def get_link_text(self):
        return "Download"

    def get_link(self):
        return reverse("download_tool", kwargs={'tooluuid': self.unid})

    def tool_type(self):
        return 'f'


def downloadFileFromTools(tooluuid):
    try:
        tool = FileTool.objects.get(unid=tooluuid)
    except Exception as exc:
        print(exc)
        return None
    response = HttpResponse(FileWrapper(tool.uplfile))
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(tool.uplfile.name))
    response['X-Sendfile'] = smart_str(tool.uplfile.name)
    return response

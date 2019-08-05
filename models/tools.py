from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.utils.encoding import smart_str
from urllib.parse import quote, unquote
from django.conf import settings
from django.dispatch import receiver
from wsgiref.util import FileWrapper
from django.urls import reverse
import uuid, os, random, pytz, mimetypes
from clientmanagement import utilities, error_views


def upload_to_file_tool(instance, filename):
    return os.path.join(instance.get_file_folder(), filename)

TOOL_TYPE_FIELD = {'l': {'class': 'LinkTool', 'inst': 'linktool'}, 
                    'f': {'class': 'FileTool', 'inst': 'filetool'}}


class MainTool(models.Model):

    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    name = models.CharField('Tool name', max_length=80, null=False)
    public = models.BooleanField("Public tool", default=False, unique=False, blank=False)
    publicinlist = models.BooleanField("Public tool in list", default=True, unique=False, blank=False)
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
        return (self.url[:settings.LINK_TOOL_STRING_LENGTH] + '...') if len(self.url) > settings.LINK_TOOL_STRING_LENGTH else self.url

    def get_full_name(self):
        return "Link tool " + self.name
    
    def get_name_for_user(self):
        return self.name

    def tool_type(self):
        return 'l'


class FileTool(MainTool):
    uplfile = models.FileField("File", upload_to=upload_to_file_tool, max_length=255, null=True)
    version = models.CharField("Version", max_length=50, null=False, blank=True, default="")

    def __init__(self, *args, **kwargs):
        self._meta.get_field('tool_type_field').default = 'f'
        super(FileTool, self).__init__(*args, **kwargs)

    def get_full_name(self):
        if (os.path.exists(self.uplfile.path)):
            return "File tool " + self.name + " (v. " + self.version + ")"
        else:
            return "File was deleted"
    
    def get_name_for_user(self):
        if (os.path.exists(self.uplfile.path)):
            return self.name + " (v. " + self.version + ")"
        else:
            return "File was deleted"

    def get_link_text(self):
        if (os.path.exists(self.uplfile.path)):
            return "Download (" + utilities.humanize_bytes(os.path.getsize(self.uplfile.path)) + ")"
        else:
            return "File was deleted"

    def get_link(self):
        if (os.path.exists(self.uplfile.path)):
            if self.public:
                return reverse("download_tool_public", kwargs={'tooluuid': self.unid})
            else:
                return reverse("download_tool", kwargs={'tooluuid': self.unid})
        else:
            return ''

    def tool_type(self):
        return 'f'

@receiver(models.signals.post_delete, sender=FileTool)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.uplfile:
        if os.path.isfile(instance.uplfile.path):
            os.remove(instance.uplfile.path)
            os.rmdir( os.path.dirname(instance.uplfile.path))


def downloadFileFromTools(request, tooluuid):
    try:
        tool = FileTool.objects.get(unid=tooluuid)
    except Exception as exc:
        print(exc)
        return error_views.notfound(request)
    if tool.public or request.user.is_authenticated:
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(tool.uplfile, chunk_size),
                                content_type=mimetypes.guess_type(tool.uplfile.path)[0])
        response['Content-Length'] = os.path.getsize(tool.uplfile.path)    
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(tool.uplfile.path))
        return response
    else:
        return redirect(reverse("download_tool", kwargs={'tooluuid': tool.unid}))

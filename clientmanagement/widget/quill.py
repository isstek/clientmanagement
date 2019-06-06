from django import forms
from django.db import models
from django import template
import json
from clientmanagement.quill_delta_to_html import quill_to_html


class QuillWidget(forms.Textarea):
    template_name = 'forms/widget/quill.html'

    def __init__(self, attrs=None):
        return super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if 'placeholder' in attrs:
            context['widget']['placeholder'] = attrs['placeholder']
        if 'theme' in attrs:
            context['widget']['theme'] = attrs['theme']
        else:
            context['widget']['theme'] = 'snow'
        if 'value' in context['widget']:
            context['widget']['quill_object']=QuillObject(context['widget']['value'])
        return context


class QuillField(forms.CharField):
    widget = QuillWidget

    def __init__(self, max_length=None, min_length=None, strip=True, empty_value='', **kwargs):
        return super().__init__(max_length=max_length, min_length=min_length, strip=strip, empty_value=empty_value, **kwargs)


def check_quill_string(str):
    try:
        res = json.loads(str)
        if 'ops' in res:
            return True
        else:
            return False
    except Exception:
        return False

        
def get_quill_text(str):
    try:
        a=json.loads(str)
        result = quill_to_html.quill_delta_to_html(a)
        if result is None:
            return str
        return result
    except Exception:
        return json.dumps(str)


class QuillObject():
    def __init__(self, text=""):
        self.text=text

    def is_quill_content(self):
        return check_quill_string(self.text)

    def get_quill_content(self):
        return get_quill_text(self.text)

    def get_content(self):
        return self.text

    def get_content_js(self):
        return self.text.replace("\n", "\\n")

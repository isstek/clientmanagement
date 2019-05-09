from django import forms
from django.db import models
from django import template
import json

register = template.Library()

@register.filter
def get_quill_text(str):
    try:
        a=json.loads(str)
        return str
    except Exception:
        return json.dumps(str)


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
            context['widget']['theme'] = 'bubble'
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
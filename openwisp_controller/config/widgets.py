from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class JsonSchemaWidget(AdminTextareaWidget):
    """
    JSON Schema Editor widget
    """

    @property
    def media(self):
        js = [
            static(f'config/js/{path}')
            for path in (
                'utils.js',
                'lib/advanced-mode.js',
                'lib/tomorrow_night_bright.js',
                'lib/jsonschema-ui.js',
                'widget.js',
            )
        ]
        css = {
            'all': [
                static(f'config/css/{path}')
                for path in ('lib/jsonschema-ui.css', 'lib/advanced-mode.css')
            ]
        }
        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['class'] = 'vLargeTextField jsoneditor-raw'
        html = """
<input class="button json-editor-btn-edit advanced-mode" type="button" value="{0}">
<script>django._netjsonconfigSchemaUrl = "{1}";</script>
<label id="netjsonconfig-hint">
    Want to learn to use the advanced mode? Consult the
    <a href="http://netjsonconfig.openwisp.org/en/stable/general/basics.html"
       target="_blank">netjsonconfig documentation</a>.
</label>
"""
        html = html.format(_('Advanced mode (raw JSON)'), reverse('admin:schema'))
        html += super().render(name, value, attrs, renderer)
        return html

from django.conf import settings
from django.template import Context
import django
from django.template.loader import get_template
from django.utils.safestring import mark_safe

class JsonKeyValueWidget(AdminTextareaWidget):
    """
    JSON Key/Value widget
    """

    @property
    def media(self):
        internal_js = [
            'lib/underscore.js',
            'jsonwidget.js'
        ]
        js = [static(f'config/js/{path}') for path in internal_js]
        css = {
            'all': (static('config/css/keyvalue.css'),)
        }
        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        # it's called "original" because it will be replaced by a copy
        attrs['class'] = 'flat-json-original-textarea'
        html = super().render(name, value, attrs)
        template = get_template('json_keyvalue_widget.html')
        html += template.render({'field_name': name})
        return mark_safe(html)

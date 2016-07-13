from django import template
from PIL import Image
from django.conf import settings
import os
import datetime
from dashboard_admin.models import SiteText

register = template.Library()

@register.filter(name='footer_text')
def footer_text(request):
	footer = SiteText.objects.get(name='footer')
	return footer.text

@register.filter(name='lower_replace')
def lower_replace(value):
	return str(value.lower().replace(' ',''))

# register.simple_tag(lower_replace)
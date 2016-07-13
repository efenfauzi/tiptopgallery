from django import template
from PIL import Image
from django.conf import settings
import os
import datetime
import humanize
path = settings.TEMP_DIR_IMAGE 
from dashboard_admin.models import SiteText

register = template.Library()

@register.filter(name='image_size')
def image_size(filename):
	try:
		im = Image.open(path+'/'+filename)
		return im.size
	except:
		return "image couldn't decoded"

@register.filter(name='modification_date')
def modification_date(filename):
	try:
		t = os.path.getmtime(path+'/'+filename)
		return datetime.datetime.fromtimestamp(t)
	except:
		return "no file"

@register.filter(name='get_size')
def get_size(filename):
	try:
		t = os.path.getsize(path+'/'+filename)
		return humanize.naturalsize(t)
	except:
		return "no file"

@register.filter(name='get_name')
def get_name(filename):
	print filename
	# try:
	# 	t = os.remove(path+'/'+filename)
	# 	# return '<button onclick="%s">Click me</button>' %(t)
	# 	print t
	# except:
	# 	return "no file"


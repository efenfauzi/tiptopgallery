from django import template
from PIL import Image
from django.conf import settings
import os
import datetime
import humanize

register = template.Library()

@register.filter(name='image_size')
def image_size(a):
	path = settings.TEMP_DIR_IMAGE 
	try:
		im = Image.open(path+'/'+a)
		return im.size
	except:
		return "image couldn't decoded"

@register.filter(name='modification_date')
def modification_date(filename):
	path = settings.TEMP_DIR_IMAGE 

	t = os.path.getmtime(path+'/'+filename)
	return datetime.datetime.fromtimestamp(t)

@register.filter(name='get_size')
def get_size(filename):
	path = settings.TEMP_DIR_IMAGE 

	t = os.path.getsize(path+'/'+filename)

	return humanize.naturalsize(t)

from django import forms
from .models import *

class PostForm(forms.ModelForm):
	title = forms.CharField(max_length=255)

	class Meta:
		model = Post
		fields = ('title', )


class ImageForm(forms.ModelForm):
	images = forms.ImageField(label='Image')    
	
	class Meta:
		model = PostImage
		fields = ('images', )


class ScrapImageForm(forms.ModelForm):
	url = forms.URLField(label='URL')    
	
	class Meta:
		model = ScrapImage
		fields = ('url', )
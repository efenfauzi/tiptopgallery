from __future__ import unicode_literals

from django.db import models
import random
import uuid
from PIL import Image as Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class Post(models.Model):
	id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	title = models.CharField(max_length=255)
	# category = models.IntegerField()
	# tags = models.IntegerField()
	created = models.DateTimeField(auto_now=True)
	modified = models.DateTimeField(auto_now_add=True)
	url_id = models.UUIDField(default=uuid.uuid4, editable=False)

	
	def __str__(self):
		return str(self.title)

	def save(self, *args, **kwargs):
		if self.url_id:
			self.url_id = uuid.uuid4()
		super(Post, self).save(*args, **kwargs)

		
	
	def get_first_image(self):
		img = self.images.count()
		# print img
		try:
			if img != 0: 
				random_thumb = random.randrange(int(img))
				image_random = self.images.all()[random_thumb]
				return image_random.images.url
		except:
			return 0

	def get_thumb_image(self):
		img = self.images.count()

		thumb = PostImage.objects.filter(post=self.id)

		print thumb.values('thumbs')
		try:
			if img != 0: 
				random_thumb = random.randrange(int(img))
				image_random = thumb.values_list('thumbs', flat=True)[random_thumb]
				return image_random
		except:
			return 0
		# print thumb

		
	def get_image(self):
		return self.images.all()
	
	class Meta:
		db_table = 'posts'
		verbose_name = u'Posting Gambar'
		verbose_name_plural = u'Posting Gambar'


class PostImage(models.Model):

	upload_to = 'image/%s/%s'

	def _get_upload_to(self, filename):
		title = str(self.post.title).replace(" ","")
		ext = filename.split('.')[-1]
		name = "{0}.{1}".format(str(self.post.title), ext)
		return self.upload_to % (title, name)

	post = models.ForeignKey(Post, related_name='images')
	images = models.ImageField(upload_to='image/', max_length=255)
	thumbs = models.ImageField(upload_to='image/thumbs', max_length=255, null=True, blank=True)
	
	def __str__(self):
		return str(self.post)


	def save(self, *args, **kwargs):
		print self.images
		ext = str(self.images).split('.')[-1]
		image = Image.open(StringIO.StringIO(self.images.read()))

		if self.thumbs:
			image = Image.open(StringIO.StringIO(self.images.read()))
			if image.mode != "RGB":
				image = image.convert("RGB")
		image.thumbnail((225,225), Image.ANTIALIAS)
		output = StringIO.StringIO()
		image.save(output, format='jpeg', quality=99)
		output.seek(0)
		self.thumbs= InMemoryUploadedFile(output,'ImageField', "{0}_thumb.{1}".format(self.images.name.split('.')[0], ext), 'image/jpeg', output.len, None)

		super(PostImage, self).save(*args, **kwargs)
		
	class Meta:
		db_table = 'post_images'
		verbose_name = u'Gambar'
		verbose_name_plural = u'Gambar'

class ScrapImage(models.Model):
	url = models.URLField()
	downloaded_image = models.CharField(max_length=255, null=True, blank=True)
	failed_image = models.CharField(max_length=255, null=True, blank=True)
	created = models.DateTimeField(auto_now=True)
	modified = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = ' scrap_image'
		verbose_name = u'Scrap Image'
		verbose_name_plural = u'Scrap Image'
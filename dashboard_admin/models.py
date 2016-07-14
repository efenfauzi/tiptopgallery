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
		# img = self.images.count()

		# thumb = PostImage.objects.filter(post=self.id)

		# # print thumb.values('thumbs')
		# try:
		# 	if img != 0: 
		# 		random_thumb = random.randrange(int(img))
		# 		image_random = thumb.values_list('thumbs', flat=True)[random_thumb]
		# 		return image_random
		# except:
		# 	return 0
		img = self.images.count()
		# print img
		try:
			if img != 0: 
				random_thumb = random.randrange(int(img))
				image_random = self.images.all()[random_thumb]
				return image_random.thumbs.url
		except:
			return 0

	# def get_height_size(self):
		#= get width <= width
		# thumb = PostImage.objects.filter(post=self.id)

		# for x in thumb:

		# 	image = Image.open(StringIO.StringIO(x.thumbs.read()))
		# 	width, height = image.size
			# print width
			# print height
			# if width < height :
				# print dir(image)
				# print image
		# return
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
		image.thumbnail((180,180), Image.ANTIALIAS)
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

def upload_icon(instance, filename):
	ext = filename.split('.')[-1]
	name = "{0}.{1}".format(str(instance.name).lower(), ext)
	return ('image/icon/'+name)

class Category(models.Model):
	parent = models.ForeignKey('self', null=True,blank=True, related_name='subcategories')
	name = models.CharField(max_length=100)
	list_status = ((0, "not active"), (1, "active"))
	status = models.IntegerField(default=1, choices=list_status)
	icon = models.ImageField(upload_to=upload_icon, max_length=255, null=True, blank=True)
	
	def __str__(self):
		return self.name

	class Meta:
		db_table = 'categories'
		verbose_name = 'Category'
		verbose_name_plural = 'Category'

	def icon_image(self):
		if self.icon:
			return self.icon
		else:
			return "none"

	def save(self, *args, **kwargs):

		if self.icon:
			ext = str(self.icon).split('.')[-1]
			image = Image.open(StringIO.StringIO(self.icon.read()))
			if image.mode != "RGB":
				image = image.convert("RGB")
			image.thumbnail((64,64), Image.ANTIALIAS)
			output = StringIO.StringIO()
			image.save(output, format='jpeg', quality=99)
			output.seek(0)
			self.icon= InMemoryUploadedFile(output,'ImageField', "{0}.{1}".format(self.icon.name, ext), 'image/jpeg', output.len, None)

		super(Category, self).save(*args, **kwargs)

class CategoryPost(models.Model):
	post = models.ForeignKey(Post, related_name='categorypost')
	category = models.ForeignKey(Category, null=True, blank=True)

	def __str__(self):
		return str(self.post.title)

	class Meta:
		db_table = 'category_posts'
		verbose_name = 'Category Post'
		verbose_name_plural = 'Category Post'


class VisitPagePost(models.Model):
	post = models.ForeignKey(Post, related_name='visitedpost')
	count = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return str(self.count)

	class Meta:
		db_table = 'visit_posts'
		verbose_name = 'Visit Post'
		verbose_name_plural = 'Visit Post'

	def date_counter(self):
		return self.date.strftime('%Y-%m-%d')


class SiteText(models.Model):
	name = models.CharField(max_length=255) 
	text = models.TextField()


	def __str__(self):
		return str(self.name)


	class Meta:
		db_table = 'site_text'
		verbose_name = 'a description site'
		verbose_name_plural = 'a description sites'


class AdsPost(models.Model):
	post = models.ForeignKey(Post)
	ads = models.TextField()


	def __str__(self):
		return str(self.ads)

	class Meta:
		db_table = 'posts_ads'
		verbose_name = 'ads to post'
		verbose_name_plural = 'ads to posts'

class ModelNamePost(models.Model):
	post = models.ForeignKey(Post)
	name = models.CharField(max_length=100)

	def __str__(self):
		return str(self.name)

	class Meta:
	 	db_table = 'models_posts'
		verbose_name = 'model name related post'
		verbose_name_plural = 'model name related posts'
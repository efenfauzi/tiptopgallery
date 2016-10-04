from django.contrib import admin
from .models import *
import uuid

# Register your models here.


class PostImageInline(admin.TabularInline):
	model = PostImage
	extra = 5
	# max_num = 10


class PostAdmin(admin.ModelAdmin):
	# pass
	inlines = [PostImageInline, ]
	list_display = 'title', 'get_thumb_image', 'url_id', #'get_height_size'


class PostImageAdmin(admin.ModelAdmin):
	pass

	
class CategoryAdmin(admin.ModelAdmin):
	list_display = 'name', 'status', 

class CategoryPostAdmin(admin.ModelAdmin):
	list_display = 'post', 'category', 


class VisitPagePostAdmin(admin.ModelAdmin):
	list_display = 'post', 'count', 'date_counter' 
	ordering = ['-date',]


class SiteTextAdmin(admin.ModelAdmin):
	list_display = 'name', 'text'

class ModelNameAdmin(admin.ModelAdmin):
	list_display = 'name', 'description',

class ModelNamePostAdmin(admin.ModelAdmin):
	list_display = 'post', 'name',


admin.site.register(Post, PostAdmin)
# admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryPost, CategoryPostAdmin)
admin.site.register(VisitPagePost, VisitPagePostAdmin)
admin.site.register(SiteText, SiteTextAdmin)
admin.site.register(ModelNamePost, ModelNamePostAdmin)
admin.site.register(ModelName, ModelNameAdmin)

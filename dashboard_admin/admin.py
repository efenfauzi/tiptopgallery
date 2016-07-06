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


	
	# actions = ['change_uuid', ]


	# def change_uuid(self, request, queryset):
	# 	url_id = queryset.update(url_id=uuid.uuid4())
	# 	message_bit = "%s " % url_id
	# 	self.message_user(request, "%s URL id berhasil diubah." % message_bit)
	# change_uuid.short_description = u'Ubah Url ID'

class PostImageAdmin(admin.ModelAdmin):
	pass

	
class CategoryAdmin(admin.ModelAdmin):
	list_display = 'name', 'status', 

class CategoryPostAdmin(admin.ModelAdmin):
	list_display = 'post', 'category', 


class VisitPagePostAdmin(admin.ModelAdmin):
	list_display = 'post', 'count', 


admin.site.register(Post, PostAdmin)
# admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryPost, CategoryPostAdmin)
admin.site.register(VisitPagePost, VisitPagePostAdmin)

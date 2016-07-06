"""bokepdo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dashboard_admin import views as dab
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', dab.index, name='index'),
    url(r'^$', dab.index_new, name='index_new'),
    url(r'^upload/$', dab.post, name='post'),

    url(r'^gallery/image=(?P<post_id>[^/]+).html$', dab.detail_new, name='detail_new'),
    url(r'^gallery/image=(?P<post_id>[^/]+).html/rename$', dab.rename_data, name='rename_data'),
    url(r'^gallery/image=(?P<post_id>[^/]+).html/zip$', dab.zip_post, name='zip_post'),

    # url(r'^detail/(?P<post_id>[0-9]+)/$', dab.detail, name='detail'),
    url(r'^scrap/$', dab.image_scrapper, name='image_scrapper'),
    url(r'^output/$', dab.list_image, name='list_image'),
    url(r'^export/$', dab.export_image, name='export_image'),
    url(r'^zip/$', dab.zip_file, name='zip_file'),
    url(r'^generate_uuid/$', dab.generate_uuid, name='generate_uuid'),
    url(r'^post/$', dab.export_to_post, name='export_to_post'),
    url(r'^delete/(?P<x>[^/]+)$', dab.delete_one, name='delete_one'),
    url(r'^category/search=(?P<name>[^/]+).html$', dab.category_post, name='category_post'),
    url(r'^populer.html$', dab.populer_post, name='populer_post'),

    # url(r'^delete_one/$', dab.delete_one, name='delete_one'),


]

if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
	}))

    urlpatterns.append(url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.STATIC_ROOT,
	}))
	

	
	
	

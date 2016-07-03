from .models import *
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.forms import modelformset_factory
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image
import image_scraper as scrap
import subprocess
from django.conf import settings
import os
import datetime
import string
import uuid
# Create your views here.
def index(request):
	data = Post.objects.all()
	return render(request, 'index.html', {'data':data})
	

def detail(request, post_id):
	data = get_object_or_404(Post, pk=post_id)
	return render(request, 'detail.html', {'data': data})

def randomword(length):
	kombinasi = "%s%s0123456789" % (string.lowercase, string.uppercase)
	return ''.join(random.choice(kombinasi) for i in range(length))


def index_new(request):
	all = Post.objects.all()
	# generate_uuid = all.values('url_id')

	# date = datetime.datetime.now().strftime('%H:%M:%S')
	# try:
	# 	date == '00:00:00'
	# 	for data in all:
	# 		data.url_id = uuid.uuid4()
	# 		data.save()
	# except:
	# 	pass


	paginator = Paginator(all, 16) # Show 25 contacts per page
	
	page = request.GET.get('page')
    
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		data = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		data = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {'data':data})
	
def detail_new(request, post_id):
    data = get_object_or_404(Post, url_id=post_id)
    return render(request, 'detail.html', {'data': data})
	

def post(request):

	ImageFormSet = modelformset_factory(PostImage, form=ImageForm, extra=3)

	if request.method == 'POST':

		postForm = PostForm(request.POST)
		formset = ImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())

		if postForm.is_valid() and formset.is_valid():

			post_form = postForm.save(commit=False)
			post_form.save()

			for form in formset.cleaned_data:
				image = form['images']
				photo = PostImage(post=post_form, image=image)
				photo.save()
				messages.success(request,"Yeeew,check it out on the home page!")
			return HttpResponseRedirect("/")
		else:
			print postForm.errors, formset.errors
	else:
		postForm = PostForm()
		formset = ImageFormSet(queryset=PostImage.objects.none())
	return render(request, 'upload.html', {'postForm': postForm, 'formset': formset},context_instance=RequestContext(request))


def image_scrapper(request):
	# print scrap
	if request.method == 'POST':	
		if request.POST.get('url'):
			url = request.POST.get('url')
			path = "media/image_download"
			subprocess.call("image-scraper {0} -s {1}".format(url, path), shell=True)
			return HttpResponseRedirect('/output')    #<b>scrapping image berhasil</b><br><a href='/output'>disini</a>)

	else:
		return render(request, 'image-scraper.html') #{'form':form, }

	return render(request, 'image-scraper.html') #{'form':form, }


def list_image(request):
	path = settings.TEMP_DIR_IMAGE 
	datafile = os.listdir(path)
	url_media = settings.URL_MEDIA

	# if request.POST.getlist('data'):
	# 	request.session['datalist'] = request.POST.getlist('data')
	# 	print "datalist %s" % request.session['datalist']
	# else :
	# 	if 'datalist' in request.session:
	# 		request.session['datalist'] = request.POST.getlist('data')

	if request.method == 'POST':
		# if request.POST.get('data'):
		# 	data = request.POST.get('data')
		# 	subprocess.call("rm -rf {0}/{1}".format(path, data), shell=True)
		data = request.POST.getlist('data')
		for x in data:
			# im = Image.open(path+'/'+x)
			# print "data gambar %s size %s " %(x,  im.size)
			# subprocess.call("rm -rf {0}/{1}".format(path, x), shell=True)
			os.remove(path+'/'+x)
		return HttpResponseRedirect('/output')
	return render(request, 'list_image.html', {'datafile': datafile, 'url_media': url_media}) #{'form':form, }


def export_image(request):
	path = settings.TEMP_DIR_IMAGE
	dir_path = settings.BASE_DIR+'/media/' 
	print dir_path
	url_media = settings.URL_MEDIA
	datafile = os.listdir(path)

	if request.POST.getlist('data'):
		request.session['datalist'] = request.POST.getlist('data')
		print "datalist %s" % request.session['datalist']
	else :
		if 'datalist' in request.session:
			request.session['datalist'] = request.POST.getlist('data')

	print "data di export %s" %request.session['datalist']
	for x in request.session['datalist']:
		print x
		# subprocess.call("mv {0}/{1} {2}".format(path, x, dir_path), shell=True)
		# subprocess.call("cp {0}/{1} {2}".format(path, x, dir_path), shell=True)
	return HttpResponse('<b>Copy image berhasil</b><br><a href="/output">disini</a>')
	# return render(request, 'list_image.html', {'datafile': datafile, 'url_media': url_media}) #{'form':form, }


def zip_file(request):
	path = settings.TEMP_DIR_IMAGE 
	datafile = os.listdir(path)
	url_media = settings.URL_MEDIA
	zip_media = settings.ZIP_MEDIA
	date = datetime.datetime.now().strftime('%d_%m_%Y')
	print path
	print date

	subprocess.call("rm -r {0}/*.zip".format(zip_media), shell=True)

	if request.method == 'POST':
		data = request.POST.getlist('data')
		print data
		for x in data:
			print x
			# print "proses zip"
	        # subprocess.call("mkdir -p db", shell=True)
			subprocess.call("zip -rj5 {0}/image_data.zip {1}/{2}".format(zip_media, path, x), shell=True)
		
		zip_file = open(zip_media+"/image_data.zip", 'r')
		response = HttpResponse(zip_file, content_type='application/force-download')
		response['Content-Disposition'] = 'attachment; filename="image_%s_%s.zip"' % (randomword(6), date)
		return response
		# return HttpResponseRedirect('/zip')
	return render(request, 'export_zip_image.html', {'datafile': datafile, 'url_media': url_media, 'path':path}) #{'form':form, }

def delete_one(request, x):
	path = settings.TEMP_DIR_IMAGE 
	datafile = os.listdir(path)
	url_media = settings.URL_MEDIA


	# print "data data"
	# if request.method == 'POST':
		# data = request.POST.get('data')
		# print data
	os.remove(path+'/'+x)
	return HttpResponseRedirect('/output')
	# return render(request, 'list_image.html', {'datafile': datafile, 'url_media': url_media}) #{'form':form, }

def generate_uuid(request):
	all = Post.objects.all()
	try:
		for data in all:
			data.url_id = uuid.uuid4()
			data.save()
	except:
		pass

	return HttpResponseRedirect('/')


def rename_data(request, post_id):
	data = Post.objects.get(url_id=post_id)
	image = PostImage.objects.filter(post=data.id)
	title =  str(data.title).replace(" ", "")
	unique = randomword(4)
	img_dir = settings.IMAGE_DIR
	print img_dir
	count = 0

	for x in image:
		data = str(x.images)
		path = data.split('/')[0]
		file = data.split('/')[1]
		filename = file.split('.')[0]
		ext = data.split('.')[1]
		if count <= int(image.count()):
			try:
				x.images = "{0}/{1}_{2}_img_{3}.{4}".format(path, unique, title, count, ext)
				x.save()
				src = ("{0}/{1}.{2}".format(img_dir,filename, ext))
				dest = ("{0}/{1}_{2}_img_{3}.{4}".format(img_dir, unique, title, count, ext))
				os.rename(src, dest) 
				count = count + 1
			except:
				pass

	return HttpResponseRedirect("/")
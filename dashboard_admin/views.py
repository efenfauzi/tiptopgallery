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
from shutil import copyfile, move, make_archive
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
import json 
# Create your views here.


# def login_user(request):
# 	return render(request,'login.html')

def login_user(request):
	logout(request)
	redirect_to = request.GET.get('next', '')
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		print username
		print password

	user = authenticate(username=username, password=password)
	if user is not None:
		if request.user.is_authenticated:
			login(request, user)
		return HttpResponseRedirect(redirect_to)  
	return render_to_response('login.html', context_instance=RequestContext(request))

def index(request):
	data = Post.objects.all()
	return render(request, 'index.html', {'data':data})
	

def detail(request, post_id):
	data = get_object_or_404(Post, pk=post_id)
	category = CategoryPost.objects.filter(post=data)
	return render(request, 'detail.html', {'data': data, 'category':category})


def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))


def index_new(request):
	all = Post.objects.all().order_by('-created')
	model_name = ModelName.objects.all()
	# generate_uuid = all.values('url_id')

	# date = datetime.datetime.now().strftime('%H:%M:%S')
	# try:
	# 	date == '00:00:00'
	# 	for data in all:
	# 		data.url_id = uuid.uuid4()
	# 		data.save()
	# except:
	# 	pass
	paginator = Paginator(all, 16) 
	
	page = request.GET.get('page')
    
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {'data':data, 'model_name':model_name})
	

def detail_new(request, post_id):
	data = get_object_or_404(Post, url_id=post_id)
	category = CategoryPost.objects.filter(post=data).filter(category__status=1)

	if request.method == 'GET':
		counter = VisitPagePost.objects.filter(post=data).last()
		date = datetime.datetime.now().strftime('%Y-%m-%d')

		print date

	
		try:
			date_count =  counter.date.strftime('%Y-%m-%d')
			print date_count
		except:
			date_count = datetime.datetime.now()
			print "tanggal sekarang %s" %datetime.datetime.now()

		if counter is None or date != date_count:
			# print "save baru"
			VisitPagePost(post=data, count=1, date=datetime.datetime.now()).save()
		else:
			# print int(counter.count)+1
			# if date == counter.date.strftime('%Y-%m-%d'):
			VisitPagePost.objects.filter(post=data).update(count=int(counter.count)+1, date=datetime.datetime.now())
			# else:
			# 	VisitPagePost(post=data, count=1, date=datetime.datetime.now()).save()

	# print category

	populer = VisitPagePost.objects.all().order_by('-count')[:5]

	recent = Post.objects.order_by('-created')[:5]

	# print recent

	return render(request, 'detail.html', {'data': data, 'category':category, 'populer':populer, 'recent':recent})

@login_required(login_url='/login/')
def image_scrapper(request):
	# print scrap
	if request.method == 'POST':	
		if request.POST.get('url'):
			url = request.POST.get('url')
			path = "{0}/image_download".format(settings.MEDIA_ROOT)
			subprocess.call("image-scraper {0} -s {1}".format(url, path), shell=True)
			return HttpResponseRedirect('/output')    #<b>scrapping image berhasil</b><br><a href='/output'>disini</a>)

	else:
		return render(request, 'image-scraper.html') #{'form':form, }

	return render(request, 'image-scraper.html') #{'form':form, }

@login_required(login_url='/login/')
def list_image(request):
	path = settings.TEMP_DIR_IMAGE 
	datafile = os.listdir(path)
	url_media = settings.URL_MEDIA

	print url_media

	if request.method == 'POST':
		data = request.POST.getlist('data')
		for x in data:
			os.remove(path+'/'+x)
		return HttpResponseRedirect('/output')
	return render(request, 'list_image.html', {'datafile': datafile, 'url_media': url_media}) #{'form':form, }

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def delete_one(request, x):
	path = settings.TEMP_DIR_IMAGE 
	url_media = settings.URL_MEDIA
	print path
	print x
	os.remove(path+'/'+x)
	return HttpResponseRedirect('/output')
	# return HttpResponseRedirect(reverse('delete_one'))

@login_required(login_url='/login/')
def generate_uuid(request):
	all = Post.objects.all()
	try:
		for data in all:
			data.url_id = uuid.uuid4()
			data.save()
	except:
		pass

	return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def rename_data(request, post_id):
	data = Post.objects.get(url_id=post_id)
	image = PostImage.objects.filter(post=data.id)
	title =  str(data.title).replace(" ", "")
	unique = randomword(4)
	img_dir = settings.IMAGE_DIR
	thumb_dir = settings.MEDIA_ROOT+'image/thumb'
	print img_dir
	count = 0

	print image
	for x in image:
		# print x.images
		ext = str(x.images).split('.')[-1]
		if count <= image.count():
			try:
				src = ("{0}/{1}".format(settings.MEDIA_ROOT, x.images))
				dest = ("{0}/{1}_{2}_img_{3}.{4}".format(img_dir, unique, title, count, ext))
				print "data belum diubah %s" %src 
				print "data setelah diubah %s" %dest
				os.move(src, dest)

				src_thumb = ("{0}/{1}".format(settings.MEDIA_ROOT, x.thumbs))
				dest_thumb = ("{0}/{1}_{2}_img_{3}-150x150thumb.{4}".format(thumb_dir, unique, title, count, ext))
				print "data belum diubah %s" %src_thumb 
				print "data setelah diubah %s" %dest_thumb
				os.move(src_thumb, dest_thumb)

				image_name = ("image/{0}_{1}_img_{2}.{3}".format(unique, title, count, ext))
				thumb_name = ("image/thumb/{1}_{2}_img_{3}-150x150thumb.{4}".format(unique, title, count, ext))

				print "image %s" %image_name
				print "thumb %s" %thumb_name

				data = PostImage(post=data, images=image_name, thumbs=thumb_name)
				data.save()
				# x.images = ("image/{0}_{1}_img_{2}.{3}".format(unique, title, count, ext))
				# x.save()
				count = count + 1

			except:
				print "error file doesnt exist"
	return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def export_to_post(request):
	path = settings.TEMP_DIR_IMAGE 
	datafile = os.listdir(path)
	url_media = settings.URL_MEDIA
	zip_media = settings.ZIP_MEDIA
	image_dir = settings.IMAGE_DIR
	count = 0
	unique = randomword(4)

	category = Category.objects.filter(status=1)
	models_name = ModelName.objects.all()

	if request.method == 'POST':
		data = request.POST.getlist('data')
		for x in data:
			print x
			src = ("{0}/{1}".format(path, x))
			dest = ("{0}/{1}".format(image_dir, x))
			print src
			print dest
			# copyfile(src, dest)
			move(src, dest)
		title = request.POST.get('title')

		post = Post(title=title.title())
		post.save()
		for x in data:
			ext = str(x).split('.')[-1]
			src = ("{0}/{1}".format(image_dir, x))
			dest = ("{0}/{1}_{2}_img_{3}.{4}".format(image_dir, unique, title.replace(" ", "_"), count, ext))
			print "data belum diubah %s" %src 
			print "data setelah diubah %s" %dest
			os.rename(src, dest)

			PostImage.objects.get_or_create(post=post, images="image/{0}_{1}_img_{2}.{3}".format(unique, title.replace(" ", "_"), count, ext))
			count = count + 1
		cat = request.POST.getlist('category')
		print cat
		for a in cat:
			CategoryPost.objects.get_or_create(post=post, category_id=int(a))
			print ''

		artis = request.POST.get('artis')

		print artis

		try:
			if artis is not None:
				ModelNamePost.objects.get_or_create(post=post, name_id=int(artis))
		except:
			pass

		return HttpResponseRedirect('/post')

			
	return render(request, 'export_to_post.html', {'datafile': datafile, 'url_media': url_media, 'path':path, 'category': category, 'models_name': models_name}) #{'form':form, }

@login_required(login_url='/login/')
def zip_post(request, post_id):
	data = get_object_or_404(Post, url_id=post_id)
	zip_media = settings.ZIP_MEDIA
	image_dir = settings.IMAGE_DIR
	x = str(data.title.title()).replace(" ", "")
	print x

	subprocess.call("rm -r {0}/*.zip".format(zip_media), shell=True)

	img =  data.images.all()

	for a in img:
		print a.images
		subprocess.call("zip -rj5 {0}/{1}.zip {2}/{3}".format(zip_media, x, settings.MEDIA_ROOT, a.images), shell=True)

	zip_file = open("{0}/{1}.zip".format(zip_media, x))
	response = HttpResponse(zip_file, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename="img_%s.zip"' % (x)
	return response

	# return render(request, 'detail.html', {'data': data})

def category_post(request, name):
	# category = CategoryPost.objects.filter(category__status=1)

	all_category = Category.objects.filter(status=1)
	category = CategoryPost.objects.filter(category__status=1)
	data =  category.filter(category__name=name)
	cat = data.values_list('category__name', flat=True)[0]

	post = Post.objects.all().order_by('-created')
	# print x
	paginator = Paginator(data, 10) 
	
	page = request.GET.get('page')
    
	try:
		postdata = paginator.page(page)
	except PageNotAnInteger:
		postdata = paginator.page(1)
	except EmptyPage:
		postdata = paginator.page(paginator.num_pages)

	return render(request, 'category.html', {'postdata': postdata, 'category':category, 'cat':cat, 'all_category': all_category, 'post':post})

def populer_post(request):
	# post = Post.objects.all()
	visitpost = VisitPagePost.objects.all().order_by('-count')[:5]

	# print visitpost
	return HttpResponse('view data')


def search_post(request):

	if request.method == 'POST':
		search = request.POST.get('search')
		print search

		post = Post.objects.filter(title__contains=search)
		print post

		category = CategoryPost.objects.filter(category__name=search)
		print category
	return render(request, 'search.html', {'search': search, 'post':post, 'category':category})


def model_list(request, name):
	post = Post.objects.all()

	name = name.replace('-', ' ')
	# print name

	model_list = ModelNamePost.objects.filter(name__name__contains=str(name))

	# print model_list

	paginator = Paginator(model_list.order_by('-post__created'), 3) # Show 25 contacts per page
	
	page = request.GET.get('page')

	try:
		postdata = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		postdata = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		postdata = paginator.page(paginator.num_pages)

	return render(request, 'models.html', {'postdata': postdata, 'name':name, 'post':post})

@login_required(login_url='/login/')
def add_modelname(request):
	# data = ModelName.objects.all()

	if request.method == 'POST':
		name = request.POST.get('name')
		description = request.POST.get('description')

		print name

		try:
			if not name == '':
				ModelName(name=name, description=description).save()
		except:
			pass



	return render(request, 'add_modelname.html')



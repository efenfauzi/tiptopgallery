# tiptopgallery
simple python-django web with image scrapper 

## fitured 
- image scrapping (get image from url)
- random thumb 
- featherlight gallery
- simple and fast organizing content (no need manual input admin)
- zipped gallery


# Screnshoot 
[![index.png](https://s6.postimg.org/a88az7mhd/index.png)](https://postimg.org/image/orfg0mfm5/)

[![scrap.png](https://s6.postimg.org/50rt8hv9t/scrap.png)](https://postimg.org/image/vylqa8fwt/)

[![output.png](https://s6.postimg.org/5p0nrftzl/output.png)](https://postimg.org/image/pwe3jqrgt/)

[![orgaizing.png](https://s6.postimg.org/4y3c7x28h/orgaizing.png)](https://postimg.org/image/q7qyirij1/)

[![gallery.png](https://s6.postimg.org/5et583fdd/gallery.png)](https://postimg.org/image/6tupwtggd/)

# Configuration

1. pip install -r requirements.txt

2. rename setings.py.example

3. change serving STATIC and MEDIA depend your config server(apache, nginx, etc...) see: https://docs.djangoproject.com/en/1.10/howto/static-files/

4. run `python manage.py collectstatic` then `yes`

5. run `python manage.py migrate` 

6. start the server by `python manage.py runserver` **PORT**

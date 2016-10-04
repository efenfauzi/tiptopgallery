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

1. create virtualenv, eg. `virtualenv venv`

2. activate virtualenv, install requirement --> `pip install -r requirements.txt`

3. rename settings.py.example in folder `bokepdo` to settings.py

4. change serving STATIC and MEDIA depend your config server(apache, nginx, etc...) see: https://docs.djangoproject.com/en/1.10/howto/static-files/

5. `python manage.py collectstatic` then `yes`

6. `python manage.py migrate` (this step render default django model)

7. `python manage.py makemigrations dashboard_admin` (this step render model aps)

8. `python manage.py migrate dashboard_admin` 

9. start the server by `python manage.py runserver` **PORT**

10. open http://localhost:**PORT** in web browser, see urls.py for more details

11. localhost:**port**/scrap , to scrapping image, login by default user/pass --> `root` : `root`

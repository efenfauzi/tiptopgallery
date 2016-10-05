FROM ubuntu:14.04
MAINTAINER TesxZZZ
RUN apt-get update && apt-get install -y python-dev gcc libxml2-dev libxslt1-dev libffi-dev libssl-dev python-pip

RUN mkdir -p /opt/tiptopgallery
WORKDIR /opt/tiptopgallery

COPY requirements.txt /opt/tiptopgallery/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/tiptopgallery

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver"]

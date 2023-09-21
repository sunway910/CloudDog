# docker build -t sunway/cpm:image20230921 -f Dockerfile .
# docker run -d  -p 8000:8000 -e DJANGO_MYSQL_HOST=172.17.0.1 -e DJANGO_MYSQL_PASSWORD=mysql8 -e DJANGO_MYSQL_USER=root -e DJANGO_MYSQL_DATABASE=djangoblog --name djangoblog sunway/djangoblog:image20230710
# when build a new image, copy the directory to container which is created by cronjob (/data/editor is the previous data in old container)
# docker exec -it djangoblog mkdir /code/djangoblog/uploads
# docker cp /data/editor djangoblog:/code/djangoblog/uploads/editor
FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /code/cpm/
RUN  apt-get install  default-libmysqlclient-dev -y && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip  && \
        pip install --no-cache-dir -r requirements.txt  && \
        pip install --no-cache-dir gunicorn[gevent] && \
        pip cache purge
        
ADD . .
RUN chmod +x /code/cpm/bin/docker_start.sh
ENTRYPOINT ["/code/cpm/bin/docker_start.sh"]

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
RUN chmod +x /code/cpm/start.sh
ENTRYPOINT ["/code/cpm/start.sh"]
# docker build -t sunway/cpm:image20230921 -f Dockerfile .
# docker run -d  --name postgres  -p 5432:5432 -e POSTGRES_PASSWORD=sunway  -v /data/postgres:/var/lib/postgresql/data  postgres:latest
# docker exec -it postgres psql -U postgres
# create database cpm;
# docker logs -f --tail=100 postgresql
# docker run -d  -p 8000:8000 -e DJANGO_POSTGRES_HOST=172.17.0.2  --name cpm  -v /data/cpm/log:/code/cpm/log   sunway/cpm:image20230921
# docker logs -f --tail=100 cpm
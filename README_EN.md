# Cloud Dog

[English document](https://github.com/0utsiderZhong/CloudDog/blob/main/README_EN.md)

A Finops tool base on Vue3, Django4 and Postgres

[Demo](https://www.runsunway.com)

**Dependency**

- Python 3.11
- Django 4.2.5
- Node 18.16.1
- Vue3
- Typescript
- Element Plus
- Unocss (Tailwind Css)
- Postgres

## Preface

This system is used to implement Finops of the cloud platform

## Features

1.
    - [ ] Aliyun/AlibabaCloud

    1.
        - [x] ECS monitor
    2.
        - [x] WAF monitor
    3.
        - [x] Load Balancer monitor

        1.
            - [x] ALB monitor
        2.
            - [x] SLB monitor
        3.
            - [ ] NLB monitor
    4.
        - [ ] RDS monitor
    5.
        - [ ] Redis monitor
    6.
        - [x] Elastic Internet IP monitor
    7.
        - [x] Cloud Security Center monitor
    8.
        - [ ] Cloud FireWall monitor
    9.
        - [x] SSL Certificate monitor
    10.
        - [ ] Billing monitor
2.
    - [ ] AWS

    1.
        - [ ] EC2 monitor
    2.
        - [ ] Billing monitor
3.
    - [ ] GCP

    1.
        - [ ] Compute Engine monitor
    2.
        - [ ] Billing monitor
4.
    - [ ] Azure

    1.
        - [ ] Virtual Machine monitor
    2.
        - [ ] Billing monitor
5.
    - [ ] Basic Features

    1.
        - [x] Login/Logout
    2.
        - [x] Data Export
    3.
        - [x] Email
    4.
        - [x] Cron Job
    5.
        - [x] Tab
    6.
        - [x] Django permission management
    7.
        - [x] Vue permission management
    8.
        - [x] Table
    9.
        - [x] Form
    10.
        - [x] pinia
    11.
        - [x] Toast
    12.
        - [x] vite 3
    13.
        - [x] axios
    14.
        - [x] i18n
    15.
        - [x] Localstorage Desensitization
    16.
        - [ ] postgres data encrypt
    17.
        - [ ] Echarts

## How To Start

```
git clone https://github.com/0utsiderZhong/CloudDog.git      
cd CloudDog   
cd backend
docker build -t xxx:clouddog2023 -f Dockerfile .
mkdir -p /data/postgres && mkdir -p /data/cpm/log
docker run -d  --name postgres  -p 5432:5432 -e POSTGRES_PASSWORD=sunway -v /data/postgres:/var/lib/postgresql/data  postgres:latest
docker run -d  -p 8000:8000 -e DJANGO_POSTGRES_HOST=<PG Container IP> --name cpm -v /data/cpm/log:/code/cpm/log xxx:clouddog2023

cd ../frontend 
pnpm build
docker build -t xxx:nginx2023 -f Dockerfile_Nginx .
docker run -d  -p 80:80 --name nginx xxx:nginx2023       

// run frontend
pnpm install
pnpm run dev

// build frontend
pnpm run build

// run backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## License

[MIT](https://github.com/0utsiderZhong/CloudDog/blob/main/LICENSE)
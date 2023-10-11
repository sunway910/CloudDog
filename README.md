# Cloud Dog

[English Document](https://github.com/0utsiderZhong/CloudDog/blob/main/README_EN.md)

基于 Vue3 + Django4 + Postgres 的Finops工具

[测试地址](https://www.runsunway.com)

**Dependency**

- Python 3.11
- Django 4.2.5
- Node 18.16.1
- Vue3
- Typescript
- Element Plus
- Unocss (Tailwind Css)
- Postgres

## 前言

该系统用于实现常用云平台的Finops

## 功能

1.
    - [ ] 阿里云/阿里云国际

    1.
        - [x] ECS 监控
    2.
        - [x] WAF 监控
    3.
        - [x] Load Balancer 监控

        1.
            - [x] ALB 监控
        2.
            - [x] SLB 监控
        3.
            - [ ] NLB 监控
    4.
        - [x] RDS 监控
    5.
        - [x] Redis 监控
    6.
        - [x] Elastic Internet IP 监控
    7.
        - [x] Cloud Security Center 监控
    8.
        - [ ] Cloud FireWall 监控
    9.
        - [x] SSL Certificate 监控
    10.
        - [ ] Billing 监控
2.
    - [ ] AWS

    1.
        - [ ] EC2 监控
    2.
        - [ ] Billing 监控
3.
    - [ ] GCP

    1.
        - [ ] Compute Engine 监控
    2.
        - [ ] Billing 监控
4.
    - [ ] Azure

    1.
        - [ ] Virtual Machine 监控
    2.
        - [ ] Billing 监控
5.
    - [ ] Basic 基础

    1.
        - [x] Login/Logout
    2.
        - [x] Data Export
    3.
        - [x] Email
    4.
        - [x] Cron Job
    5.
        - [x] Tab 选项卡
    6.
        - [x] Auth Django权限管理
    7.
        - [x] Auth Vue权限管理
    8.
        - [x] Table 表格
    9.
        - [x] Form 表单
    10.
        - [x] pinia
    11.
        - [x] Toast
    12.
        - [x] axios
    13.
        - [x] i18n
    14.
        - [x] Localstorage脱敏
    15.
        - [ ] postgres加密
    16.
        - [ ] Echarts
    17.
        - [ ] ASGI

## 安装步骤 How To Start

```
git clone https://github.com/0utsiderZhong/CloudDog.git      
cd CloudDog   
cd backend
docker build -t xxx:clouddog2023 -f Dockerfile .
mkdir -p /data/postgres && mkdir -p /data/clouddog/log
docker run -d  --name postgres  -p 5432:5432 -e POSTGRES_PASSWORD=sunway -v /data/postgres:/var/lib/postgresql/data  postgres:latest
docker run -d  -p 8000:8000 -e DJANGO_POSTGRES_HOST=<PG Container IP> --name clouddog -v /data/clouddog/log:/code/clouddog/log xxx:clouddog2023

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
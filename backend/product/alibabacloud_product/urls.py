from . import views
from django.urls import path

app_name = "alibabacloud"

urlpatterns = [
    path('api/ecs/list', views.get_ecs_list),
    path('api/ecs/call', views.call_ecs_api),

    path('api/waf/call', views.call_waf_api),
    path('api/waf/list', views.get_waf_list),

    path('api/slb/call', views.call_slb_api),
    path('api/slb/list', views.get_slb_list),

    path('api/alb/call', views.call_alb_api),
    path('api/alb/list', views.get_alb_list),

    path('api/eip/call', views.call_eip_api),
    path('api/eip/list', views.get_eip_list),

    path('api/ssl/call', views.call_ssl_api),
    path('api/ssl/list', views.get_ssl_list),

    path('api/csc/call', views.call_csc_api),
    path('api/csc/list', views.get_csc_list),

    path('api/rds/call', views.call_rds_api),
    path('api/rds/list', views.get_rds_list),

    path('api/redis/call', views.call_redis_api),
    path('api/redis/list', views.get_redis_list),
]

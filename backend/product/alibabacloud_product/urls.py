from . import views
from django.urls import path

app_name = "alibabacloud"

urlpatterns = [
    path('api/ecs/list', views.get_ecr_list),
    path('api/ecs/search', views.search_ecr),
    path('api/ecs/init', views.init_ecr_list),

    path('api/waf/init', views.init_waf_list),
    path('api/waf/list', views.get_waf_list),
    path('api/waf/search', views.search_waf),

    path('api/slb/init', views.init_slb_list),
    path('api/slb/list', views.get_slb_list),
    path('api/slb/search', views.search_slb),

    path('api/alb/init', views.init_alb_list),
    path('api/alb/list', views.get_alb_list),
    path('api/alb/search', views.search_alb),
]

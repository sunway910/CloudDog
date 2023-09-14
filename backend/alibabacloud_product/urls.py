from . import views
from django.urls import path

app_name = "ecs"

urlpatterns = [
    path('api/ecs/list', views.get_ecr_list),
    path('api/ecs/search', views.search_ecr),
    path('api/ecs/init', views.init_ecr_list),
    path('api/waf/init', views.init_waf_list),
]

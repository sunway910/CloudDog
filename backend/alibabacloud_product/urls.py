from . import views
from django.urls import path

app_name = "ecs"

urlpatterns = [
    path('api/ecs/list', views.get_list),
    path('api/ecs/search', views.search),
]

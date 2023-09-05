from . import views
from django.urls import path

app_name = "project"

urlpatterns = [
    path('api/project/list', views.list_api),
    path('api/project/detail', views.detail),
    path('api/project/create', views.create),
    path('api/project/update', views.update),
    path('api/project/delete', views.delete),
]

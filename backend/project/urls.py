from . import views
from django.urls import path

app_name = "project"

urlpatterns = [
    path('api/project/list', views.get_list),
    path('api/project/search', views.search),
    path('api/project/create_or_update', views.create_or_update),
    path('api/project/delete', views.delete),
]

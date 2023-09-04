from . import views
from django.urls import path
from django.views.decorators.cache import cache_page

app_name = "project"

urlpatterns = [
    path(r'list', views.ProjectViewSet.as_view, name='list'),
    path('<str:project_name>', views.ProjectViewSet.as_view, name='detail'),
]

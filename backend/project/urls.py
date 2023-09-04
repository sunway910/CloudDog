from . import views
from django.urls import path
from django.views.decorators.cache import cache_page

app_name = "project"

urlpatterns = [
    path(r'api/project/list', views.ProjectViewSet.as_view),
]

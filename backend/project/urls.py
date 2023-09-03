from django.urls import path
from project import views

urlpatterns = [
    path('api/project/list', views.get_project_list),
    path('api/project/edit/(P<pk>[0-9]+)', views.write_project)
]

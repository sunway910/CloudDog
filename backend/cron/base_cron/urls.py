from django.urls import path
from . import views

app_name = "job"

urlpatterns = [path('api/job/list', views.DjangoJobBaseViewSet().get_job_list),
               path('api/job/exec_list', views.DjangoJobBaseViewSet().get_job_exec_list),
               path('api/job/search', views.DjangoJobBaseViewSet().search),
               ]

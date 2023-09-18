from django.urls import path
from . import views

app_name = "job"

urlpatterns = [path('api/job/list', views.DjangoJobBaseViewSet().get_list), path('api/job/search', views.DjangoJobBaseViewSet().search)]

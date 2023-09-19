from . import views
from django.urls import path

app_name = "message"

urlpatterns = [
    path('api/message/list', views.get_list),
    path('api/message/search', views.search),
    path('api/message/update', views.update),
]

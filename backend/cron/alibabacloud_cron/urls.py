from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import AliECSDjangoJobViewSet, AliWAFDjangoJobViewSet

router = routers.DefaultRouter()

router.register('ali_ecs_job', AliECSDjangoJobViewSet)
router.register('ali_waf_job', AliWAFDjangoJobViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

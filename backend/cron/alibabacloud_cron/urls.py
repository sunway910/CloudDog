from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register('ali_ecs_job', AliECSDjangoJobViewSet)
router.register('ali_waf_job', AliWAFDjangoJobViewSet)
router.register('ali_slb_job', AliSLBDjangoJobViewSet)
router.register('ali_alb_job', AliALBDjangoJobViewSet)
router.register('ali_eip_job', AliEIPDjangoJobViewSet)
router.register('ali_ssl_job', AliSSLDjangoJobViewSet)
router.register('ali_csc_job', AliCSCDjangoJobViewSet)
router.register('ali_rds_job', AliRDSDjangoJobViewSet)
router.register('ali_redis_job', AliRedisDjangoJobViewSet)
router.register('ali_cfw_job', AliCFWDjangoJobViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

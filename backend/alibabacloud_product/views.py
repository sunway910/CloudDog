import logging

from .models import EcsProject, WafProject, ProductType
from .permissions import IsAdminUserOrReadOnly
from django.views.generic.list import ListView
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


# Models CRUD
class InstanceBasicViewList(ListView):
    permission_classes = [IsAdminUserOrReadOnly]
    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    product_type = ProductType.ECS

    @property
    def get_page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset_cache_key(self):
        raise NotImplementedError()

    def get_queryset_all_data(self):
        raise NotImplementedError()

    def get_queryset_is_bad(self):
        """
        is bad means that instance is stopped, expired or something bad
        """
        raise NotImplementedError()

    def get_queryset_is_good(self):
        """
        is good means that instance is running, keep working or something like that
        """
        raise NotImplementedError()

    def get_data_from_cache(self, cache_key):
        value = cache.get(cache_key)
        # get data from cache
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        # get data from db and data to cache
        else:
            instance_list = self.get_queryset_all_data()
            cache.set(cache_key, instance_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return instance_list

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = self.get_data_from_cache(key)
        return value

    def get_context_data(self, **kwargs):
        kwargs['productType'] = self.product_type
        return super(InstanceBasicViewList, self).get_context_data(**kwargs)


class EcsViewList(InstanceBasicViewList):
    product_type = ProductType.ECS

    def get_queryset_cache_key(self):
        """
        Front-end get data from cache via cache-key
        """
        cache_key = 'ecs_info_{page_number}'.format(page_number=self.get_page_number)
        return cache_key

    def get_queryset_all_data(self):
        """
        get all ecs instances
        """
        ecs_list = EcsProject.objects.all()
        return ecs_list

    def get_queryset_is_bad(self):
        """
        get all ecs instances which status is stopped
        """
        ecs_list = EcsProject.objects.filter(ecs_status='Stopped')
        return ecs_list

    def get_queryset_is_good(self):
        """
        get all ecs instances which status is running
        """
        ecs_list = EcsProject.objects.filter(ecs_status='Running')
        return ecs_list


class WafViewList(InstanceBasicViewList):
    product_type = ProductType.WAF

    def get_queryset_cache_key(self):
        """
        Front-end get data from cache via cache-key
        """
        cache_key = 'waf_info_{page_number}'.format(page_number=self.get_page_number)
        return cache_key

    def get_queryset_all_data(self):
        """
        get all waf instances
        """
        waf_list = WafProject.objects.all()
        return waf_list

    def get_queryset_is_bad(self):
        """
        get all waf instances which status is expired
        """
        waf_list = WafProject.objects.filter(waf_status=0)
        return waf_list

    def get_queryset_is_good(self):
        """
        get all waf instances which status is keep working
        """
        waf_list = WafProject.objects.filter(waf_status=1)
        return waf_list

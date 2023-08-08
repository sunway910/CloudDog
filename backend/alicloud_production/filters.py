from django_filters import rest_framework as filters

from .models import EcsInstance, WafInstance, BaseModel


class ApiResponseFilter(filters.FilterSet):
    """
    自定义文章标题过滤器类，实现对文章标题进行模糊搜索(不区分大小写)
    """
    title = filters.CharFilter(field_name='instance_id', lookup_expr='icontains', label='状态(模糊搜索且不区分大小写)')

    class Meta:
        model = BaseModel
        fields = ['instance_id']

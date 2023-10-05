from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer
from product.alibabacloud_product.models import *


class AlibabacloudEcsApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudEcsApiResponse
        fields = '__all__'


class AlibabacloudWafApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudWafApiResponse
        fields = '__all__'


class AlibabacloudSlbApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudSLBApiResponse
        fields = '__all__'


class AlibabacloudAlbApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudALBApiResponse
        fields = '__all__'


class AlibabacloudEipApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudEIPApiResponse
        fields = '__all__'


class AlibabacloudSSLApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudSSLApiResponse
        fields = '__all__'


class AlibabacloudCSCApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudCSCApiResponse
        fields = '__all__'

from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer
from alibabacloud_product.models import AlibabacloudEcsApiResponse, AlibabacloudWafApiResponse


class AlibabacloudEcsApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudEcsApiResponse
        fields = '__all__'


class AlibabacloudWafApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudWafApiResponse
        fields = '__all__'

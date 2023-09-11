from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer
from alibabacloud_product.models import AlibabacloudEcsApiResponse


class AlibabacloudEcsApiResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AlibabacloudEcsApiResponse
        fields = '__all__'

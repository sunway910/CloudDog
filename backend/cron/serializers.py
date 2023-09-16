from django_apscheduler.models import DjangoJob
from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer


class DjangoJobSerializer(DynamicFieldsModelSerializer):
    class Meta:
        fields = '__all__'
        model = DjangoJob

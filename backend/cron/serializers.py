from django_apscheduler.models import DjangoJob, DjangoJobExecution
from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer


class DjangoJobSerializer(DynamicFieldsModelSerializer):
    class Meta:
        fields = '__all__'
        model = DjangoJob


class DjangoJobExecutionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        fields = '__all__'
        model = DjangoJobExecution

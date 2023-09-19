from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer
from message.models import Event


class EventSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

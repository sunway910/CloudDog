from dynamicFieldsModelSerializer import DynamicFieldsModelSerializer
from project.models import Project


class ProjectSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

from rest_framework import serializers
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    # 声明需要被序列化和反序列化的字段，同 model 的字段，
    # 字段名注意需要同 model 字段同名
    id = serializers.IntegerField()
    cloud_platform = serializers.CharField(max_length=100, allow_blank=True)
    account = serializers.CharField(max_length=100, allow_blank=True)
    project_name = serializers.CharField(max_length=100, allow_blank=True)
    project_access_key = serializers.CharField(max_length=100, allow_blank=True)
    project_secret_key = serializers.CharField(max_length=100, allow_blank=True)
    key_authority = serializers.CharField(max_length=100, allow_blank=True)
    create_time = serializers.DateTimeField()

    # 定义创建方法
    def create(self, validated_date):
        return Project.objects.all()

    # 定义修改方法
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.cloud_platform = validated_data.get('cloud_platform', instance.cloud_platform)
        instance.account = validated_data.get('account', instance.account)
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.project_access_key = validated_data.get('project_access_key', instance.project_access_key)
        instance.project_secret_key = validated_data.get('project_secret_key', instance.project_secret_key)
        instance.key_authority = validated_data.get('key_authority', instance.key_authority)
        instance.create_time = validated_data.get('create_time', instance.create_time)

    class Meta:
        model = Project
        fields = ('id',
                  'cloud_platform',
                  'account',
                  'project_name',
                  'project_access_key',
                  'project_secret_key',
                  'key_authority',
                  'create_time'
                  )

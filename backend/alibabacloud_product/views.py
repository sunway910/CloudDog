import logging

from .models import EcsInstance, WafProduct, ProductType
from .permissions import IsAdminUserOrReadOnly
from django.views.generic.list import ListView
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)
import asyncio
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from handler import APIResponse
from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permissions import IsAdminUserOrReadOnly
import logging
import time
import json
import datetime


def create_client(access_key_id: str, access_key_secret: str, ) -> Ecs20140526Client:
    """
    使用AK&SK初始化账号Client
    @param access_key_id: LTAI5sQAwvrwHZQx7PuG2ur4
    @param access_key_secret: ijWtg8hCaptL3U73U7PsFqNCLQwEG2
    @return: Ecs20140526Client
    @throws Exception
    """
    config = open_api_models.Config(
        # your AccessKey ID,
        access_key_id=access_key_id,
        # your AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/Ecs
    config.endpoint = f'ecs-cn-hangzhou.aliyuncs.com'
    return Ecs20140526Client(config)


def main_async() -> None:
    # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
    client = create_client('LTAI5t74a9Xot9saANDiHYYN', 'iA5fEqkzFVPxFIO7TePVaNSjty3OG1')
    runtime = util_models.RuntimeOptions()
    describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id='cn-hongkong')
    instance_ids = []
    try:
        DescribeInstanceResponse = client.describe_instances_with_options(describe_instances_request, runtime)
        DescribeInstanceResponseToStr = UtilClient.to_jsonstring(DescribeInstanceResponse)
        # ConsoleClient.log(DescribeInstanceResponseToStr)
        DescribeInstanceResponseJsonObject = json.loads(DescribeInstanceResponseToStr)
        print('Response code: ', DescribeInstanceResponseJsonObject['statusCode'])
        instance_list = DescribeInstanceResponseJsonObject['body']['Instances']['Instance']
        for instance in instance_list:
            ecs = EcsInstance()
            ecs.api_request_id = "str(instance['RequestId'])"
            ecs.instance_id = instance['InstanceId']
            ecs.request_time = datetime.time
            ecs.product_type = instance['InstanceTypeFamily']
            # ecs.project = 'mtr'
            ecs.region_id = instance['RegionId']
            ecs.ecs_status = instance['Status']
            ecs.instance_charge_type = instance['InstanceChargeType']
            ecs.internet_charge_type = instance['InternetChargeType']
            ecs.expired_time = instance['ExpiredTime']
            ecs.stopped_mode = instance['StoppedMode']
            ecs.auto_release_time = instance['AutoReleaseTime']
            ecs.lock_reason = instance['OperationLocks']['LockReason']
            print("ecs ===== ", ecs.__str__())
            ecs.save()
            print('实例ID：', instance['InstanceId'])
            print('实例地域：', instance['RegionId'])
            print('实例状态：', instance['Status'])
            instance_ids.append(instance['InstanceId'])
            print('付费类型：', instance['InstanceChargeType'])
            print('过期时间', instance['ExpiredTime'])
            # KeepCharging：停机后继续收费，为您继续保留库存资源。
            # StopCharging：停机后不收费。停机后，我们释放实例对应的资源，例如vCPU、内存和公网IP等资源。重启是否成功依赖于当前地域中是否仍有资源库存。
            # Not-applicable：本实例不支持停机不收费功能
            print('实例停机后是否继续收费：', instance['StoppedMode'])
            print('实例最近一次的启动时间：', instance['StartTime'])
            print('按 固定带宽/使用流量 计费：', instance['InternetChargeType'])
            print('按量付费实例的自动释放时间：', instance['AutoReleaseTime'])
            # financial：因欠费被锁定。security：因安全原因被锁定。Recycling：抢占式实例的待释放锁定状态。dedicatedhostfinancial：因为专有宿主机欠费导致ECS实例被锁定。refunded：因退款被锁定。"
            print('实例的锁定原因：', instance['OperationLocks']['LockReason'])
        for instance_id in instance_ids:
            describe_instance_auto_renew_attribute_request = ecs_20140526_models.DescribeInstanceAutoRenewAttributeRequest(region_id='cn-hongkong', instance_id=instance_id)
            DescribeInstanceAutoRenewAttributeResponse = client.describe_instance_auto_renew_attribute_with_options(describe_instance_auto_renew_attribute_request, runtime)
            DescribeInstanceAutoRenewAttributeResponseToStr = UtilClient.to_jsonstring(DescribeInstanceAutoRenewAttributeResponse)
            # ConsoleClient.log(DescribeInstanceAutoRenewAttributeResponseToStr)
            DescribeInstanceAutoRenewAttributeResponseJsonObject = json.loads(DescribeInstanceAutoRenewAttributeResponseToStr)
            instance_info = DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
            print('是否已开启自动续费功能: ', instance_info['AutoRenewEnabled'])
            print('实例的自动续费状态: ', instance_info['RenewalStatus'])
            print('自动续费时长的单位: ', instance_info['PeriodUnit'])
            print('自动续费时长: ', instance_info['Duration'])
            # ecs.period_init = instance['InstanceTypeFamily']
            # ecs.duration = instance['InstanceTypeFamily']
            # ecs.auto_renew_enabled = instance['InstanceTypeFamily']
            # ecs.renewal_status = instance['InstanceTypeFamily']
            print('-----------------------------------------------------------------------------------------------------------------------------')
            print('-----------------------------------------------------------------------------------------------------------------------------')

    except Exception as error:
        UtilClient.assert_as_string(error)


# Models CRUD
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_list(request):
    main_async()


# select * from project where project.project_name = project_name and cloud_platform = cloud_platform
# projectList = Project.objects.all().extra(tables=['project'], where=['project.project_name = project_name', 'cloud_platform = cloud_platform'])
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search(request):
    try:
        cloud_platform = request.GET.get('cloud_platform', None)
        project_name = request.GET.get('project_name', None)
        queryset = Project.objects.all()
        if cloud_platform and cloud_platform != "All":
            queryset = queryset.filter(cloud_platform=cloud_platform)
        if project_name:
            queryset = queryset.filter(project_name__icontains=project_name)
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = ProjectSerializer(queryset, many=True, fields=('id', 'cloud_platform', 'region', 'account', 'project_name', 'status', 'create_time', 'cron_expression', 'cron_toggle'))
    return APIResponse(code=0, msg='request successfully', data=serializer.data)

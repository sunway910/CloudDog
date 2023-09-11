from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from alibabacloud_product.serializers import AlibabacloudEcsApiResponseSerializer
from handler import APIResponse
from project.models import Project
from alibabacloud_product.models import AlibabacloudEcsApiResponse, AlibabacloudWafApiResponse
from asgiref.sync import sync_to_async


import logging
import asyncio
import json

logger = logging.getLogger(__name__)


def create_client(access_key_id: str, access_key_secret: str, ) -> EcsApiClient:
    """
    use AK&SK to init Client
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
    # Endpoint Ref: https://api.aliyun.com/product/Ecs
    config.endpoint = f'ecs-cn-hangzhou.aliyuncs.com'
    return EcsApiClient(config)


@sync_to_async
def get_ecs_api_response() -> None:
    project_list = Project.objects.filter(project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True).values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = create_client(project['project_access_key'], project['project_secret_key'])
        for region in project['region']:
            describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id=region)
            try:
                # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances
                DescribeInstanceResponse = client.describe_instances_with_options(describe_instances_request, runtime)
                DescribeInstanceResponseToStr = UtilClient.to_jsonstring(DescribeInstanceResponse)
                DescribeInstanceResponseJsonObject = json.loads(DescribeInstanceResponseToStr)
                instance_list = DescribeInstanceResponseJsonObject['body']['Instances']['Instance']
                for instance in instance_list:
                    describe_instance_auto_renew_attribute_request = ecs_20140526_models.DescribeInstanceAutoRenewAttributeRequest(region_id=region, instance_id=instance['InstanceId'])
                    # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstanceAutoRenewAttribute
                    DescribeInstanceAutoRenewAttributeResponse = client.describe_instance_auto_renew_attribute_with_options(describe_instance_auto_renew_attribute_request, runtime)
                    DescribeInstanceAutoRenewAttributeResponseToStr = UtilClient.to_jsonstring(DescribeInstanceAutoRenewAttributeResponse)
                    DescribeInstanceAutoRenewAttributeResponseJsonObject = json.loads(DescribeInstanceAutoRenewAttributeResponseToStr)
                    InstanceAutoRenewInfo = DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
                    # request 2 API and get two request id, so the new request id is formed by combining two request id
                    requestId = DescribeInstanceResponseJsonObject['body']['RequestId'] + " " + DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['RequestId']
                    ecs = AlibabacloudEcsApiResponse(api_request_id=requestId,
                                                     instance_id=instance['InstanceId'],
                                                     project_name=project['project_name'],
                                                     instance_name=instance['InstanceName'],
                                                     project_id=project['id'],
                                                     region_id=instance['RegionId'],
                                                     ecs_status=instance['Status'],
                                                     instance_charge_type=instance['InstanceChargeType'],
                                                     internet_charge_type=instance['InternetChargeType'],
                                                     expired_time=instance['ExpiredTime'],
                                                     stopped_mode=instance['StoppedMode'],
                                                     start_time=instance['StartTime'],
                                                     auto_release_time=instance['AutoReleaseTime'],
                                                     lock_reason=instance['OperationLocks']['LockReason'],
                                                     auto_renew_enabled=InstanceAutoRenewInfo['AutoRenewEnabled'],
                                                     renewal_status=InstanceAutoRenewInfo['RenewalStatus'],
                                                     period_init=InstanceAutoRenewInfo['PeriodUnit'],
                                                     duration=InstanceAutoRenewInfo['Duration'],
                                                     )
                    logger.info(ecs.get_basic_info())
                    ecs.save()
            except Exception as error:
                UtilClient.assert_as_string(error)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_list(request):
    res = asyncio.run(get_ecs_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_list(request):
    alibabacloudEcsApiResponse = AlibabacloudEcsApiResponse.objects.all()
    serializer = AlibabacloudEcsApiResponseSerializer(alibabacloudEcsApiResponse, many=True)
    return APIResponse(code=0, msg='success', data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search(request):
    try:
        cloud_platform = request.GET.get('cloud_platform', None)
        project_name = request.GET.get('project_name', None)
        queryset = AlibabacloudEcsApiResponse.objects.all()
        if cloud_platform and cloud_platform != "All":
            queryset = queryset.filter(cloud_platform=cloud_platform)
        if project_name:
            queryset = queryset.filter(project_name__icontains=project_name)
    except AlibabacloudEcsApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudEcsApiResponseSerializer(queryset, many=True)
    return APIResponse(code=0, msg='request successfully', data=serializer.data)

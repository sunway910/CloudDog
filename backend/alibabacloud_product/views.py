from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from alibabacloud_waf_openapi20211001.client import Client as WAFApiClient
from alibabacloud_waf_openapi20211001 import models as waf_openapi_20211001_models

from alibabacloud_product.serializers import AlibabacloudEcsApiResponseSerializer
from handler import APIResponse
from paginator import CustomPaginator
from project.models import Project
from alibabacloud_product.models import AlibabacloudEcsApiResponse, AlibabacloudWafApiResponse
from asgiref.sync import sync_to_async

import logging
import asyncio
import json

logger = logging.getLogger(__name__)


def create_ecs_client(access_key_id: str, access_key_secret: str, ) -> EcsApiClient:
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


def create_waf_client(access_key_id: str, access_key_secret: str, ) -> WAFApiClient:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/waf-openapi
    config.endpoint = f'wafopenapi.ap-southeast-1.aliyuncs.com'
    return WAFApiClient(config)


@sync_to_async
def get_ecr_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = create_ecs_client(project['project_access_key'], project['project_secret_key'])
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


@sync_to_async
def get_waf_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    print("project_list", project_list)
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = create_waf_client(project['project_access_key'], project['project_secret_key'])
        describe_instance_info_request = waf_openapi_20211001_models.DescribeInstanceRequest(
            region_id='ap-southeast-1'
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.describe_instance_with_options(describe_instance_info_request, runtime)
            DescribeWAFAttributeResponseToStr = UtilClient.to_jsonstring(res)
            DescribeWAFAttributeResponseJsonObject = json.loads(DescribeWAFAttributeResponseToStr)
            print("WAF INFO==", DescribeWAFAttributeResponseJsonObject['body'])
            wafInfo = DescribeWAFAttributeResponseJsonObject['body']
            waf = AlibabacloudWafApiResponse(api_request_id=wafInfo['RequestId'],
                                             instance_id=wafInfo['InstanceId'],
                                             project_name=project['project_name'],
                                             project_id=project['id'],
                                             waf_status=wafInfo['Status'],
                                             end_time=wafInfo['EndTime'],
                                             version=wafInfo['Edition'],
                                             region=wafInfo['RegionId'],
                                             pay_type=wafInfo['PayType'],
                                             in_debt=wafInfo['InDebt'],
                                             start_time=wafInfo['StartTime'],
                                             )
            logger.info(waf.get_basic_info())
            waf.save()
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_ecr_list(request):
    res = asyncio.run(get_ecr_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_waf_list(request):
    res = asyncio.run(get_waf_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ecr_list(request):
    alibabacloudEcsApiResponse = AlibabacloudEcsApiResponse.objects.all()
    paginator = CustomPaginator(request, alibabacloudEcsApiResponse)
    total = paginator.count
    data = paginator.get_page()
    serializer = AlibabacloudEcsApiResponseSerializer(data, many=True)
    return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_ecr(request):
    try:
        cloud_platform = request.GET.get('cloud_platform', None)
        project_name = request.GET.get('project_name', None)
        alibabacloudEcsApiResponse = AlibabacloudEcsApiResponse.objects.all()
        if cloud_platform and cloud_platform != "All":
            alibabacloudEcsApiResponse = alibabacloudEcsApiResponse.filter(cloud_platform=cloud_platform)
        if project_name:
            alibabacloudEcsApiResponse = alibabacloudEcsApiResponse.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloudEcsApiResponse)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudEcsApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudEcsApiResponseSerializer(data, many=True)
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)

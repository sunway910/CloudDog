import asyncio
import json

from alibabacloud_alb20200616 import models as alb_20200616_models
from alibabacloud_alb20200616.client import Client as AlbApiClient
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_ecs20140526.client import Client as EcsApiClient
from alibabacloud_slb20140515 import models as slb_20140515_models
from alibabacloud_slb20140515.client import Client as SlbApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_waf_openapi20211001 import models as waf_openapi_20211001_models
from alibabacloud_waf_openapi20211001.client import Client as WAFApiClient
from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.settings import ENDPOINT
from handler import APIResponse
from paginator import CustomPaginator
from product.alibabacloud_product.serializers import *
from project.models import Project

logger = logging.getLogger('clouddog')


def set_client_config(access_key_id: str, access_key_secret: str, endpoint: str) -> open_api_models.Config:
    """
    use AK&SK to init Client
    @param access_key_id: LTAI5sQAwvrwHZQx7PuG2ur4
    @param access_key_secret: ijWtg8hCaptL3U73U7PsFqNCLQwEG2
    @param endpoint: ecs-cn-hangzhou.aliyuncs.com
    @return: OpenApiClient
    @throws Exception
    """
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = endpoint  # Endpoint Ref: https://api.aliyun.com/product/Ecs
    return config


@sync_to_async
def get_ecs_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = EcsApiClient(set_client_config(
            project['project_access_key'],
            project['project_secret_key'],
            ENDPOINT['WAF_ENDPOINT']['oversea'])
        )
        for region in project['region']:
            describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id=region)
            try:
                # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances
                describe_instance_response = client.describe_instances_with_options(describe_instances_request, runtime)
                describe_instance_response_to_str = UtilClient.to_jsonstring(describe_instance_response)
                describe_instance_response_json_obj = json.loads(describe_instance_response_to_str)
                instance_list = describe_instance_response_json_obj['body']['Instances']['Instance']
                for instance in instance_list:
                    describe_instance_auto_renew_attribute_request = ecs_20140526_models.DescribeInstanceAutoRenewAttributeRequest(region_id=region, instance_id=instance['InstanceId'])
                    # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstanceAutoRenewAttribute
                    describe_instance_auto_renew_attribute_response = client.describe_instance_auto_renew_attribute_with_options(describe_instance_auto_renew_attribute_request, runtime)
                    describe_instance_auto_renew_attribute_response_to_str = UtilClient.to_jsonstring(describe_instance_auto_renew_attribute_response)
                    describe_instance_auto_renew_attribute_response_json_obj = json.loads(describe_instance_auto_renew_attribute_response_to_str)
                    if describe_instance_auto_renew_attribute_response_json_obj['body']['TotalCount'] > 0:
                        instance_auto_renew_info = describe_instance_auto_renew_attribute_response_json_obj['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
                        # request 2 API and get two request id, so the new request id is formed by combining two request id
                        request_id = describe_instance_response_json_obj['body']['RequestId'] + " " + describe_instance_auto_renew_attribute_response_json_obj['body']['RequestId']
                        ecs = AlibabacloudEcsApiResponse(api_request_id=request_id,
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
                                                         auto_renew_enabled=instance_auto_renew_info['AutoRenewEnabled'],
                                                         renewal_status=instance_auto_renew_info['RenewalStatus'],
                                                         period_init=instance_auto_renew_info['PeriodUnit'],
                                                         duration=instance_auto_renew_info['Duration'],
                                                         )
                        logger.info(ecs.get_basic_info())
                        ecs.save()
            except Exception as error:
                UtilClient.assert_as_string(error)


@sync_to_async
def get_waf_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()

    for project in project_list:
        client = WAFApiClient(set_client_config(
            project['project_access_key'],
            project['project_secret_key'],
            ENDPOINT['WAF_ENDPOINT']['oversea'])
        )
        describe_instance_info_request = waf_openapi_20211001_models.DescribeInstanceRequest()
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.describe_instance_with_options(describe_instance_info_request, runtime)
            describe_waf_attribute_response_to_str = UtilClient.to_jsonstring(res)
            describe_waf_attribute_response_json_obj = json.loads(describe_waf_attribute_response_to_str)
            waf_info = describe_waf_attribute_response_json_obj['body']
            waf = AlibabacloudWafApiResponse(api_request_id=waf_info['RequestId'],
                                             instance_id=waf_info['InstanceId'],
                                             project_name=project['project_name'],
                                             project_id=project['id'],
                                             waf_status=waf_info['Status'],
                                             end_time=waf_info['EndTime'],
                                             edition=waf_info['Edition'],
                                             region=waf_info['RegionId'],
                                             pay_type=waf_info['PayType'],
                                             in_debt=waf_info['InDebt'],
                                             start_time=waf_info['StartTime'], )
            logger.info(waf.get_basic_info())
            waf.save()
        except Exception as error:
            UtilClient.assert_as_string(error)


@sync_to_async
def get_slb_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        client = SlbApiClient(set_client_config(project['project_access_key'],
                                                project['project_secret_key'],
                                                ENDPOINT['SLB_ENDPOINT']['general']))
        for region in project['region']:
            describe_load_balancers_request = slb_20140515_models.DescribeLoadBalancersRequest(region_id=region)
            try:
                res = client.describe_load_balancers_with_options(describe_load_balancers_request, runtime)
                describe_slb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_slb_attribute_response_json_obj = json.loads(describe_slb_attribute_response_to_str)
                if describe_slb_attribute_response_json_obj['body']['TotalCount'] > 0:
                    slb_info = describe_slb_attribute_response_json_obj['body']['LoadBalancers']
                    for num, slb_instance in enumerate(slb_info):
                        describe_load_balancer_attribute_request = slb_20140515_models.DescribeLoadBalancerAttributeRequest(region_id=region, load_balancer_id=slb_instance['InstanceId'])
                        detail_res = client.describe_load_balancer_attribute_with_options(describe_load_balancer_attribute_request, runtime)
                        describe_slb_detail_attribute_response_to_str = UtilClient.to_jsonstring(detail_res)
                        describe_slb_detail_attribute_response_json_obj = json.loads(describe_slb_detail_attribute_response_to_str)
                        slb_instance_detail = describe_slb_detail_attribute_response_json_obj['body']
                        slb = AlibabacloudSLBApiResponse(api_request_id=(describe_slb_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=slb_instance['InstanceId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         bandwidth=slb_instance_detail['Bandwidth'],
                                                         end_time_stamp=slb_instance_detail['EndTimeStamp'],
                                                         end_time=slb_instance_detail['EndTime'],
                                                         auto_release_time=slb_instance_detail['AutoReleaseTime'],
                                                         renewal_status=slb_instance_detail['RenewalStatus'],
                                                         renewal_duration=slb_instance_detail['RenewalDuration'],
                                                         renewal_cyc_unit=slb_instance_detail['RenewalCycUnit'],
                                                         create_time=slb_instance['CreateTime'],
                                                         pay_type=slb_instance['PayType'],
                                                         internet_charge_type=slb_instance['InternetChargeType'],
                                                         load_balancer_name=slb_instance['LoadBalancerName'],
                                                         address=slb_instance['Address'],
                                                         address_type=slb_instance['AddressType'],
                                                         address_ip_version=slb_instance['AddressIPVersion'],
                                                         region_id=slb_instance['RegionId'],
                                                         load_balancer_status=slb_instance['LoadBalancerStatus'],
                                                         load_balancer_spec=slb_instance['LoadBalancerSpec'],
                                                         instance_charge_type=slb_instance['InstanceChargeType'],
                                                         master_zone_id=slb_instance['MasterZoneId'],
                                                         slave_zone_id=slb_instance['SlaveZoneId'],
                                                         )
                        logger.info(slb.get_basic_info())
                        slb.save()
            except Exception as error:
                UtilClient.assert_as_string(error)


@sync_to_async
def get_alb_api_response() -> None:
    project_list = Project.objects.filter(status='Running', project_access_key__isnull=False, project_secret_key__isnull=False, cron_toggle=True). \
        values('project_access_key', 'project_secret_key', 'region', 'project_name', 'id')
    runtime = util_models.RuntimeOptions()
    for project in project_list:
        for region in project['region']:
            client = AlbApiClient(set_client_config(project['project_access_key'],
                                                    project['project_secret_key'],
                                                    ENDPOINT['ALB_ENDPOINT'][region]))
            list_load_balancers_request = alb_20200616_models.ListLoadBalancersRequest()
            try:
                res = client.list_load_balancers_with_options(list_load_balancers_request, runtime)
                describe_alb_attribute_response_to_str = UtilClient.to_jsonstring(res)
                describe_alb_attribute_response_json_obj = json.loads(describe_alb_attribute_response_to_str)
                if describe_alb_attribute_response_json_obj['body']['TotalCount'] > 0:
                    alb_info = describe_alb_attribute_response_json_obj['body']['LoadBalancers']
                    for num, alb_instance in enumerate(alb_info):
                        alb = AlibabacloudALBApiResponse(api_request_id=(describe_alb_attribute_response_json_obj['body']['RequestId'] + str(num)),
                                                         instance_id=alb_instance['LoadBalancerId'],
                                                         project_name=project['project_name'],
                                                         project_id=project['id'],
                                                         create_time=alb_instance['CreateTime'],
                                                         address_allocated_mode=alb_instance['AddressAllocatedMode'],
                                                         address_type=alb_instance['AddressType'],
                                                         dns_name=alb_instance['DNSName'],
                                                         pay_type=alb_instance['LoadBalancerBillingConfig']['PayType'],
                                                         load_balancer_bussiness_status=alb_instance['LoadBalancerBussinessStatus'],
                                                         load_balancer_edition=alb_instance['LoadBalancerEdition'],
                                                         load_balancer_name=alb_instance['LoadBalancerName'],
                                                         load_balancer_status=alb_instance['LoadBalancerStatus'],
                                                         address_ip_version=alb_instance['AddressIpVersion'],
                                                         )
                        if alb.address_ip_version != 'Ipv4':
                            alb.ipv6_address_type = alb_instance['Ipv6AddressType']
                        logger.info(alb.get_basic_info())
                        alb.save()
            except Exception as error:
                UtilClient.assert_as_string(error)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_ecr_list(request):
    res = asyncio.run(get_ecs_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ecr_list(request):
    alibabacloud_ecs_api_response = AlibabacloudEcsApiResponse.objects.all().order_by("project_id")
    paginator = CustomPaginator(request, alibabacloud_ecs_api_response)
    total = paginator.count
    data = paginator.get_page()
    serializer = AlibabacloudEcsApiResponseSerializer(data, many=True)
    logger.info("{} call get_ecr_list api".format(request.user.username))
    return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_ecr(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_ecs_api_response = AlibabacloudEcsApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_ecs_api_response = alibabacloud_ecs_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_ecs_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudEcsApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudEcsApiResponseSerializer(data, many=True)
    logger.info("{} call search_ecr api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_waf_list(request):
    res = asyncio.run(get_waf_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_waf_list(request):
    alibabacloud_waf_api_response = AlibabacloudWafApiResponse.objects.all().order_by("project_id")
    paginator = CustomPaginator(request, alibabacloud_waf_api_response)
    total = paginator.count
    data = paginator.get_page()
    serializer = AlibabacloudWafApiResponseSerializer(data, many=True)
    logger.info("{} call get_waf_list api".format(request.user.username))
    return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_waf(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_waf_api_response = AlibabacloudWafApiResponse.objects.all().order_by("project_id")

        if project_name:
            alibabacloud_waf_api_response = alibabacloud_waf_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_waf_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudWafApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudWafApiResponseSerializer(data, many=True)
    logger.info("{} call search_waf api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_slb_list(request):
    res = asyncio.run(get_slb_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_slb_list(request):
    alibabacloud_slb_api_response = AlibabacloudSLBApiResponse.objects.all().order_by("project_id")
    paginator = CustomPaginator(request, alibabacloud_slb_api_response)
    total = paginator.count
    data = paginator.get_page()
    serializer = AlibabacloudSlbApiResponseSerializer(data, many=True)
    logger.info("{} call get_slb_list api".format(request.user.username))
    return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_slb(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_slb_api_response = AlibabacloudSLBApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_slb_api_response = alibabacloud_slb_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_slb_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudSLBApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudSlbApiResponseSerializer(data, many=True)
    logger.info("{} call search_slb api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def init_alb_list(request):
    res = asyncio.run(get_alb_api_response())
    return APIResponse(code=0, msg='request successfully', data=res)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_alb_list(request):
    alibabacloud_alb_api_response = AlibabacloudALBApiResponse.objects.all().order_by("project_id")
    paginator = CustomPaginator(request, alibabacloud_alb_api_response)
    total = paginator.count
    data = paginator.get_page()
    serializer = AlibabacloudAlbApiResponseSerializer(data, many=True)
    logger.info("{} call get_alb_list api".format(request.user.username))
    return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_alb(request):
    try:
        project_name = request.GET.get('project_name', None)
        alibabacloud_alb_api_response = AlibabacloudALBApiResponse.objects.all().order_by("project_id")
        if project_name:
            alibabacloud_alb_api_response = alibabacloud_alb_api_response.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, alibabacloud_alb_api_response)
        total = paginator.count
        data = paginator.get_page()
    except AlibabacloudSLBApiResponse.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = AlibabacloudAlbApiResponseSerializer(data, many=True)
    logger.info("{} call search_alb api with conditions project_name: {}".format(request.user.username, project_name))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)

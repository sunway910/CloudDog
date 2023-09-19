import json

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_waf_openapi20211001.client import Client as WAFApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_waf_openapi20211001 import models as waf_openapi_20211001_models
from alibabacloud_ecs20140526.client import Client as EcsApiClient
from handler import APIResponse
from config import settings
from asgiref.sync import sync_to_async

import logging
import json
from alibabacloud_tea_util.client import Client as UtilClient

from config.settings import ENDPOINT

wafInfo = {
    'Details': {
        'AclRuleMaxIpCount': 100,
        'AntiScan': False,
        'AntiScanTemplateMaxCount': 20,
        'BackendMaxCount': 20,
        'BaseWafGroup': True,
        'BaseWafGroupRuleInTemplateMaxCount': 100,
        'BaseWafGroupRuleTemplateMaxCount': 3,
        'Bot': False,
        'BotApp': False,
        'BotTemplateMaxCount': 50,
        'BotWeb': False,
        'CnameResourceMaxCount': 3,
        'CustomResponse': False,
        'CustomResponseRuleInTemplateMaxCount': 100,
        'CustomResponseTemplateMaxCount': 20,
        'CustomRule': False,
        'CustomRuleAction': 'js,block,monitor',
        'CustomRuleCondition': 'URL,URLPath,IP,Referer,User-Agent,Params,Cookie,Content-Type,Content-Length,X-Forwarded-For,Post-Body,Http-Method,Extension,Filename,Server-Port,Host,Header,Cookie-Exact,Query-Arg,Post-Arg',
        'CustomRuleInTemplateMaxCount': 100,
        'CustomRuleRatelimitor': 'remote_addr,header,queryarg,cookie,cookie.acw_tc',
        'CustomRuleTemplateMaxCount': 20,
        'DefenseGroupMaxCount': 10,
        'DefenseObjectInGroupMaxCount': 50,
        'DefenseObjectInTemplateMaxCount': 10,
        'DefenseObjectMaxCount': 300,
        'Dlp': False,
        'DlpRuleInTemplateMaxCount': 50,
        'DlpTemplateMaxCount': 20,
        'ExclusiveIp': False,
        'Gslb': False,
        'HttpPorts': '80,8080',
        'HttpsPorts': '443,8443',
        'IpBlacklist': False,
        'IpBlacklistIpInRuleMaxCount': 200,
        'IpBlacklistRuleInTemplateMaxCount': 1,
        'IpBlacklistTemplateMaxCount': 20,
        'Ipv6': False,
        'LogService': False,
        'MajorProtection': False,
        'MajorProtectionTemplateMaxCount': 20,
        'Tamperproof': False,
        'TamperproofRuleInTemplateMaxCount': 50,
        'TamperproofTemplateMaxCount': 20,
        'VastIpBlacklistInFileMaxCount': 2000,
        'VastIpBlacklistInOperationMaxCount': 500,
        'VastIpBlacklistMaxCount': 50000,
        'Whitelist': True,
        'WhitelistLogical': 'not-contain,contain,none,ne,eq,len-lt,len-eq,len-gt,lt,gt,not-match,match-one,all-not-match,contain-one,all-not-contain,prefix-match,empty,suffix-match,exists,inl,range-ip,not-range-ip',
        'WhitelistRuleCondition': 'IP,URL,Referer,User-Agent,Params,Query-Arg,Cookie,Content-Type,X-Forwarded-For,Content-Length,Post-Body,Http-Method,Header,URLPath,Host',
        'WhitelistRuleInTemplateMaxCount': 100,
        'WhitelistTemplateMaxCount': 20
    },
    'Edition': 'Basic',
    'EndTime': 1720022400000,
    'InstanceId': 'waf_v3prepay_public_inal-sg-dza3aesaa01',
    'PayType': 'PREPAY',
    'RegionId': 'ap-southeast-1',
    'RequestId': 'FF358066-C89E-38DA-9997-B3AA69A6290C',
    'StartTime': 1688369814000,
    'Status': 1
}


def test_json_exist():
    global a, obj
    a = UtilClient.to_jsonstring(wafInfo)
    obj = json.loads(a)
    if 'InDebt' in obj:
        print("键 InDebt 存在")
    else:
        print("键 InDebt 不存在")
    print(obj['InDebt'] if 'InDebt' in obj else None)


def test_endpoint():
    endpoint = ENDPOINT['ECS_ENDPOINT']['mainland']
    print("endpoint=", endpoint)


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
    # Endpoint Ref: https://api.aliyun.com/product/Ecs
    config.endpoint = endpoint
    return config


def get_waf_api_response() -> None:
    runtime = util_models.RuntimeOptions()
    client = WAFApiClient(set_client_config('',
                                            '',
                                            ENDPOINT['WAF_ENDPOINT']['oversea']))
    describe_instance_info_request = waf_openapi_20211001_models.DescribeInstanceRequest()
    try:
        # 复制代码运行请自行打印 API 的返回值
        res = client.describe_instance_with_options(describe_instance_info_request, runtime)
        DescribeWAFAttributeResponseToStr = UtilClient.to_jsonstring(res)
        DescribeWAFAttributeResponseJsonObject = json.loads(DescribeWAFAttributeResponseToStr)
        wafInfo = DescribeWAFAttributeResponseJsonObject['body']
        print("WAF INFO==", wafInfo)

    except Exception as error:
        UtilClient.assert_as_string(error)


def get_ecr_api_response() -> None:
    runtime = util_models.RuntimeOptions()
    client = EcsApiClient(set_client_config('',
                                            '',
                                            ENDPOINT['ECS_ENDPOINT']['mainland']))

    describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id='cn-hongkong')
    try:
        # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstances
        DescribeInstanceResponse = client.describe_instances_with_options(describe_instances_request, runtime)

        DescribeInstanceResponseToStr = UtilClient.to_jsonstring(DescribeInstanceResponse)
        DescribeInstanceResponseJsonObject = json.loads(DescribeInstanceResponseToStr)
        instance_list = DescribeInstanceResponseJsonObject['body']['Instances']['Instance']
        for instance in instance_list:
            describe_instance_auto_renew_attribute_request = ecs_20140526_models.DescribeInstanceAutoRenewAttributeRequest(region_id='cn-hongkong', instance_id=instance['InstanceId'])
            # API Ref: https://next.api.aliyun.com/document/Ecs/2014-05-26/DescribeInstanceAutoRenewAttribute
            DescribeInstanceAutoRenewAttributeResponse = client.describe_instance_auto_renew_attribute_with_options(describe_instance_auto_renew_attribute_request, runtime)
            DescribeInstanceAutoRenewAttributeResponseToStr = UtilClient.to_jsonstring(DescribeInstanceAutoRenewAttributeResponse)
            DescribeInstanceAutoRenewAttributeResponseJsonObject = json.loads(DescribeInstanceAutoRenewAttributeResponseToStr)
            InstanceAutoRenewInfo = DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
            # request 2 API and get two request id, so the new request id is formed by combining two request id
            requestId = DescribeInstanceResponseJsonObject['body']['RequestId'] + " " + DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['RequestId']
            print("ECS INFO==", InstanceAutoRenewInfo)

    except Exception as error:
        UtilClient.assert_as_string(error)


# get_ecr_api_response()
# test_endpoint()
# test_json_exist()

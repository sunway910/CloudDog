# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import asyncio
import json

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


# https://next.api.alibabacloud.com/api/Ecs/2014-05-26/DescribeInstanceStatus?tab=DOC&lang=PYTHON
class Sample:
    def __init__(self):
        pass

    @staticmethod
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

    @staticmethod
    async def main_async() -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('LTAI5t74a9Xot9saANDiHNNY', 'iA5fEqkzFVPxFIO7TePVaNSjty3OG1')
        runtime = util_models.RuntimeOptions()
        describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(region_id='cn-hongkong')
        instance_ids = []
        try:
            DescribeInstanceResponse = await client.describe_instances_with_options_async(describe_instances_request, runtime)
            DescribeInstanceResponseToStr = UtilClient.to_jsonstring(DescribeInstanceResponse)
            # ConsoleClient.log(DescribeInstanceResponseToStr)
            DescribeInstanceResponseJsonObject = json.loads(DescribeInstanceResponseToStr)
            print('Response code: ', DescribeInstanceResponseJsonObject['statusCode'])
            instance_list = DescribeInstanceResponseJsonObject['body']['Instances']['Instance']
            for instance in instance_list:
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
                DescribeInstanceAutoRenewAttributeResponse = await client.describe_instance_auto_renew_attribute_with_options_async(describe_instance_auto_renew_attribute_request, runtime)
                DescribeInstanceAutoRenewAttributeResponseToStr = UtilClient.to_jsonstring(DescribeInstanceAutoRenewAttributeResponse)
                # ConsoleClient.log(DescribeInstanceAutoRenewAttributeResponseToStr)
                DescribeInstanceAutoRenewAttributeResponseJsonObject = json.loads(DescribeInstanceAutoRenewAttributeResponseToStr)
                instance_info = DescribeInstanceAutoRenewAttributeResponseJsonObject['body']['InstanceRenewAttributes']['InstanceRenewAttribute'][0]
                print('是否已开启自动续费功能: ', instance_info['AutoRenewEnabled'])
                print('实例的自动续费状态: ', instance_info['RenewalStatus'])
                print('自动续费时长的单位: ', instance_info['PeriodUnit'])
                print('自动续费时长: ', instance_info['Duration'])
                print('-----------------------------------------------------------------------------------------------------------------------------')
                print('-----------------------------------------------------------------------------------------------------------------------------')

        except Exception as error:
            UtilClient.assert_as_string(error)


# Python 字典类型转换为 JSON 对象
# json.dumps()

# 将 JSON 对象转换为 Python 字典
# json.loads()

if __name__ == '__main__':
    asyncio.run(Sample().main_async())

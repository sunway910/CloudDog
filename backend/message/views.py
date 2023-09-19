import logging

from django.core.mail import send_mail
from django.template.loader import get_template

from config import settings

logger = logging.getLogger('cpm')


# 首先先定义一个sendMessage的函数，方便后期调用
def send_message(event_info) -> bool:
    try:
        # 自定义邮件内容模板将在下面 Email.html 文件中写！
        template = get_template('template.html')
        # [project_name type instance_id account] in email template
        html_content = template.render(
            {'project_name': event_info['project_name'],
             'type': event_info['type'],
             'instance_id': event_info['instance_id'],
             }
        )

        from_send = settings.EMAIL_HOST_USER
        # sbj:就是人家收到你的邮件时，显示的标题，，
        sbj = 'Sunway Service'
        send_mail(subject=sbj, message=None, html_message=html_content, from_email=from_send, recipient_list=[settings.RECIPIENT_ADDRESS])
        return True
    except Exception as error:
        logger.error("send message failed: {}".format(error))
        return False

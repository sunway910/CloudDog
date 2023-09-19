import logging

from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from config import settings
from handler import APIResponse
from message.models import Event
from message.serializers import EventSerializer
from paginator import CustomPaginator

logger = logging.getLogger('cpm')


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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_list(request):
    if request.method == 'GET':
        status = request.GET.get('status', "unread")
        event_list = Event.objects.filter(status=status).all()
        paginator = CustomPaginator(request, event_list)
        data = paginator.get_page()
        total = paginator.count
        serializer = EventSerializer(data, many=True)
        logger.info("{} call message list api".format(request.user.username))
        return APIResponse(code=0, msg='success', total=total, data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search(request):
    try:
        project_name = request.GET.get('project_name', None)
        status = request.GET.get('status', "unread")
        event_list = Event.objects.filter(status=status).all()
        if project_name:
            event_list = event_list.filter(project_name__icontains=project_name)
        paginator = CustomPaginator(request, event_list)
        data = paginator.get_page()
        total = paginator.count
    except Event.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    serializer = EventSerializer(data, many=True)
    logger.info("{} call message search api with conditions project_name: {}, message status: {}"
                .format(request.user.username, project_name, status))
    return APIResponse(code=0, msg='request successfully', total=total, data=serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        project = Event.objects.filter(id=request.data['id']).update(status=request.data['status'])
        logger.info("{} call message update api, request data: {}".format(request.user.username, request.data))
        return APIResponse(code=0, msg='operate message successfully', data=project)
    except Event.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')

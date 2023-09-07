from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from handler import APIResponse
from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permissions import IsAdminUserOrReadOnly
import logging
import time

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_api(request):
    if request.method == 'GET':
        projects = Project.objects.values('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time').order_by('-id')
        serializer = ProjectSerializer(projects, many=True, fields=('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time'))
        return APIResponse(code=0, msg='success', data=serializer.data)


# select * from project where project.project_name = project_name and cloud_platform = cloud_platform
# projectList = Project.objects.all().extra(tables=['project'], where=['project.project_name = project_name', 'cloud_platform = cloud_platform'])
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def detail(request):
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
    serializer = ProjectSerializer(queryset, many=True, fields=('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time'))
    return APIResponse(code=0, msg='request successfully', data=serializer.data)


@api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUserOrReadOnly])
def create(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("{}, create a project {}".format(time.strftime('%X'), request.data))
        return APIResponse(code=0, msg='create successfully', data=serializer.data)
    else:
        print(serializer.errors)
    return APIResponse(code=1, msg='create failed')


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUserOrReadOnly])
def update(request):
    try:
        project_id = request.data['id']
        project_name = request.data['project_name']
        account = request.data['account']
        accountList = [account]
        # Project.objects.filter(id=project_id).update(project_name=project_name, account=accountList)
        #
        project = Project.objects.filter(id=project_id)
        serializer = ProjectSerializer(project, data=request.data)
        print("project_id==", project_id)
        print("project_name==", project_name)
        print("account==", account)
        if serializer.is_valid():
            Project.objects.filter(id=project_id).update(project_name=project_name, account=account)
            logger.info("{}, update a project {}".format(time.strftime('%X'), request.data))
        return APIResponse(code=0, msg='update project successfully', data=request.data)
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')


@api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUserOrReadOnly])
def delete(request):
    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Project.objects.filter(id__in=ids_arr).delete()
        logger.info("{}, delete projects {}".format(time.strftime('%X'), request.data))
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')

    return APIResponse(code=0, msg='delete successfully')

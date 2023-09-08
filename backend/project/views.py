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
def get_list(request):
    if request.method == 'GET':
        projects = Project.objects.values('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time').order_by('-id')
        serializer = ProjectSerializer(projects, many=True, fields=('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time'))
        return APIResponse(code=0, msg='success', data=serializer.data)


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
    serializer = ProjectSerializer(queryset, many=True, fields=('id', 'cloud_platform', 'account', 'project_name', 'status', 'create_time'))
    return APIResponse(code=0, msg='request successfully', data=serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUserOrReadOnly])
def create_or_update(request):
    try:
        if request.data['id'] is not None:
            Project.objects.filter(id=request.data['id']).update(
                account=request.data['account'],
                project_name=request.data['project_name'],
                status=request.data['status'],
                create_time=request.data['create_time']
            )
        else:
            Project.objects.create(
                account=request.data['account'],
                cloud_platform=request.data['cloud_platform'],
                project_name=request.data['project_name'],
                status=request.data['status'],
                create_time=request.data['create_time']
            )
        return APIResponse(code=0, msg='update project successfully', data=request.data)
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUserOrReadOnly])
def delete(request):
    try:
        project_id = request.GET.get('id', None)
        logger.info("{}, delete projects {}".format(time.strftime('%X'), Project.objects.get(id=project_id)))
        Project.objects.filter(id=project_id).delete()
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')
    return APIResponse(code=0, msg='delete successfully')

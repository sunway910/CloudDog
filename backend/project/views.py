from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAdminUserOrReadOnly
from handler import APIResponse
from project.models import Project
from project.serializers import ProjectSerializer
import logging
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import time

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_api(request):
    if request.method == 'GET':
        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        return APIResponse(code=0, msg='success', data=serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def detail(request):
    try:
        pk = request.GET.get('id', -1)
        thing = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist err')
    if request.method == 'GET':
        serializer = ProjectSerializer(thing)
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
# @permission_classes([IsAuthenticated, IsAdminUserOrReadOnly])
def update(request):
    try:
        pk = request.GET.get('id', -1)
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return APIResponse(code=1, msg='no exist error')
    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("{}, update a project {}".format(time.strftime('%X'), request.data))
        return APIResponse(code=0, msg='update successfully', data=serializer.data)

    return APIResponse(code=1, msg='update failed')


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

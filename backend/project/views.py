import logging

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.decorators import api_view

from rest_framework import viewsets

from .filters import ArticleFilter
# from rest_framework.permissions import IsAdminUser
from .models import Article, Avatar, Category, Tag
from .permissions import IsAdminUserOrReadOnly
from .serializers import (ArticleDetailSerializer, ArticleSerializer, AvatarSerializer, CategoryDetailSerializer,
                          CategorySerializer, TagSerializer)

@api_view(['GET'])
def get_project_list(request):
    if request.method == 'GET':
        project_list = Project.objects.all()

        project_name = request.query_params.get('project_name', None)
        if project_name is not None:
            project_list = project_list.filter(title__icontains=project_name)

        projects_serializer = ProjectSerializer(project_list, many=True)
        return JsonResponse(projects_serializer.data, safe=False)
        # 'safe=False' for objects serialization


@api_view(['PUT', 'DELETE'])
def write_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        logging.info("project: ", project)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(Project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Project.delete(pk)
        return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

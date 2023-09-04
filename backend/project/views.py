import logging

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.decorators import api_view
import logging
import os
import uuid
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .permissions import IsAdminUserOrReadOnly

logger = logging.getLogger(__name__)

from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_name'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]

        return super().get_permissions()

    @action(detail=False)
    def sorted(self, request):
        queryset = Project.objects.all().order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=['get'])
    def get_project_list(self, request):
        queryset = Project.objects.all()
        project_name = request.query_params.get('project_name', None)
        if project_name is not None:
            queryset = queryset.filter(title__icontains=project_name)

        projects_serializer = ProjectSerializer(queryset, many=True)
        return JsonResponse(projects_serializer.data, safe=False)

    @action(detail=True, methods=['put', 'delete'])
    def edit_project(self, request):
        try:
            project_detail = Project.objects.get(id=request.query_params.get('id', None))
            logging.info("project_detail: ", project_detail)
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
            if request.query_params.get('id') is not None:
                Project.delete(request.query_params.get('id', None))
                return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({'message': 'The Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

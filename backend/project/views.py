from rest_framework import viewsets

# from rest_framework.permissions import IsAdminUser
from models import Project
from permissions import IsAdminUserOrReadOnly


# 视图集类把列表、详情等逻辑都集成到一起，并且提供了默认的增删改查的实现
class EcsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

"""backend URL Configuration

The `urlpatterns` list routes URLs to pages. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function pages
    1. Add an import:  from my_app import pages
    2. Add a URL to urlpatterns:  path('', pages.home, name='home')
Class-based pages
    1. Add an import:  from other_app.pages import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from user.views import UserViewSet
from project.views import get_project_list
router = DefaultRouter()
router.register(r'user', UserViewSet)
# router.register(r'project/list', get_project_list)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    # 使用form表单或JSON将有效的username和password字段POST到api/token/时会获取token,其他api则需要在http header中设置token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/project/list', include('project.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

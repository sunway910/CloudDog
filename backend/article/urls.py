from django.urls import path
import views

app_name = 'article'

urlpatterns = [
    path('', views.ArticleViewSet.as_view(), name='list'),
    path('<int:pk>', views.ArticleViewSet.as_view(), name='detail'),
]

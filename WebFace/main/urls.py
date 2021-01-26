from django.urls import path,re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<str:user_name>/', views.index),
    path('', views.index),
    path('find_user', views.find_user),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

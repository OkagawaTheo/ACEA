from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from pessoas.views import TAlunoViewSet


router = DefaultRouter();
router.register(r'alunos',TAlunoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls))
]

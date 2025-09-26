from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from pessoas.views import *
from educacao.views import *

router = DefaultRouter();
router.register(r'alunos',TAlunoViewSet)
router.register(r'professores',TProfessorViewSet)
router.register(r'presidentes',TPresidenteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls))
]

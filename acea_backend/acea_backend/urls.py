from django.contrib import admin
from django.urls import path,include
from rest_framework import routers

from pessoa.viewsets import AlunoViewSet, ProfessorViewSet, PresidenteViewSet, AdministradorViewSet, DoadorViewSet
from curso.viewsets import CursoViewSet, AtividadeEsportivaViewSet
from documentacao.viewsets import PagamentoViewSet, DoacaoViewSet

from pessoa.auth_views import LoginAPIView 


router = routers.DefaultRouter()

router.register(r'alunos', AlunoViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'presidentes', PresidenteViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'doadores', DoadorViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'atividades_esportivas', AtividadeEsportivaViewSet)
router.register(r'pagamentos', PagamentoViewSet)
router.register(r'doacoes', DoacaoViewSet)


urlpatterns = [
    path('pessoa/',include("pessoa.urls")),
    path('api/login/', LoginAPIView.as_view(), name='api_login'), 
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    path('admin/', admin.site.urls),
]
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Aluno, Professor, Presidente

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # 2. Gera ou pega o token
        token, created = Token.objects.get_or_create(user=user)
        
        tipo_usuario = 'desconhecido'
        id_especifico = None

        if hasattr(user, 'aluno'):
            tipo_usuario = 'aluno'
            id_especifico = user.aluno.id_aluno
        elif hasattr(user, 'professor'):
            tipo_usuario = 'professor'
            id_especifico = user.professor.id_professor
        elif user.is_superuser: # Presidente/Admin
            tipo_usuario = 'admin'

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'tipo_usuario': tipo_usuario,
            'id_especifico': id_especifico,
            'email': user.email
        })
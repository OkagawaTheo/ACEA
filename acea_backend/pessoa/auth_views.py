from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .auth_serializer import LoginSerializer

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
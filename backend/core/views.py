from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.response import Response
from core.serializers import UserSerializer, ClientSerializer, HabitacionSerializer, StaffSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.settings import api_settings
from rest_framework.decorators import permission_classes, authentication_classes
from django.template import loader
from .models import Administrador, User, Cliente, Habitacion, Recepcionista
from rest_framework.views import APIView

# Create your views here.

class CreateTokenView(ObtainAuthToken):
    """Create auth token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'error': False,
                'token': token.key,
                'email': user.email,
                'name': user.nombre,
            },status=status.HTTP_302_FOUND)
        else:
            return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserAdminView(generics.CreateAPIView):
    """Create user on the system"""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class clientView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            user_client = Cliente.objects.get(id_user=user.id)
            serializer = ClientSerializer(user_client, many=False, context={'request': request})    
        except Cliente.DoesNotExist:
            return Response({"error": True}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Info_user": serializer.data} , status=status.HTTP_200_OK)

class adminView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            user_admin = Administrador.objects.get(id_user=user.id)
            serializer = StaffSerializer(user_admin, many=False, context={'request': request})    
        except Administrador.DoesNotExist:
            return Response({"error": True}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Info_user": serializer.data} , status=status.HTTP_200_OK)
    def post(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            user_client = Administrador.objects.get(id_user=user.id)
        except Administrador.DoesNotExist:
            return Response({"error": True}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = HabitacionSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            habitacion = Habitacion(**validated_data)
            habitacion.save()
            serializer_response = HabitacionSerializer(habitacion)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
    
class recepcionistaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = Token.objects.get(key=request.auth.key).user
            user_recep = Recepcionista.objects.get(id_user=user.id)
            serializer = StaffSerializer(user_recep, many=False, context={'request': request})    
        except Recepcionista.DoesNotExist:
            return Response({"error": True}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Info_user": serializer.data} , status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_token(request):
    user = User.objects.get(id=request.data['id_user'])
    token = Token.objects.get(user=user)
    return Response({"email": user.email, "token": token.key})
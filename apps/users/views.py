from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .services import AuthService

User = get_user_model()


# Maybe we can use CreateAPIView here insted of api_view
# https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Регистрация нового пользователя
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = AuthService.create_user(serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Аутентификация пользователя
    """
    # try to use django.contrib.auth.authenticate()
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = AuthService.authenticate_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserRegistrationSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Выход пользователя из системы
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Обновление токена доступа
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        return Response(
            {
                "access": str(token.access_token),
            }
        )
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

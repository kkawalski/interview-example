from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from apps.users import serializers as user_serializers
from apps.users import services as user_services

User = get_user_model()


# Maybe we can use CreateAPIView here insted of api_view
# https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Регистрация нового пользователя
    """
    serializer = user_serializers.UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = user_services.AuthService.create_user(serializer.validated_data)
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Аутентификация пользователя
    """
    # try to use django.contrib.auth.authenticate()
    serializer = user_serializers.UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = user_services.AuthService.authenticate_user(
        email=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "user": user_serializers.UserRegistrationSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )

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

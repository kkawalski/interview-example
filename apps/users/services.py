from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

User = get_user_model()

class AuthService:
    @staticmethod
    @transaction.atomic
    def create_user(user_data):
        """
        Создает нового пользователя с валидацией данных
        """
        email = user_data.get('email')
        password = user_data.get('password')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Пользователь с таким email уже существует'))
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})
        
        user = User.objects.create_user(
            email=email,
            password=password,
            **{k: v for k, v in user_data.items() if k not in ['email', 'password']}
        )
        
        return user

    @staticmethod
    def authenticate_user(email, password):
        """
        Аутентифицирует пользователя по email и паролю
        """
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise ValidationError(_('Неверный пароль'))
            return user
        except User.DoesNotExist:
            raise ValidationError(_('Пользователь не найден'))

    @staticmethod
    def change_password(user, old_password, new_password):
        """
        Изменяет пароль пользователя
        """
        if not user.check_password(old_password):
            raise ValidationError(_('Неверный текущий пароль'))
        
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise ValidationError({'new_password': e.messages})
        
        user.set_password(new_password)
        user.save()
        return user 
import uuid

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from online_shop.settings import EMAIL_HOST_USER
from users.models import RecoveryCode, User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "username",
            "position",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def send_email(self) -> None:
        send_mail(
            "Регистрация",
            "Вы успешно зарегистрировались!",
            EMAIL_HOST_USER,
            [self.instance.email],
        )


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def validate(self, data: dict) -> dict:
        user = User.objects.filter(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid credentials")
        return data

    def get_token(self, validated_data: dict) -> str:
        user = User.objects.filter(email=validated_data["email"]).first()
        token = Token.objects.get_or_create(user=user)[0]
        return token.key


class RecoveryCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def send_code(self, data: dict) -> None:
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("Invalid email")
        code = RecoveryCode.objects.filter(user=user).order_by("-created_at").first()
        if not code:
            code = RecoveryCode.objects.create(user=user, code=uuid.uuid4())

        send_mail(
            "Восстановление пароля",
            f"Ваш код восстановления: {code.code}",
            EMAIL_HOST_USER,
            [user.email],
        )


class RecoverPasswordSerializer(serializers.Serializer):
    code = serializers.UUIDField(write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)

    def create(self, validated_data: dict) -> User:
        code = RecoveryCode.objects.filter(code=validated_data["code"]).first()
        if not code:
            raise serializers.ValidationError("Invalid code")
        user = User.objects.filter(id=code.user.id).first()
        user.set_password(validated_data["password"])
        user.save()
        RecoveryCode.objects.filter(user=user).delete()
        return user

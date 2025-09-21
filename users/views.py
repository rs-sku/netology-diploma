from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    RecoverPasswordSerializer,
    RecoveryCodeSerializer,
)


class CreateUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.send_email()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.get_token(serializer.validated_data)
            return Response({"token": token})
        return Response(serializer.errors, status=400)


class RecoveryCodeView(APIView):
    def post(self, request):
        serializer = RecoveryCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_code(serializer.validated_data)
            return Response({"message": "Code sent"}, status=201)
        return Response(serializer.errors, status=400)


class RecoverPasswordView(APIView):
    def patch(self, request: Request) -> Response:
        serializer = RecoverPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed"}, status=201)
        return Response(serializer.errors, status=400)

from django.urls import path

from users.views import (
    CreateUserView,
    LoginUserView,
    RecoverPasswordView,
    RecoveryCodeView,
)

urlpatterns = [
    path("users", CreateUserView.as_view(), name="create_user"),
    path("users/login", LoginUserView.as_view(), name="login_user"),
    path("users/recovery-code", RecoveryCodeView.as_view(), name="recovery_code"),
    path(
        "users/recover-password", RecoverPasswordView.as_view(), name="recover_password"
    ),
]

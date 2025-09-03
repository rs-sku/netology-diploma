from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False, unique=True)
    position = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Список пользователей"
        ordering = ("last_name",)

class RecoveryCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.code}"
    
    class Meta:
        verbose_name = "Код восстановления"
        verbose_name_plural = "Список кодов восстановления"
        ordering = ("created_at",)




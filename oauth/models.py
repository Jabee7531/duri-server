from django.db import models
from user.models import User

# Create your models here.


class Oauth(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField("제공자", max_length=12)
    social_id = models.CharField("소셜 아이디", max_length=255)
    disabled = models.BooleanField(default=False)
    created_at = models.DateField("생성날짜", auto_now_add=True)
    updated_at = models.DateField("최근 접속날짜", auto_now=True)

    class Meta:
        db_table = "oauth"
        verbose_name = "유저 테이블"

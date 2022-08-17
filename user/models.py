from time import time
from django.db import models

from lib.jwt import generate_token

# Create your models here.


class User(models.Model):
    name = models.CharField("이름", max_length=255)
    nickname = models.CharField("닉네임", max_length=255, unique=True)
    email = models.CharField("이메일", unique=True, max_length=255)
    thumbnail = models.CharField("썸네일", max_length=255, null=True)
    is_certified = models.BooleanField(default=False)
    created_at = models.DateField("생성날짜", auto_now_add=True)
    updated_at = models.DateField("최근 접속날짜", auto_now=True)

    def generate_token(self):
        iat = time()
        exp = iat + 60 * 60 * 24

        payload = {
            "sub": "user_jwt",
            "user_id": self.id,
            "iat": iat,
            "exp": exp,
        }

        return generate_token(payload)

    class Meta:
        db_table = "user"
        verbose_name = "유저 테이블"

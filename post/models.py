from django.db import models
from user.models import User

# Create your models here.

# have comment
class Post(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField("작성자", max_length=255)
    title = models.CharField("제목", max_length=255)
    content = models.TextField("내용")
    thumbnail = models.CharField("섬네일", max_length=255, null=True)
    likes = models.IntegerField("좋아요", default=0)
    views = models.IntegerField("조회수", default=0)
    deleted = models.BooleanField("삭제", default=False)
    created_at = models.DateField("게시글 생성날짜", auto_now_add=True)
    updated_at = models.DateField("게시글 수정날짜", auto_now=True)

    class Meta:
        db_table = "post"
        verbose_name = "게시글 테이블"

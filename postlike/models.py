from django.db import models
from post.models import Post
from user.models import User

# Create your models here.


class PostLike(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateField("좋아요 생성날짜", auto_now_add=True)
    updated_at = models.DateField("좋아요 수정날짜", auto_now=True)

    class Meta:
        db_table = "postlike"
        verbose_name = "게시글 좋아요 테이블"

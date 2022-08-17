from django.db import models
from post.models import Post
from user.models import User

# Create your models here.


class Comment(models.Model):
    fk_user_id = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    fk_post_id = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    commenter = models.CharField("작성자 닉네임", max_length=255)
    content = models.TextField("내용")
    has_replies = models.BooleanField("대댓글", default=False)
    reply_to = models.PositiveBigIntegerField("대댓글id", null=True, default=None)
    level = models.IntegerField("레벨", default=0)
    likes = models.IntegerField("좋아요", default=0)
    deleted = models.BooleanField("삭제", default=False)
    created_at = models.DateField("댓글 생성날짜", auto_now_add=True)
    updated_at = models.DateField("댓글 수정날짜", auto_now=True)

    # def clean(self):
    #     from django.forms import ValidationError
    #     if self.commenter == "":
    #         raise ValidationError("Empty code not allowed")

    class Meta:
        db_table = "comment"
        verbose_name = "댓글 테이블"

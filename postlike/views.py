from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from postlike.models import PostLike
from user.decorators import is_login
from user.models import User
from post.models import Post

# Create your views here.


@method_decorator(is_login, name="post")
class CreatePostLike(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        post_id = request.data.get("post_id")

        post = Post.objects.filter(id=post_id).first()
        if not post:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글이 없음",
                    "result": data,
                },
                status=400,
            )

        postlike = PostLike.objects.filter(
            fk_user_id=user_id,
            fk_post_id=post_id,
        ).first()

        if postlike:
            postlike.delete()

            post.likes -= 1
            post.save()

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "좋아요 취소",
                    "result": data,
                },
                status=200,
            )

        user = User.objects.filter(id=user_id).first()
        if not user:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "로그인이 되어있지 않음",
                    "result": data,
                },
                status=400,
            )

        postlike = PostLike.objects.create(
            fk_user_id=user,
            fk_post_id=post,
        )

        post.likes += 1
        post.save()

        data = {}

        return Response(
            data={
                "code": 200000,
                "message": "좋아요!",
                "result": data,
            },
            status=200,
        )


# @method_decorator(is_login, name="delete")
class DeletePostLike(APIView):
    def delete(self, request):
        return Response("delete like")

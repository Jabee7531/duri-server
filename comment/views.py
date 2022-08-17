from rest_framework.views import APIView
from rest_framework.response import Response
from user.decorators import is_login
from .serializers import CommentSerializer
from .models import Comment
from post.models import Post
from user.models import User
from django.utils.decorators import method_decorator


# Create your views here.


@method_decorator(is_login, name="post")
class CreateComment(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            post_id = request.data.get("post_id")
            content = request.data.get("content")
            level = request.data.get("level", 0)
            reply_to = request.data.get("reply_to")

            user = User.objects.filter(id=user_id).first()
            if not user:
                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "유저가 없음",
                        "result": data,
                    },
                    status=400,
                )

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

            if reply_to:
                comment = Comment.objects.filter(id=reply_to).first()

                if not comment.has_replies:
                    comment.has_replies = 1
                    comment.save()

            comment = Comment.objects.create(
                fk_user_id=user,
                fk_post_id=post,
                commenter=user.nickname,
                content=content,
                level=level,
                reply_to=reply_to,
            )

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "댓글 생성 성공",
                    "result": data,
                },
                status=200,
            )

        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "댓글 생성 실패",
                    "result": data,
                },
                status=400,
            )


class ReadComments(APIView):
    def get(self, request):
        try:
            post_id = request.GET.get("post_id")
            level = request.GET.get("level")
            reply_to = request.GET.get("reply_to")

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

            comment = Comment.objects.filter(
                fk_post_id=post_id,
                level=level,
                reply_to=reply_to,
                deleted=0,
            )

            serializer = CommentSerializer(comment, many=True)

            data = {
                "comments": serializer.data,
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "댓글 조회 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "댓글 조회 실패",
                    "result": data,
                },
                status=400,
            )


@method_decorator(is_login, name="patch")
class UpdateComment(APIView):
    def patch(self, request):
        try:
            user_id = request.data.get("user_id")
            comment_id = request.data.get("comment_id")
            content = request.data.get("content")

            commnet = Comment.objects.filter(
                id=comment_id,
                fk_user_id=user_id,
            ).first()
            if not commnet:
                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "댓글을 찾을 수 없음",
                        "result": data,
                    },
                    status=400,
                )

            commnet.content = content
            commnet.save()

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "댓글 수정 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "댓글 수정 실패",
                    "result": data,
                },
                status=400,
            )


@method_decorator(is_login, name="delete")
class DeleteComment(APIView):
    def delete(self, request):
        try:
            user_id = request.data.get("user_id")
            comment_id = request.data.get("comment_id")

            comment = Comment.objects.filter(
                id=comment_id,
                fk_user_id=user_id,
            ).first()
            if not comment:
                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "댓글을 찾을 수 없음",
                        "result": data,
                    },
                    status=400,
                )

            comment.deleted = 1
            comment.save()

            reply_to = comment.reply_to
            if reply_to:
                if not Comment.objects.filter(reply_to=reply_to, deleted=0).exists():
                    fix = Comment.objects.filter(id=reply_to).first()
                    fix.has_replies = 0
                    fix.save()

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "댓글 삭제 성공",
                    "result": data,
                },
                status=200,
            )

        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "댓글 삭제 실패",
                    "result": data,
                },
                status=400,
            )

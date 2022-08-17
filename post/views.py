from rest_framework.views import APIView
from rest_framework.response import Response
from user.decorators import is_login
from post.serializers import PostSerializer
from user.models import User
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.db.models import Q


# Create your views here.

# TODO: 게시글 정규식 걸기 (ex 제목이 너무 길면 안됨)
@method_decorator(is_login, name="post")
class CreatePost(APIView):
    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            title = request.data.get("title")
            content = request.data.get("content")
            thumbnail = request.data.get("thumbnail_name")
            if thumbnail:
                thumbnail = f"https://duhbhveegwq63.cloudfront.net/post/{thumbnail}"

            user = User.objects.filter(id=user_id).first()
            if not user:
                data = {}

                return Response(
                    data={
                        "code": 401000,
                        "message": "유저 오브젝트가 없음",
                        "result": data,
                    },
                    status=401,
                )

            post = Post.objects.create(
                fk_user_id=user,
                author=user.nickname,
                title=title,
                content=content,
                thumbnail=thumbnail,
            )

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 생성 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 생성 실패",
                    "result": data,
                },
                status=400,
            )


class ReadPost(APIView):
    def get(self, request):
        try:
            post_id = request.GET.get("post_id")

            if not post_id:
                data = {}

                return Response(
                    data={
                        "code": 404000,
                        "message": "쿼리가 없음",
                        "result": data,
                    },
                    status=404,
                )

            post = Post.objects.filter(
                id=post_id,
                deleted=0,
            ).first()

            if not post:
                data = {}

                return Response(
                    data={
                        "code": 404000,
                        "message": "게시글을 찾을 수 없음",
                        "result": data,
                    },
                    status=404,
                )

            serializer = PostSerializer(post)

            data = {
                "post": serializer.data,
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 조회 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 조회 실패",
                    "result": data,
                },
                status=400,
            )


class ReadPosts(APIView):
    def get(self, request):
        try:
            cursor = request.GET.get("cursor", 1)
            post = Post.objects.filter(deleted=0).order_by("-id")

            paginator = Paginator(post, 10)
            posts = paginator.page(cursor)

            data = {
                "page": cursor,
                "has_next": posts.has_next(),
                "posts": posts.object_list.values(),
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 조회 성공",
                    "result": data,
                },
                status=200,
            )
        except EmptyPage:
            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "EmptyPage",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 조회 실패",
                    "result": data,
                },
                status=400,
            )


@method_decorator(is_login, name="patch")
class UpdatePost(APIView):
    def patch(self, request):
        try:
            user_id = request.data.get("user_id")
            post_id = request.data.get("post_id")
            title = request.data.get("title")
            content = request.data.get("content")
            thumbnail = request.data.get("thumbnail_name")
            if thumbnail:
                thumbnail = f"https://duhbhveegwq63.cloudfront.net/post/{thumbnail}"

            post = Post.objects.filter(
                fk_user_id=user_id,
                id=post_id,
            ).first()

            if not post:
                data = {}

                return Response(
                    data={
                        "code": 404000,
                        "message": "게시글을 찾을 수 없음",
                        "result": data,
                    },
                    status=404,
                )

            post.title = title
            post.content = content
            post.thumbnail = thumbnail
            post.save()

            serializer = PostSerializer(post)

            data = {
                "post": serializer.data,
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 수정 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 수정 실패",
                    "result": data,
                },
                status=400,
            )


@method_decorator(is_login, name="delete")
class DeletePost(APIView):
    def delete(self, request):
        try:
            user_id = request.data.get("user_id")
            post_id = request.data.get("post_id")

            post = Post.objects.get(
                fk_user_id=user_id,
                id=post_id,
            )

            if not post:
                data = {}

                return Response(
                    data={
                        "code": 404000,
                        "message": "게시글을 찾을 수 없음",
                        "result": data,
                    },
                    status=404,
                )

            # post.delete()
            post.deleted = 1
            post.save()

            data = {}

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 삭제 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 삭제 실패",
                    "result": data,
                },
                status=400,
            )


class SearchPosts(APIView):
    def get(self, request):
        try:
            cursor = request.GET.get("cursor", 1)
            search = request.GET.get("search", "두리")

            q = Q()

            if search:
                q |= Q(title__icontains=search)
                q |= Q(content__icontains=search)

            post = Post.objects.filter(q, deleted=0).order_by("-id")
            count = post.count()

            paginator = Paginator(post, 10)
            posts = paginator.page(cursor)

            data = {
                "page": cursor,
                "has_next": posts.has_next(),
                "posts": posts.object_list.values(),
                "count": count,
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "게시글 조회 성공",
                    "result": data,
                },
                status=200,
            )
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "게시글 검색 실패",
                    "result": data,
                },
                status=400,
            )

import re
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import Oauth, User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

# "user_info": {
#     "id": "123412341234123412341234",
#     "email": "sample1234@gmail.com",
#     "verified_email": true,
#     "name": "홍길동",
#     "given_name": "길동",
#     "family_name": "홍",
#     "picture": "https://lh3.googleusercontent.com/a/asdfasdfasdfasdfasdfasdfasdfasdf=asdf",
#     "locale": "ko"
# }
def get_user_info(access_token: str) -> dict:
    try:
        base_url = "https://www.googleapis.com/userinfo/v2/me"
        access_token = access_token
        url = "".join((base_url, "?access_token=", access_token))
        user_info = requests.get(url=url).json()

        return user_info
    except:
        print("get_user_info에서 에러 발생")


# =============================================
# POST /user/oauth/check
# Check User
#
# request(
#   access_token: str
# )
#
# result{
#   exists : boolean
# }
# =============================================
class UserCheck(APIView):
    """
    유저 회원가입 유무 확인

    # TO-DO를 생성할 때 사용하는 API
        - user_id : 사용자 ID
        - name : To-Do 이름
    """

    id_field = openapi.Schema(
        "id", description="To-Do가 생성되면 자동으로 채번되는 ID값", type=openapi.TYPE_STRING
    )

    success_response = openapi.Schema(
        title="response", type=openapi.TYPE_OBJECT, properties={"id": id_field}
    )

    @swagger_auto_schema(
        tags=["Oauth"],
        request_body=UserSerializer,
        query_serializer=UserSerializer,
        responses={
            200: success_response,
            403: "인증에러",
            400: "입력값 유효성 검증 실패",
            500: "서버에러",
        },
    )
    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            user_info = get_user_info(access_token)

            data = {
                "exists": user_info,
            }

            if not user_info["id"]:
                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "토큰인증 실패",
                        "result": data,
                    },
                    status=400,
                )

            # Oauth 조회
            social_account = Oauth.objects.filter(
                provider="google",
                social_id=user_info["id"],
            ).first()

            if not social_account:
                print("소셜 어카운트가 없어")

                data = {
                    "exists": False,
                }

                return Response(
                    data={
                        "code": 200000,
                        "message": "Oauth가 등록되지 않음",
                        "result": data,
                    },
                    status=200,
                )

            # 응답
            data = {
                "exists": True,
            }

            return Response(
                data={
                    "code": 200000,
                    "message": "성공",
                    "result": data,
                },
                status=200,
            )

        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "인증 실패",
                    "result": data,
                },
                status=400,
            )


# =================================================
# POST /user/oauth/signin
# SignIn User
#
# request(
#   access_token: str
# )
#
# result{
#   "user": user.nickname,
#   "user_jwt": user_jwt,
# }
# =================================================
class UserSignIn(APIView):
    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            user_info = get_user_info(access_token)

            # Oauth 조회
            oauth_exist = Oauth.objects.filter(
                provider="google",
                social_id=user_info["id"],
            ).first()

            if not oauth_exist:
                print("Oauth가 없음")

                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "Oauth가 등록되지 않음",
                        "result": data,
                    },
                    status=400,
                )

            # User 조회
            user = User.objects.filter(
                id=oauth_exist.fk_user_id.id,
            ).first()

            if not user:
                print("유저가 가입되어 있지 않음")

                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "유저가 가입되어 있지 않음",
                        "result": data,
                    },
                    status=400,
                )

            user_jwt = user.generate_token()

            serializer = UserSerializer(user)

            data = {
                "user": serializer.data,
            }

            response = Response(
                data={
                    "code": 200000,
                    "message": "로그인 성공",
                    "result": data,
                },
                status=200,
            )

            response.set_cookie(
                "user_jwt",
                user_jwt,
                path="/",
                httponly=True,
                secure=True,
                max_age=60 * 60 * 24 * 15,
            )
            print(user_jwt)

            return response
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "로그인 실패",
                    "result": data,
                },
                status=400,
            )


# =================================================
# POST /user/oauth/signup
# SignUp User
#
# request (
#    access_token: str
#    nickname: str
# )
#
# result{
#   "user": user.nickname,
#   "user_jwt": user_jwt,
# }
# =================================================
class UserSignUp(APIView):
    def post(self, request):
        try:
            nickname = request.data.get("nickname")
            access_token = request.data.get("access_token")
            provider = "google"

            nickname_regex = re.compile("([ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]{2,10})")

            # nickname 정규화 필터
            if not nickname_regex.match(nickname):
                print("닉네임이 정규식을 만족하기 못했어 !")

                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "닉네임이 정규식을 만족하기 못했어 !",
                        "result": data,
                    },
                    status=400,
                )

            # 프로필 받아오기 받아오기
            user_info = get_user_info(access_token)

            # Oauth 조회
            oauth_exist = Oauth.objects.filter(
                provider="google",
                social_id=user_info["id"],
            ).first()
            if oauth_exist:
                print("Oauth가 이미 존재")

                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "Oauth가 이미 존재",
                        "result": data,
                    },
                    status=400,
                )

            # 닉네임 조회
            nickname_exist = User.objects.filter(
                nickname=nickname,
            ).first()
            if nickname_exist:
                print("닉네임이 이미 존재")

                data = {}

                return Response(
                    data={
                        "code": 409000,
                        "message": "닉네임이 이미 존재",
                        "result": data,
                    },
                    status=409,
                )

            # User 조회
            email_exist = User.objects.filter(
                email=user_info["email"],
            ).first()
            if email_exist:
                print("유저가 가입 되어 있음")

                data = {}

                return Response(
                    data={
                        "code": 400000,
                        "message": "유저가 가입 되어 있음",
                        "result": data,
                    },
                    status=400,
                )

            # DB 생성
            user = User.objects.create(
                name=user_info["name"],
                nickname=nickname,
                email=user_info["email"],
                thumbnail=user_info["picture"],
                is_certified=True,
            )
            oauth = Oauth.objects.create(
                fk_user_id=user,
                provider=provider,
                social_id=user_info["id"],
            )

            user_jwt = user.generate_token()

            serializer = UserSerializer(user)

            data = {
                "user": serializer.data,
            }

            response = Response(
                data={
                    "code": 200000,
                    "message": "회원가입 성공",
                    "result": data,
                },
                status=200,
            )

            response.set_cookie(
                "user_jwt",
                user_jwt,
                path="/",
                httponly=True,
                secure=True,
                max_age=60 * 60 * 24 * 15,
            )

            return response

        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "회원가입 실패",
                    "result": data,
                },
                status=400,
            )


# =================================================
# POST /user/oauth/logout
# Logout User
#
# request (
# )
#
# result{
# }
# =================================================
class UserLogOut(APIView):
    def post(self, request):
        try:
            data = {}

            response = Response(
                data={
                    "code": 200000,
                    "message": "로그아웃 성공",
                    "result": data,
                },
                status=200,
            )
            response.delete_cookie("user_jwt")

            return response
        except:
            data = {}

            return Response(
                data={
                    "code": 400000,
                    "message": "로그아웃 실패",
                    "result": data,
                },
                status=400,
            )

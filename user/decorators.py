from rest_framework.response import Response

from lib.jwt import decode


def is_login(func):  # 데코레이터 명명
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")

            user_jwt = decode(request.COOKIES["user_jwt"])

            check = user_jwt["user_id"] == user_id
        except:
            check = False

        if check:
            return func(request, *args, **kwargs)
        else:
            data = {}

            return Response(
                data={
                    "code": 401000,
                    "message": "데코레이터 로그인 실패",
                    "result": data,
                },
                status=401,
            )

    return wrapper

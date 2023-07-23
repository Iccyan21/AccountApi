from .serializers import RegisterSerializer,LoginSerializer,UserUpdateSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .models import  User, AccessToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # UserIDがすでに使われていた場合
            if User.objects.filter(user_id=serializer.validated_data['user_id']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                serializer.save()
            except:
                # データベースエラー
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data['user_id']
            user = User.objects.get(user_id=user_id)  # ここでUserオブジェクトを取得
            token = AccessToken.create(user)
            return Response({'detail': "ログインが成功しました。", 'error': 0, 'token': token.token, 'user_id': user_id})
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, user_id):
        # ユーザ情報の取得
        user = User.objects.filter(user_id=user_id).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        response_data = {
            "message": "User details by user_id",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname,
                "comment": user.comment
            }
        }

        return Response(response_data, status=200)
    
class UserUpdateView(APIView):
    def patch(self, request, user_id):
        # ユーザ情報の取得
        user = User.objects.filter(user_id=user_id).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        if user_id != user.user_id:
            # 認証と異なるIDのユーザを指定した場合
            return Response({"message": "No Permission for Update"}, status=403)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            response_data = {
                "message": "User successfully updated",
                "user": {
                    "nickname": user.nickname,
                    "comment": user.comment
                }
            }
            return Response(response_data, status=200)
        else:
            error_message = serializer.errors.get('non_field_errors', ['User updation failed'])[0]
            return Response({"message": "User updation failed", "cause": error_message}, status=400)

    def post(self, request, user_id):
        return Response({"message": "Method not allowed"}, status=405)
    
class DeleteAccountView(APIView):
    def post(self, request,user_id):
        ## アカウントの削除処理
        try:
            user = User.objects.filter(user_id=user_id).first()
            user.delete()
        except User.DoesNotExist:
            raise Response("No User found")

        return Response({"message": "Account and user successfully removed"}, status=200)
        


# Create your views here.


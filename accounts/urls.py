from . import views
from django.urls import path, include


urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='user-signup'), # 新規登録処理'
    path('login/', views.LoginView.as_view(), name='user-login'), # ログイン処理
    path('users/<str:user_id>/', views.UserDetailView.as_view(), name='user-detail'), # ユーザ情報取得
    path('users/<str:user_id>/update/', views.UserUpdateView.as_view(), name='user-update'), # ユーザ情報更新
    path('delete/<str:user_id>/', views.DeleteAccountView.as_view(), name='delete-account'), # アカウント削除
]

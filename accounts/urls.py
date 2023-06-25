from django.urls import path
from .views import SignUpView, activate_account, login_View

urlpatterns = [
    path('signup/',SignUpView,name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('login/',login_View,name='login'),
]
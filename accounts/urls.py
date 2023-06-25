from django.urls import path
from .views import SignUpView, activate_account

urlpatterns = [
    path('signup/',SignUpView,name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
]
from .views import *
from django.urls import path,include


urlpatterns = [
    path('signup/',Signupuser.as_view(),name='signup'),
    path('verifyotp/',VerifyOTP.as_view(),name='verification'),
    path('login/',Login.as_view(),name='verification'),
    path('refreshToken/', RefreshTokenView.as_view()),


]
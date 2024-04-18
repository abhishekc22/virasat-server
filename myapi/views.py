import random
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import Usersignupserializer,Loginseralizer
from .models import CustomUser, VerifiedUser
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from rest_framework_simplejwt.views import TokenRefreshView


class Signupuser(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = Usersignupserializer(data=data)
            if serializer.is_valid():
                # Generate OTP
                otp = ''.join(random.choices('0123456789', k=4))
                # Save the OTP and set is_verified to False initially
                user = CustomUser.objects.create(
                    username=serializer.data.get('username'),
                    email=serializer.data.get('email'),
                    is_verified=False
                )
                user.set_password(serializer.data.get('password'))
                user.save()
                

                self.send_otp_email(user.email, otp)
              

                
                verified_user = VerifiedUser.objects.create(user=user, otp=otp)
                
                data = {'userid': user.id}
                return Response(status=status.HTTP_201_CREATED, data=data)
            else:
                print(serializer.errors)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        



    def send_otp_email(self, email, otp):
        subject = 'OTP Verification'
        message = f'Your OTP for verification is: {otp}'
        from_email ='abhishek234264@gmail.com'  
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)






class VerifyOTP(APIView):
    def post(self, request):
        print(request.data)
        try:
            user_id = request.data.get('userId')
            otp = request.data.get('otp')

            verified_user = VerifiedUser.objects.get(user_id=user_id)
            saved_otp = verified_user.otp
            
            if saved_otp == otp:
                # Mark user as verified
                user = CustomUser.objects.get(id=user_id)
                user.is_verified = True
                user.save()
                return Response(status=status.HTTP_200_OK, data={"message": "OTP verified successfully."})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Invalid OTP."})
        except (VerifiedUser.DoesNotExist, CustomUser.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User or OTP not found."})




class Login(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = Loginseralizer(data=data)
          
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = authenticate(request=request, email=email, password=password)
                if user is not None:
                    if user.is_verified:
                        refresh = RefreshToken.for_user(user)
                        return Response(status=status.HTTP_200_OK, data={
                            "message": "Login successful.",
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                            'username':user.username,
                            'userid':user.id

                        })
                    else:
                        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "User is not verified."})
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "Invalid email or password."})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    "message": "Invalid data.",
                    "errors": serializer.errors
                })
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"message": "Internal server error."})
        
        
class RefreshTokenView(APIView):
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response({'error':'refresh Token is required'},status=status.HTTP_400_BAD_REQUEST)   
            
            refresh  = RefreshToken(refresh_token)

            token = {
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            }
            
            return Response(token,status=status.HTTP_200_OK)   
        except Exception as e:
            print(e)  
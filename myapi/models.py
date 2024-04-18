from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.email



class VerifiedUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification')
    otp = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s OTP ({self.otp})"

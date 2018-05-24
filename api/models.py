from django.contrib.auth.models import User
from django.db import models


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roleName = models.CharField(max_length=30)

    def __str__(self):
        return self.roleName

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
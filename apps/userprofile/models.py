from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_tutor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, related_name="Tutor", on_delete=models.CASCADE)
    department = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, related_name="Student", on_delete=models.CASCADE)
    department = models.CharField(max_length=50, null=True, blank=True)
    tutor = models.ForeignKey(Tutor, blank=True, null=True, related_name="students", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
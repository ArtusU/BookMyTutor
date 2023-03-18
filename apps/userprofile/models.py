from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_tutor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class Department(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, related_name="Tutor", on_delete=models.CASCADE)
    department = models.CharField(max_length=50, null=True, blank=True)
    #department = models.ForeignKey(Department, related_name="tutors", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, related_name="Student", on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, blank=True, null=True, related_name="students", on_delete=models.CASCADE)
    department = models.CharField(max_length=50, null=True, blank=True)
    #department = models.ForeignKey(Department, related_name="students", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


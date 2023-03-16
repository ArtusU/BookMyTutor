from django.contrib import admin

from .models import CustomUser, Tutor, Student


admin.site.register(CustomUser)
admin.site.register(Tutor)
admin.site.register(Student)

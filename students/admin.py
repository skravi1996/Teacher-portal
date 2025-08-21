from django.contrib import admin
from .models import Teacher, Student,AuditLog

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(AuditLog)

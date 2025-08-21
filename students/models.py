from django.db import models

# Create your models here.
import hashlib
import os
from datetime import datetime

class Teacher(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=256)
    salt = models.CharField(max_length=32)

    def set_password(self, raw_password):
        self.salt = os.urandom(16).hex()
        self.password_hash = hashlib.sha256((raw_password + self.salt).encode()).hexdigest()

    def check_password(self, raw_password):
        return self.password_hash == hashlib.sha256((raw_password + self.salt).encode()).hexdigest()
    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class AuditLog(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=datetime.now)
    details = models.TextField()


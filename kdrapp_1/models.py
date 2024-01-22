from django.db import models
from django.contrib.auth.models import User

class User_details(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    join_date = models.DateField(null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    email = models.EmailField(null=True)
    contact_number = models.CharField(null=True, max_length=15)
    university_name = models.CharField(null=True, max_length=200)
    photo = models.ImageField(upload_to='user_profile_pic/', null=True,blank = True)

    def __str__(self):
        return f" {self.username} {self.university_name}"

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.task_name} {self.description}"

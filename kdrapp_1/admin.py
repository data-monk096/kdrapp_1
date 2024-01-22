from django.contrib import admin
from kdrapp_1.models import User_details
from kdrapp_1.models import Task

class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "university_name","task",)
admin.site.register(User_details, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
  list_display = ("task_name","description")
admin.site.register(Task,TaskAdmin)
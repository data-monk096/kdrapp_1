from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/',views.login_user,name='login_user'),
    path('homepage/',views.content_1,name='homepage'),
    path('user_photo/<str:username>/', views.user_photo, name='user_photo'),
    path('edit_task/',views.edit_task, name='edit_task'),
    path('assign_task/',views.task_add_assign,name='task_add_assign'),
    path('',views.main, name='main'),
    path('logout/',views.log_out, name = 'log_out'),
    path('signup/',views.signup_newuser, name='signup_user')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
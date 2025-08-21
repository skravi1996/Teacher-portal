from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('home/', views.home, name='home'),
    path('update_marks/<int:student_id>/', views.update_marks, name='update_marks'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add_student/', views.add_student, name='add_student'),
]

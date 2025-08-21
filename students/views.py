from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher, Student, AuditLog
import uuid
from django.contrib import messages

SESSION_STORE = {}

def calculate_new_marks(existing, new):
    return (existing + new)


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Teacher.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        teacher = Teacher(username=username)
        teacher.set_password(password)
        teacher.save()
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher = Teacher.objects.filter(username=username).first()
        if teacher and teacher.check_password(password):
            session_token = str(uuid.uuid4())
            SESSION_STORE[session_token] = teacher.id
            response = redirect('home')
            response.set_cookie('session_token', session_token, httponly=True, secure=True)
            messages.success(request, "Logged In successfully")
            return response
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    session_token = request.COOKIES.get('session_token')
    if session_token and session_token in SESSION_STORE:
        del SESSION_STORE[session_token]
    response = redirect('login')
    response.delete_cookie('session_token')
    messages.success(request, "Logged out successfully")
    return response


def home(request):
    session_token = request.COOKIES.get('session_token')
    teacher_id = SESSION_STORE.get(session_token)
    if not teacher_id:
        return redirect('login')          
    students = Student.objects.all()
    return render(request, 'home.html', {'students': students})


def update_marks(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        new_marks = int(request.POST.get('marks'))
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        if new_marks < 0 or new_marks > 100:
            messages.error(request, "Total marks cannot exceed 100")
            return redirect("home")
        else:
            messages.success(request, f"Marks updated for {name}")
        student.marks = new_marks
        student.name = name
        student.subject = subject
        student.save()
        teacher_id = SESSION_STORE.get(request.COOKIES.get('session_token'))
        AuditLog.objects.create(
            teacher_id=teacher_id,
            student=student,
            action='update_marks',
            details=f'Updated marks to {new_marks}'
        )
        return redirect('home')


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher_id = SESSION_STORE.get(request.COOKIES.get('session_token'))
    AuditLog.objects.create(
        teacher_id=teacher_id,
        student=student,
        action='delete_student',
        details=f'Student {student.name} deleted'
    )
    messages.success(request, f"Student  {student.name} delete successfully")
    student.delete()
    
    return redirect('home')


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        marks = int(request.POST.get('marks'))
        existing = Student.objects.filter(name=name, subject=subject).first()
        action = ''
        if existing:
            total_marks = calculate_new_marks(existing.marks, marks)
            if total_marks > 100:
                messages.error(request, "Total marks cannot exceed 100")
            else:
                existing.marks = total_marks
                existing.save()
                action = 'update_marks'
                messages.success(request, f"Marks updated for {name}")
        else:
            if marks > 100:
                messages.error(request, "Marks cannot exceed 100")
                return redirect("home")
            existing = Student.objects.create(name=name, subject=subject, marks=marks)
            action = 'add_student'
            messages.success(request, f"Student {name} added successfully")
        teacher_id = SESSION_STORE.get(request.COOKIES.get('session_token'))
        AuditLog.objects.create(teacher_id=teacher_id,student=existing,action=action,details=f'Student {name} {action}')
        return redirect("home")

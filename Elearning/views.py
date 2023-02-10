from django.http import HttpResponse
from django.shortcuts import render, redirect
from subject.forms import CoursesForm, ContentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from subject.models import course, description, purchase, check, OTP
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import json
import random
import time
from subject.task import *
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from allauth.socialaccount.views import ConnectionsView


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def celerys(request):
    #timesleep.delay()
    sendemail.delay()
    return HttpResponse(("Hello from celery"))

def sociallogin(request):
    return render(request,'social_login.html')

def schedule_mail(request):
    schedule,created=CrontabSchedule.objects.get_or_create(hour=12,minute=37)
    schedule.timezone = 'Asia/Kolkata'
    schedule.save()
    task=PeriodicTask.objects.get_or_create(task='subject.task.sendemail',name='unique23',crontab=schedule)#,args=json.dumps((2,3,)))
    return HttpResponse("scheduled succesfully")

def mail(user):
    subject = "welcome to Elearning course"
    s = random.randint(1000, 9999)
    OTP.objects.first().delete()
    OTP.objects.create(otp=s)
    message = f"Hi {user.first_name} {user.last_name}, Thank you for registering in Elearning your otp is {s}."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def check_otp(request):
    if request.method == "POST":
        otps = request.POST.get("otp")
        s = OTP.objects.all().values("otp")
        value = s[0]["otp"]
        if int(value) == int(otps):
            return redirect("home")
        else:
            messages.info(request, "Invalid OTP. Please try again.")
            return redirect("check_otp")
    return render(request, "otp.html")


def login(request):
    if request.method == "POST":
        name = request.POST.get("name")

        password = request.POST.get("pass")
        try:
            user = User.objects.get(username=name)
        except:
            messages.info(request, "User not found")
        user = authenticate(username=name, password=password)
        if user is not None:
            auth_login(request, user)
            mail(user)
            return redirect("check_otp")

        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    return render(request, "login.html")


def home(request):
    s = course.objects.all()
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    if cache.get(q):
        value = cache.get(q)
        print(CACHE_TTL)
        print("Cached value")
    else:
        value = course.objects.filter(course_name__icontains=q)
        print("data from database")
        cache.set(q, value, CACHE_TTL)
    if value:
        data = {"s": s, "value": value}
        return render(request, "home.html", data)
    else:
        messages.info(request, "No result found")
        data = {"s": s, "value": value}
        return render(request, "home.html", data)


def edit(request):
    form = CoursesForm()
    if request.method == "POST":
        form = CoursesForm(request.POST)
        if form.is_valid():
            k = form.save(commit=False)
            k.edited = request.user
            k.save()
            return redirect("home")
    data = {"form": form}
    return render(request, "creating_courses.html", data)


def register_as_teacher(request):
    form = UserCreationForm()
    if request.method == "POST":
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.username = user.username.lower()
            user.is_superuser = True
            user.is_staff = True
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            auth_login(request, user)
            mail(user)
            return redirect("check_otp")
    data = {"form": form}
    return render(request, "register.html", data)


def register_as_student(request):
    form = UserCreationForm()
    if request.method == "POST":
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = email
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            auth_login(request, user)
            mail(user)
            return redirect("check_otp")
    data = {"form": form}
    return render(request, "register.html", data)


def logout(request):
    auth_logout(request)
    return render(request, "login.html")


def delete(request, pk):
    value = course.objects.get(id=pk)
    if request.method == "POST":
        value.delete()
        return redirect("home")
    data = {"value": value}
    return render(request, "delete.html", data)


def update(request, pk):
    value = course.objects.get(id=pk)
    form = CoursesForm(instance=value)
    if request.method == "POST":
        form = CoursesForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            return redirect("home")
    data = {"form": form}
    return render(request, "creating_courses.html", data)


def addcontent(request, pk):
    name = course.objects.get(id=pk)
    form = ContentForm()
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.name = name
            user.save()
            return redirect("home")
    data = {"form": form}
    return render(request, "content_edit.html", data)


def content(request, pk):
    value = description.objects.get(id=pk)
    form = ContentForm(instance=value)
    if request.method == "POST":
        form = ContentForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            return redirect("home")
    data = {"form": form}
    return render(request, "content_edit.html", data)


def purchase(request, pk):
    if request.user.is_superuser:
        value = course.objects.get(id=pk)
        result = value.description_set.all().values()
        dum = value.description_set.all().values("id")
        if len(dum) > 0:
            route = dum[0]["id"]
            return render(
                request,
                "description.html",
                {"result": result, "value": value, "route": route},
            )
        else:
            return render(
                request, "description.html", {"result": result, "value": value}
            )
    else:
        value = course.objects.get(id=pk)
        p = check.objects.filter(
            check_topic=value, check_user=request.user.get_full_name()
        ).count()
        if p == 0:
            if request.method == "POST":
                p = check(check_topic=value, check_user=request.user.get_full_name())
                p.save()
                value = course.objects.get(id=pk)
                result = value.description_set.all()
                return render(
                    request, "description.html", {"result": result, "value": value}
                )

        else:
            result = value.description_set.all()
            return render(
                request, "description.html", {"result": result, "value": value}
            )
        data = {"value": value}
        return render(request, "purchase.html", data)


def deletecontent(request, pk):
    result = course.objects.get(id=pk)
    value = result.description_set.all().values("id")
    k = value[0]["id"]
    content = description.objects.get(id=k)
    print(content)
    if request.method == "POST":
        content.delete()
        return redirect("home")
    return render(request, "delete.html", {"result": result, "message": "Contents"})


def purchaselist(request, pk):
    value = course.objects.get(id=pk)
    k = check.objects.filter(check_topic=value)
    return render(request, "purchase.html", {"value": value, "k": k})

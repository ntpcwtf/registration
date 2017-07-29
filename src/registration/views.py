# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pprint import pprint
from random import randrange

import re

from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as djlogin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from registration.models import Registration

CHARSET = '0123456789'
LENGTH = 8
MAX_TRIES = 32


def home(request):
    return render(request, "reg/index.html", {})


def register(request):
    if request.method != "POST":
        messages.error(request, "Unknown error occured, please try again... (155)")
        return HttpResponseRedirect('/')

    email = request.POST.get("email", None)
    password = request.POST.get("password", None)
    password_again = request.POST.get("password-again", None)
    fullname = request.POST.get("fullname", None)
    notes = request.POST.get("notes", None)

    stct = request.POST.get("stct", False)
    ctpa = request.POST.get("ctpa", False)
    paso = request.POST.get("paso", False)
    sone = request.POST.get("sone", False)

    if stct is not False:
        stct = True

    if ctpa is not False:
        ctpa = True

    if paso is not False:
        paso = True

    if sone is not False:
        sone = True

    error = False

    if email is None:
        error = True
        messages.warning(request, "Email must not be empty")

    if password is None:
        error = True
        messages.warning(request, "Password must not be empty")

    if password_again is None:
        error = True
        messages.warning(request, "Password must not be empty")

    if fullname is None:
        error = True
        messages.warning(request, "Full name must not be empty")

    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        error = True
        messages.warning(request, "Please fill in a valid email address")

    if password != password_again:
        error = True
        messages.warning(request, "Passwords must match")

    if User.objects.filter(email=email).exists():
        error = True
        messages.warning(request, "User with this email already exists.")

    if error is True:
        return HttpResponseRedirect('/')

    code = None

    loop_num = 0
    unique = False
    while not unique:
        if loop_num < MAX_TRIES:
            new_code = ''
            for i in xrange(LENGTH):
                new_code += CHARSET[randrange(0, len(CHARSET))]
            if not User.objects.filter(username=new_code):
                code = new_code
                unique = True
            loop_num += 1
        else:
            messages.error(request, "Unknown error occured, please try again... (255)")
            return HttpResponseRedirect('/')

    pprint(stct)
    pprint(request.POST.getlist('stct'))

    user = User.objects.create_user(username=code, email=email, password=password)
    registration = Registration.objects.create(user=user, fullname=fullname, notes=notes, stct=stct, ctpa=ctpa,
                                               paso=paso, sone=sone)

    send_mail(
        subject='NTPC Registration',
        message='You have been successfully registered to NTPC! You can log in over at https://reg.ntpc.wtf/login with '
        'your email and password to review your information...',
        html_message='<h1>Welcome to NTPC!</h1>'
                     '<p>You have been successfully registered to NTPC!</p>'
                     '<p>Your payment ID is ' + code + '</p>'
                     '<p>You can now head over to <a href="https://reg.ntpc.wtf/login">the members page</a> and log'
                     'in with your email and password to review your details.</p>'
                     '<p>Also, please head over to <a href="https://lists.ntpc.wtf/mailman/listinfo/pub">NTPC Mailing List</a>'
                     ' and register there to receive notifications regarding the event.</p>',
        from_email='noreply@ntpc.wtf',
        recipient_list=[email],
        fail_silently=False,
    )

    return render(request, "reg/success.html", {"registered": user, "registration": registration})


def login(request):
    return render(request, "reg/login.html")


def signin(request):
    if request.method != "POST":
        messages.error(request, "Unknown error (313)")

    email = request.POST.get("email", None)
    password = request.POST.get("password", None)

    dbuser = User.objects.get(email=email)

    user = authenticate(username=dbuser.username, password=password)
    if user is not None:
        djlogin(request, user)
        return HttpResponseRedirect("/members")
    else:
        messages.warning(request, "Invalid email/password combination")
        return HttpResponseRedirect("/login")

@login_required
def members(request):
    user = request.user
    registration = Registration.objects.get(user=user)

    return render(request, "reg/members.html", {"registration": registration})


def logUserOut(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect("/")
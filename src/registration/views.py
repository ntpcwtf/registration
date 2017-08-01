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
        html_message='<h1>Welcome to NTPC!</h1>'
                     '<p>You have been successfully registered to NTPC!</p>'
                     '<p>Your payment ID is <b>' + code + '</b>. Use it as the variable symbol when sending your payment.</p>'
                     '<p>Please send <b>1200 CZK</b> (or 46 EUR) to a bank account number <b>2200041594/2010</b> (FIO Bank). (Please see below for international and EUR payments)</p>'
                     '<p>If you do not want to stay for the whole time, please contact <a href="mailto:snajpa@snajpa.net">snajpa@snajpa.net</a>'
                     '<p>You can now go to <a href="https://reg.ntpc.wtf/login">the members page</a> and log'
                     'in with your email and password to review your details.</p>'
                     '<p>Also, please visit <a href="https://lists.ntpc.wtf/mailman/listinfo/pub">NTPC Mailing List</a>'
                     ' and register there to receive notifications regarding the event.</p>'
                     '<p>Alternatively, you can use this QR code to pay quickly with your phone!</p>'
                     '<p><b>QR For CZK</b></p>'
                     '<img src="https://api.paylibo.com/paylibo/generator/czech/image?compress=false&size=40&accountNumber=2200041594&bankCode=2010&amount=1200&currency=CZK&vs=' + code + '" alt="Quick Payment QR Code" />'
                     '<p><b>QR For EUR</b></p>'
                     '<img src="https://api.paylibo.com/paylibo/generator/image?compress=false&size=40&iban=SK1583300000002200041594&amount=46&currency=EUR&vs="' + code +' alt="Quick Payment QR Code" />'
                     '<hr />'
                     '<p>If you are paying in EUR, please use the Slovak account with number 2200041594/8330 (FIO Bank)</p>'
                     '<p><b>International payment details:</b></p>'
                     '<p><b>IBAN CZ:</b> CZ0420100000002200041594<br />'
                     '<b>BIC: FIOBCZPPXXX</b><br />'
                     '<b>IBAN SK:</b> SK1583300000002200041594<br />'
                     '<b>BIC SK:</b> FIOZSKBA</p>',
        message='Welcome to NTPC!\r\n\r\n'
                'You have been successfully registered to NTPC!\r\n'
                'Your payment ID is ' + code + '\r\n'
                'Please send 1200 CZK (or 46 EUR) to a bank account number 2200041594/2010 (FIO Bank). (Please see below for international and EUR payments)\r\n'
                'If you do not want to stay for the whole time, please contact snajpa@snajpa.net\r\n'
                'You can now go to https://reg.ntpc.wtf/login and log in'
                'with your email and password to review your details.\r\n'
                'Also, please visit https://lists.ntpc.wtf/mailman/listinfo/pub '
                'and register there to receive notifications regarding the event.\r\n'
                'Alternatively, use one of these QR codes to pay quickly with your phone!\r\n'
                '- CZK: https://api.paylibo.com/paylibo/generator/czech/image?compress=false&size=440&accountNumber=2200041594&bankCode=2010&amount=1200&currency=CZK&vs=' + code + '/r/n'
                '- EUR: https://api.paylibo.com/paylibo/generator/image?compress=false&size=440&iban=SK1583300000002200041594&amount=46&currency=EUR&vs=' + code + '/r/n'
                '\r\n'
                'If you are paying in EUR, please use the Slovak account with number 2200041594/8330 (FIO Bank)\r\n'
                'International payment details:\r\n'
                'IBAN CZ: CZ0420100000002200041594\r\n'
                'BIC: FIOBCZPPXXX\r\n'
                'IBAN SK: SK1583300000002200041594\r\n'
                'BIC SK: FIOZSKBA\r\n',
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

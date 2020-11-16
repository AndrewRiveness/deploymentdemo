from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from.models import *


def index(request):
    return render(request, "loginreg.html")



def register(request):
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print("ERRORS FROM VALIDATOR BELOW")
    print(errorsFromValidator)
    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        newUser = User.objects.create(
            first_name=request.POST['UserFirst'], last_name=request.POST['UserLast'], email=request.POST['UserEmail'], password=request.POST['UserPW'])
        request.session['loggedInID'] = newUser.id
    return redirect("/success")



def success(request):
    if 'loggedInID' not in request.session:
        messages.error(request, "You Must Be Logged In First")
        return redirect("/")
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInID']),
        'allTrips' : Trip.objects.all(),
        'favTrips' : Trip.objects.filter(favoritors=User.objects.get(id=request.session['loggedInID'])),
        'nonTrips' : Trip.objects.exclude(favoritors=User.objects.get(id=request.session['loggedInID']))
    }
    return render(request, "loggedin.html", context)



def login(request):
    errorsFromValidator = User.objects.loginValidator(request.POST)
    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        userswithmatchingemail = User.objects.filter(email = request.POST['UserEmail'])
        request.session['loggedInID'] = userswithmatchingemail[0].id
    return redirect("/success")



def logout(request):
    request.session.clear()
    return redirect("/")



def createtravel(request):
    return render(request, "createtravel.html")

def uploadtravel(request):
    errorsfromTripValidator = Trip.objects.createTripValidator(request.POST)
    print(errorsfromTripValidator)
    if len(errorsfromTripValidator) >0:
        for key, value in errorsfromTripValidator.items():
            messages.error(request, value)
        return redirect("/trip/create")
    else:
        Trip.objects.create(description= request.POST['desc'], creator = User.objects.get(id=request.session['loggedInID']), start_date=request.POST['startDate'], end_date=request.POST['endDate'], plan=request.POST['plan'])
    return redirect("/success")

def tripinfo(request, tripID):
    context = {
        'onetrip' : Trip.objects.get(id=tripID)
    }
    return render(request, "tripinfo.html", context)

def addtrip(request,tripID):
    Trip.objects.get(id=tripID).favoritors.add(User.objects.get(id=request.session['loggedInID']))
    return redirect("/success")

def removetrip(request,tripID):
    Trip.objects.get(id=tripID).favoritors.remove(User.objects.get(id=request.session['loggedInID']))
    return redirect("/success")

def deletetrip(request,tripID):
    Trip.objects.get(id=tripID).delete()
    return redirect("/success")


from django.urls import path     
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("success", views.success),
    path("logout", views.logout),
    path("login", views.login),
    path("trip/create", views.createtravel),
    path("uploadtravel", views.uploadtravel),
    path("trip/<int:tripID>", views.tripinfo),
    path('addtrip/<int:tripID>', views.addtrip),
    path('removetrip/<int:tripID>', views.removetrip),
    path('deletetrip/<int:tripID>', views.deletetrip),
]
from django.http import request
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from .models import *
from django.views.generic import ListView,FormView,DeleteView
from.models import Room,Booking
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import AvailabilityForm
from home.booking_functions.availability import check_availability


import datetime
def RoomList(request):

    room=Room.objects.all()[0]
    room_categories= dict(room.ROOM_CATEGORIES)

    room_values =room_categories.values()

    room_list=[]
    for room_category in room_categories:
        room= room_categories.get(room_category)
        room_url=reverse('RoomDetailView',kwargs={'category':room_category})
        room_list.append((room,room_url))

    context={'room_list':room_list,}

    return render(request,'room_list_view.html',context)

class BookingList(ListView):
    model= Booking
    def get_queryset(self,*args, **kwargs):
        if self.request.user.is_staff:

            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

class RoomDetailView(View):

    def get(self, request, *args, **kwargs):

        room_category = self.kwargs.get('category',None)
        form =AvailabilityForm()
        room_list = Room.objects.filter(category= room_category)

        if len(room_list)>0:
            room = room_list[0]
            room_category=dict(room.ROOM_CATEGORIES).get(room.category, None)


            context ={ 'room_category' : room_category,
                       'form':form,}
            return render (request ,'room_details.html',context)
        else:
            return  HttpResponse('category does not exist')



    def post(self,request, *args, **kwargs):
        room_category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category= room_category)
        form= AvailabilityForm(request.POST)
        if form.is_valid():
            data =form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms ) > 0:

            room = available_rooms[0]
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out'],
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of room is booked !!')


class BookingView(FormView)  :
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    def form_valid(self, form):
        data =form.cleaned_data
        room_list=Room.objects.filter(category=data['room_category'])
        available_rooms=[]
        for room in room_list:
            if check_availability(room,data['check_in'],data['check_out']):
                available_rooms.append(room)
        if len(available_rooms>0) :

            room=available_rooms[0]
            booking=Booking.objects.create(
            user = request.user,
            room=room,
            check_in=data['check_in'],
            check_out=data['check_out'],
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of room is booked !!')





def nav(request):
    return render(request,'slideimage.html')
def about(request):
    return render(request,'about.html')
def signup(request):
    error = False
    if request.method == "POST":
        u = request.POST['uname']
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']

        m = request.POST['mobile']
        g = request.POST['male']
        d = request.POST['birth']
        p = request.POST['pwd']
        user = User.objects.create_user(first_name=f, last_name=l, username=u, password=p, email=e)
        Register.objects.create(user=user, mobile=m, gender=g, dob=d)
        error = True
    d = {'error': error}
    return render(request, 'signup.html', d)


def signin(request):

    if request.method =="POST":
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return render(request,'room_list_view.html')
    else:
        fm=AuthenticationForm()

    return render(request,'login.html',{'form':fm})
def contact(request):
    return render(request,'contact.html')
def log_out(request):
    logout(request)
    return redirect('nav')


class Cancelbookingview(DeleteView):
    model= Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingList')



# Create your views here.


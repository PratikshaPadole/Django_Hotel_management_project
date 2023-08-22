from django.contrib import admin
from django.urls import path, include
from .views import about, signin, signup, contact, nav, log_out,RoomList,BookingList,BookingView,RoomDetailView,Cancelbookingview

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', nav,name='nav'),
    path('about/',about,name='about'),
    path('signin/',signin,name='signin'),
    path('signup/',signup,name='signup'),
    path('contact/',contact,name='contact'),
    path('room_list/',RoomList,name='RoomList'),
    path('booking_list/',BookingList.as_view(),name='BookingList'),
    path('book/',BookingView.as_view(),name='booking_view'),
    path('room/<category>',RoomDetailView.as_view(),name='RoomDetailView'),
    path('booking/cancel/<pk>',Cancelbookingview.as_view(),name='Cancelbookingview'),

    path('log_out/',log_out,name='log_out'),


]

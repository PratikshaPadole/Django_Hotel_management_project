from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.conf import settings
from django.urls import reverse, reverse_lazy


class Register(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField(max_length=10,null=True)
    add = models.CharField(max_length=100,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.user.user_name

# Create your models her
class Room(models.Model):
    ROOM_CATEGORIES=(
        ('YAC','AC'),
        ('NAC','NON-AC'),('DEL','DELUXE'),('KIN','KING'),
        ('QUE','QUEEN'),
        )

    number=models.IntegerField()
    category=models.CharField(max_length=3,choices=ROOM_CATEGORIES)
    beds=models.IntegerField()
    capacity=models.IntegerField()
    def __str__(self):
        return f'{self.number}.{self.category} with {self.beds} beds for {self.capacity} people'

class Booking(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    check_in=models.DateTimeField()
    check_out = models.DateTimeField()
    def __str__(self):
        return f'{self.user} has booked {self.room} from{self.check_in}to {self.check_out}'
    def get_room_category(self):
        room_categories =dict(self.room.ROOM_CATEGORIES)
        room_category =room_categories.get(self.room.category)
        return room_category
    def get_cancel_booking_url(self):
        return  reverse_lazy('Cancelbookingview',args=[self.pk,])


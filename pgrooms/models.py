from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class extendeduser(models.Model):
    mobile = models.CharField(max_length = 15)
    user = models.OneToOneField(User,on_delete=models.CASCADE) 

class State(models.Model):
    statename =models.CharField(max_length=30,unique=True)
    def __str__(self):
         return self.statename

class City(models.Model):
    statename = models.ForeignKey(State , on_delete=models.DO_NOTHING)
    cityname = models.CharField(max_length=30,unique=True)
    def __str__(self):
         return self.cityname

class Room(models.Model):
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    pgname = models.CharField(max_length=100)
    pgtype = models.CharField(max_length=30)
    img = models.ImageField(upload_to='pics')
    statename = models.ForeignKey(State , on_delete=models.DO_NOTHING)
    cityname = models.ForeignKey(City , on_delete=models.DO_NOTHING)
    statename1 = models.CharField(default=None, blank=True, null=True,max_length=30)
    cityname1 = models.CharField(default=None, blank=True, null=True,max_length=30)
    pgaddress = models.TextField()
    gmap = models.TextField()
    desc = models.TextField()
    price = models.IntegerField()
    bedno = models.IntegerField()
    payment= models.IntegerField(default=None, blank=True, null=True)
    verifystatus = models.BooleanField(default=False)
    activestatus = models.BooleanField(default=True)
    availbalebed = models.IntegerField()
    freebed = models.IntegerField()
    def __str__(self):
        return "{} : {}".format(str(self.id), self.pgname)
        
class pgverification(models.Model):
    verifier = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    verifydate = models.DateTimeField(default=None, blank=True, null=True)
    feedback = models.TextField(default=None, blank=True, null=True)
    roomid = models.ForeignKey(Room , on_delete=models.DO_NOTHING)
    allotedstatus = models.BooleanField(default=True)

    def __str__(self):
        return self.id

class booking(models.Model):
    roomid = models.ForeignKey(Room , on_delete=models.DO_NOTHING)
    booktime = models.DateTimeField()
    vacate = models.DateTimeField(default=None, blank=True, null=True)
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    payment = models.IntegerField(default=None, blank=True, null=True)
    refund = models.IntegerField(default=None, blank=True, null=True)
    paymentstatus = models.BooleanField(default=False)
    bookingstatus = models.BooleanField(default=False)
    forcecancel = models.BooleanField(default=False)
    refundstatus = models.BooleanField(default=False)
    cancelstatus= models.BooleanField(default=False)


class cancelledbooking(models.Model):
    roomid = models.ForeignKey(Room , on_delete=models.DO_NOTHING)
    bookid = models.ForeignKey(booking , on_delete=models.DO_NOTHING)
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    canceltime = models.DateTimeField(default=None, blank=True, null=True)
    refund = models.IntegerField(default=None, blank=True, null=True)
    forcecancel = models.BooleanField(default=False)
    refundstatus = models.BooleanField(default=False)
    cancelstatus= models.BooleanField(default=False)

class PGSummary(Room):
    class Meta:
        proxy = True
        verbose_name = 'PG Summary'
        verbose_name_plural = 'PGs Summary'    

class bookingSummary(booking):
    class Meta:
        proxy = True
        verbose_name = 'Booking Report'
        verbose_name_plural = 'Bookings Report'        
        
class cancelSummary(cancelledbooking):
    class Meta:
        proxy = True
        verbose_name = 'CancelledBooking Report'
        verbose_name_plural = 'CancelledBookings Report'           


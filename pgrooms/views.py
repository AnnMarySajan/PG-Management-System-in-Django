from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import cancelledbooking, extendeduser,State,City,Room,pgverification,booking
import datetime
import stripe #to use stripe as payment gateway
from django.conf import settings

# Create your views here.
def homepage(request):
    if request.method=='POST':
        place = request.POST['place']
        pgobjs = Room.objects.filter(cityname = place,verifystatus = True).order_by('price')
        cities = City.objects.all()
        return render(request,'homepage.html',{'pgobjs' : pgobjs, 'cities' : cities})
    else :
        pgobjs = Room.objects.filter(verifystatus = True,activestatus=True).order_by('price')
        cities = City.objects.all()
        return render(request,'homepage.html',{'pgobjs' : pgobjs, 'cities' : cities})


def register(request):
    if request.method == 'POST':
        #variablename=request.POST['html_variable_name']
        username = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['phone']
        password1 = request.POST['password']
        password2 = request.POST['retypepassword']

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')

            else:
                user = User.objects.create_user(username=email,email=email,password=password1,first_name=username)
                newextendeduser = extendeduser(mobile=mobile, user=user)
                newextendeduser.save();
                messages.info(request,'user created')
                return redirect('login')
                
        else:      
            messages.info(request,'passwords not matching')
            return redirect('register')
 
    else:
        return render(request,"register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                messages.info(request,'Login Successful')
                return redirect("/emphome")
            else:    
                auth.login(request, user)
                messages.info(request,'Login Successful')
                return redirect("/")
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def forpgowners(request):
    return render(request,'forpgowners.html')

def addnewpg(request):
    if request.method == 'POST':
        userid = request.user.id
        pgname = request.POST['pgname']
        pgtype = request.POST['pgtype']
        img = request.FILES['img']
        statenamee = request.POST['statename']
        citynamee = request.POST['cityname']
        pgaddress = request.POST['pgaddress']
        desc = request.POST['descriptions']
        price = request.POST['price']
        bedno = request.POST['bedno']
        availbalebed = bedno
        freebed = bedno
        st = State.objects.get(id=statenamee)
        statename1 = st.statename
        ct = City.objects.get(id=citynamee)
        cityname1 = ct.cityname
        payment = 1000
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        stripe_total = 100000
        userid = request.user.id

        token = request.POST['stripeToken']
        email = request.POST['stripeEmail']
        customer = stripe.Customer.create(email=email,source=token)
        charge = stripe.Charge.create(amount=stripe_total,currency="inr",customer=customer.id)

        newroom = Room(userid_id=userid,pgname=pgname,pgtype=pgtype,img=img,statename_id=statenamee,cityname_id=citynamee,statename1=statename1,cityname1=cityname1,pgaddress=pgaddress,desc=desc,price=price,bedno=bedno,availbalebed=availbalebed,freebed=freebed,payment=payment)
        newroom.save();
        messages.info(request,'New PG Added Successfully')
        return render(request,'forpgowners.html',)
    
    else:
        stateobj= State.objects.all()
        cityobj= City.objects.all()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data_key = settings.STRIPE_PUBLISHABLE_KEY
        stripe_total = 100000  
        return render(request,'addnewpg.html',{'States':stateobj,'Cities':cityobj,'data_key' : data_key, 'stripe_total' : stripe_total})

def yourpglist(request):
    userid = request.user.id
    roomobj = Room.objects.filter(userid=userid)
    return render(request,'yourpglist.html',{'roomobj' : roomobj})

def editlisting(request):
    if request.method == 'POST':
        if 'edit' in request.POST:
            roomid = request.POST['roomid']
            pgname = request.POST['pgname']
            price = request.POST['price']
            bedno = request.POST['bedno']
            desc = request.POST['descriptions']
            activestatus = request.POST['activestatus']

            editroom = Room.objects.get(id = roomid)
            editroom.pgname = pgname
            editroom.price = price
            editroom.desc=desc
            editroom.bedno=bedno
            editroom.availbalebed = bedno
            editroom.freebed = bedno
            editroom.activestatus = activestatus
            editroom.save();
            messages.info(request,'Update successful')
            return render(request,'yourpglist.html',)
            
    else:    
        id = request.GET.get('pg')
        roomobj = Room.objects.filter(id=id)
        return render(request,'editlisting.html',{'roomobj' : roomobj})
        
def emphome(request):   
    if request.user.is_staff:
        roomobj = Room.objects.filter(verifystatus=False)  
        return render(request,'emphome.html',{'roomobj' : roomobj})
    else:
        return render(request,"homepage.html")
        
def acceptrequest(request):
    room_id = request.GET.get('pg') 
    room = Room.objects.get(id=room_id)
    myuserid = room.userid_id
    usermobobj = extendeduser.objects.get(user=myuserid)
    commitobj = pgverification.objects.filter(roomid=room_id,allotedstatus=True).first()
    return render(request,'acceptrequest.html',{'room' : room, 'usermobobj' : usermobobj, 'commitobj' : commitobj})

def commiting(request):
    roomid = request.GET.get('pg')
    verifier = request.user.id
    commit = pgverification(allotedstatus=True,roomid_id=roomid,verifier_id=verifier)
    commit.save();
    messages.info(request,'You can now verify the alloted slot')
    return redirect('emphome')    

def verification(request):
    userid = request.user.id
    pgverifyobj = pgverification.objects.filter(allotedstatus=True,verifier_id=userid)
    
    return render(request,'verification.html',{'pgverifyobj' : pgverifyobj})    

def unallot(request):
    verifyid = request.GET.get('pg')
    allotedlot = pgverification.objects.get(id = verifyid)
    allotedlot.allotedstatus = False
    allotedlot.save();
    messages.info(request,'Slot Unallocation done successfully!!!')
    return redirect('verification')

def verifing(request):
    if request.method == 'POST':
        verifyid = request.POST['verifyid']
        pgname = request.POST['pgname']
        pgroomid = request.POST['pgroomid']
        addescription = request.POST['description']
        pgaddress = request.POST['pgaddress']
        adprice = request.POST['price']
        gmaplink = request.POST['gmaplink']
        verifyfeedback = request.POST['feedback']


        roomobj = Room.objects.get(id = pgroomid)
        roomobj.verifystatus = True
        roomobj.pgname = pgname
        roomobj.desc = addescription
        roomobj.pgaddress = pgaddress
        roomobj.price = adprice
        roomobj.gmap = gmaplink
        
        verifyobj = pgverification.objects.get(id = verifyid)
        verifyobj.feedback = verifyfeedback
        verifyobj.verifydate = datetime.datetime.now()

        roomobj.save();
        verifyobj.save();
        messages.info(request,'Slot verified successfully!!!')
        return redirect('verifiedbyme')        


    else:
        verifyid = request.GET.get('verify')
        roomid = request.GET.get('room')
        verifyobjs = pgverification.objects.get(id = verifyid)
        roomobjs = Room.objects.get(id = roomid)
        return render(request,'verifing.html',{'verifyobjs' : verifyobjs, 'roomobjs' : roomobjs})


def verifiedbyme(request):
    userid = request.user.id
    pgverifyobj = pgverification.objects.filter(verifier_id=userid,roomid__verifystatus=True,allotedstatus=True)  
    return render(request,'verifiedbyme.html',{'pgverifyobj' : pgverifyobj})



def pgoverview(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            bookingtime = datetime.datetime.now()
            roomid = request.POST['roomid']
            userid = request.user.id
            payment = 1000
            stripe.api_key = settings.STRIPE_SECRET_KEY
        
            stripe_total = 100000
            userid = request.user.id

            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            customer = stripe.Customer.create(email=email,source=token)
            charge = stripe.Charge.create(amount=stripe_total,currency="inr",customer=customer.id)

            bookingobj = booking(booktime=bookingtime,roomid_id=roomid,userid_id=userid,payment=payment,paymentstatus=True)
            bookingobj.save();

            loteditobj = Room.objects.get(id=roomid)
            loteditobj.save();
            messages.info(request,'Succesfully Booked')
            return redirect('/')           

        else:   
            stripe.api_key = settings.STRIPE_SECRET_KEY
            data_key = settings.STRIPE_PUBLISHABLE_KEY
            stripe_total = 100000                
            room = request.GET.get('pg')
            pgobjs = Room.objects.get(id=room)  
            myuserid = pgobjs.userid_id
            usermobobj = extendeduser.objects.get(user=myuserid)
            return render(request,'pgoverview.html',{'pgobjs' : pgobjs,'usermobobj' : usermobobj,'data_key' : data_key, 'stripe_total' : stripe_total})
    else:
        messages.info(request,'Please Login to Continue')
        return redirect('login') 

def mybooking(request):
    if request.user.is_authenticated:
        userid = request.user.id
        bookobjs = booking.objects.filter(userid_id=userid).order_by('-id')
        return render(request,'mybooking.html',{'bookobjs' : bookobjs})        
    else:
        messages.info(request,'Please Login to Continue')
        return redirect('login')        

def unallocatedbooking(request):
    userid = request.user.id
    bookobjs = booking.objects.filter(bookingstatus=False,roomid__userid__id=userid)
    return render(request,'unallocatedbooking.html',{'bookobjs' : bookobjs}) 

def bookingconfirm(request):
    bookid = request.GET.get('book')
    booked = booking.objects.get(id = bookid)
    booked.bookingstatus = True
    booked.save();
    messages.info(request,'Bed Allocated and Booking Confirmed')
    return redirect('unallocatedbooking')

def allocatedbooking(request):
    userid = request.user.id
    bookobjs = booking.objects.filter(bookingstatus=True,roomid__userid__id=userid)
    return render(request,'allocatedbooking.html',{'bookobjs' : bookobjs})    

def cancelbooking(request):
    bookid = request.GET.get('cancel')
    roomid = request.GET.get('pg')
    userid = request.GET.get('user')
    cancelbooking = booking.objects.get(id = bookid)
    cancelbooking.cancelstatus = True
    cancelbooking.save();
    canceltime = datetime.datetime.now()
    cancelbook = cancelledbooking(cancelstatus=True,roomid_id=roomid,bookid_id=bookid,userid_id=userid,canceltime=canceltime)
    cancelbook.save();
    currentuser = request.user.id
    if currentuser == userid:
        messages.info(request,'Booking has been cancelled')
        return redirect('mybooking')   
    else:
        messages.info(request,'Booking has been cancelled')
        return redirect('/')   

def forcedcancel(request):
    bookid = request.GET.get('book')
    roomid = request.GET.get('pg')
    userid = request.GET.get('user')
    forcecancelbooking = booking.objects.get(id = bookid)
    forcecancelbooking.forcecancel = True
    forcecancelbooking.save();
    forcecancelbook = cancelledbooking(forcecancel=True,roomid_id=roomid,bookid_id=bookid,userid_id=userid)
    forcecancelbook.save();
    messages.info(request,'Booking has been cancelled')
    return redirect('cancelledbookings')   


def cancelledbookings(request):
    userid = request.user.id
    cancelobjs = cancelledbooking.objects.filter(roomid__userid__id=userid)
    return render(request,'cancelledbookings.html',{'cancelobjs' : cancelobjs}) 

def refundrequest(request):
    userid = request.user.id
    cancelobjs = cancelledbooking.objects.filter(cancelstatus=True,refundstatus=False,roomid__userid__id=userid)
    return render(request,'refundrequest.html',{'cancelobjs' : cancelobjs})    

def refund(request):
    bookid = request.GET.get('book')
    cancelid = request.GET.get('cancelid')
    refundbook = booking.objects.get(id = bookid)
    refundbook.refundstatus = True
    refundbook.refund = 1000
    refundbook.save();
    refundcancel = cancelledbooking.objects.get(id = cancelid)
    refundcancel.refundstatus = True
    refundcancel.refund = 1000
    refundcancel.save();
    messages.info(request,'Refund Successful!')
    return redirect('cancelledbookings')      

def ownerreports(request):
    return render(request,"ownerreports.html") 
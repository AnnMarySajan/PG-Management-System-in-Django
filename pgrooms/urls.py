from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("logout/",views.logout,name="logout"),
    path("forpgowners",views.forpgowners,name="forpgowners"),
    path("addnewpg",views.addnewpg,name="addnewpg"),
    path("yourpglist",views.yourpglist,name="yourpglist"),
    path("editlisting/",views.editlisting,name="editlisting"),
    path("emphome",views.emphome,name="emphome"),
    path('acceptrequest/',views.acceptrequest, name='acceptlisting'),
    path('commiting/',views.commiting, name='commiting'),
    path('verification',views.verification, name='verification'),
    path('unallot/',views.unallot, name='unallot'),
    path('verifing/',views.verifing, name='verifing'),
    path('verifing',views.verifing, name='verifing'),
    path('verifiedbyme',views.verifiedbyme, name='verifiedbyme'),
    path('pgoverview/',views.pgoverview, name='pgoverview'),
    path('pgoverview',views.pgoverview, name='pgoverview'),
    path('mybooking/',views.mybooking, name='mybooking'),
    path('mybooking',views.mybooking, name='mybooking'),
    path('unallocatedbooking',views.unallocatedbooking, name='unallocatedbooking'),
    path('unallocatedbooking/',views.unallocatedbooking, name='unallocatedbooking'),
    path('bookingconfirm/',views.bookingconfirm, name='bookingconfirm'),
    path('allocatedbooking',views.allocatedbooking, name='allocatedbooking'),
    path('allocatedbooking/',views.allocatedbooking, name='allocatedbooking'),
    path('cancelbooking',views.cancelbooking, name='cancelbooking'),
    path('cancelbooking/',views.cancelbooking, name='cancelbooking'),
    path('forcedcancel',views.forcedcancel, name='forcedcancel'),
    path('forcedcancel/',views.forcedcancel, name='forcedcancel'),
    path('cancelledbookings',views.cancelledbookings, name='cancelledbookings'),
    path('cancelledbookings/',views.cancelledbookings, name='cancelledbookings'),
    path('refundrequest',views.refundrequest, name='refundrequest'),
    path('refundrequest/',views.refundrequest, name='refundrequest'),
    path('refund',views.refund, name='refund'),
    path('refund/',views.refund, name='refund'),
    path('ownerreports',views.ownerreports, name='ownerreports'),
    path('ownerreports/',views.ownerreports, name='ownerreports'),
]
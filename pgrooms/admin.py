from django.contrib import admin
from django.contrib.admin import ModelAdmin,register
from .models import Room, State,City, booking, pgverification ,cancelledbooking,extendeduser,cancelledbooking,PGSummary,bookingSummary,cancelSummary
from django.db.models.aggregates import Avg,Sum
from django.db.models import Count,Avg
# Register your models here.

#admin.site.register(State)
#admin.site.register(City)
#admin.site.register(Room)
#admin.site.register(booking)
#admin.site.register(cancelledbooking)

@register(State)
class StateAdmin(ModelAdmin):
    list_display = ('id','statename')

@register(City)
class CityAdmin(ModelAdmin):
    list_display = ('id','statename','cityname')

@register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('id','pgname','get_name','get_userid','pgtype','statename','cityname','price','bedno','verifystatus','activestatus')
    list_filter = ('statename','cityname','activestatus','verifystatus')
    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.short_description = 'User ID'

@register(booking)
class bookingAdmin(ModelAdmin):
    list_display = ('id','booktime','roomid','get_name','get_userid','bookingstatus','cancelstatus','refundstatus','forcecancel')
    list_filter = ('roomid','booktime','bookingstatus','cancelstatus','refundstatus','forcecancel')
    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.short_description = 'User ID'    

@register(pgverification)
class pgverificationAdmin(ModelAdmin):
    list_display = ('id','roomid','get_name','get_verid','verifydate','allotedstatus')
    list_filter = ('allotedstatus','verifydate',)
    def get_name(self, obj):
        return obj.verifier.first_name
    get_name.admin_order_field  = 'verifier'  #Allows column order sorting
    get_name.short_description = 'Verifier Name'  #Renames column head
    def get_verid(self, obj):
        return obj.verifier.id
    get_verid.admin_order_field  = 'verifier'  #Allows column order sorting
    get_verid.short_description = 'Verifier ID'  #Renames column head

@register(extendeduser)
class extendeduserAdmin(ModelAdmin):
    list_display = ('get_userid','get_name','mobile')
    def get_name(self, obj):
        return obj.user.first_name
    get_name.admin_order_field  = 'user'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.user.id
    get_userid.admin_order_field  = 'user'  #Allows column order sorting
    get_userid.short_description = 'User ID'  #Renames column head

@register(cancelledbooking)
class cancelledbookingAdmin(ModelAdmin):
    list_display = ('id','roomid','get_name','get_userid','canceltime','cancelstatus','refundstatus','forcecancel')
    list_filter = ('roomid','canceltime','cancelstatus','refundstatus','forcecancel')
    def get_name(self, obj):
        return obj.userid.first_name
    get_name.admin_order_field  = 'userid'  #Allows column order sorting
    get_name.short_description = 'User Name'  #Renames column head
    def get_userid(self, obj):
        return obj.userid.id
    get_userid.short_description = 'User ID'  


@register(PGSummary)
class PGSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/pg_summary_change_list.html'
    list_filter = ('activestatus','cityname','statename')

    #date_hierarchy = 'created'
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'average_price': Avg('price'),
        }
        response.context_data['summary'] = list(
            qs
            .values('statename1','cityname1')
            .annotate(**metrics)
            .order_by('-total')
        )
        #return response

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response

@register(bookingSummary)
class bookingSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/booking_summary_change_list.html'
    list_filter = ('booktime','cancelstatus','roomid_id__statename','roomid_id__cityname')

    #date_hierarchy = 'created'
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'earning': Sum('payment'),
        }
        response.context_data['summary'] = list(
            qs
            .values('roomid')
            .annotate(**metrics)
            .order_by('-total','-earning')
        )
        #return response

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response


@register(cancelSummary)
class cancelSummaryAdmin(ModelAdmin):
    change_list_template = 'admin/cancelledbooking_summary_change_list.html'
    list_filter = ('canceltime','cancelstatus','roomid_id__statename','roomid_id__cityname')

    #date_hierarchy = 'created'
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'earning': Sum('refund'),
        }
        response.context_data['summary'] = list(
            qs
            .values('roomid')
            .annotate(**metrics)
            .order_by('-total','-earning')
        )
        #return response

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )
        return response



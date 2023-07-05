from django.contrib import admin
from .models import Patent, Account, Event
from django.contrib.auth.models import User

#------MODELS-IN-THE-ADMIN-PANEL----------------------------------------

# defines the Patent model's appearence in the admin panel
class PatentAdmin(admin.ModelAdmin):
    list_display = ['owner','id']
    ordering = ['pk']


class EventAdmin(admin.ModelAdmin):
    list_display = ['patentId', 'type', 'logs']
    ordering = ['_id']

# registers the models in the admin section
admin.site.register(Patent, PatentAdmin)
admin.site.register(Event, EventAdmin)


#------EXSTENSION-OF-THE-USER-MODEL-------------------------------------

# connects the Account Model to the admin panel
class InlineAccount(admin.StackedInline):
    model = Account

# re-defines the User model in the admin panel 
class UserAdmin(admin.ModelAdmin):

    def address(obj, user):
        return user.account.address
    
    def patents(obj, user):
        return user.account.patents
    
    inlines=[InlineAccount]
    list_display=['username', 'first_name', 'last_name', 'is_staff', 'address', 'patents']

# updates the registration of User and UserAdmin models
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

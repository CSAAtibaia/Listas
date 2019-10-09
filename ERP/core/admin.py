from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from ERP.core.models import CoAgri, Item, Partilha


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'estoque',
    )
    search_fields = ('produto',)

class CoAgriInline(admin.StackedInline):
    model = CoAgri

class UserAdmin(BaseUserAdmin):
    inlines = [CoAgriInline,
        ]
    #exclude = ('user_permissions',    )


admin.site.site_header = 'CSA Atibaia'
admin.site.site_title = 'CSA Atibaia'
admin.site.index_title = 'Admin'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Partilha)

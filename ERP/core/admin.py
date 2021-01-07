from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from ERP.core.models import CoAgri

''', Item, Fornecedor, Partilha


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'preco',
        'saldo',
    )
    search_fields = ('produto',)
    readonly_fields = ('saldo', )
'''

class CoAgriInline(admin.StackedInline):
    model = CoAgri


class UserAdmin(BaseUserAdmin):
    inlines = [CoAgriInline,
        ]
    list_display = (
        'first_name',
        'last_name',
        'username',
        'cota',
        'status'
        )
    def cota(self):
            return ("%s" % (self.CoAgri.cota))
        
    def status(self):
            return ("%s" % (self.CoAgri.status))
    
    status.short_description = 'Status'
    cota.short_description = 'Cota'


admin.site.site_header = 'CSA Atibaia'
admin.site.site_title = 'CSA Atibaia'
admin.site.index_title = 'Admin'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

'''admin.site.register(Item, ItemAdmin)
admin.site.register(Partilha)
admin.site.register(Fornecedor)'''

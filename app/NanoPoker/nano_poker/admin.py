from django.contrib import admin


from .models import Account


class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)

admin.site.site_header = "Nano Poker"
admin.site.index_title = "Nano Poker"
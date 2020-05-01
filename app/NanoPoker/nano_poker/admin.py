from django.contrib import admin


from .models import Account
from .models import Transaction
from .models import GameState
from .models import Action


class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class GameStateAdmin(admin.ModelAdmin):
    pass
admin.site.register(GameState, GameStateAdmin)

class ActionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Action, ActionAdmin)

admin.site.site_header = "Nano Poker"
admin.site.index_title = "Nano Poker"
from django.contrib import admin
from .models import LottoRound, LottoTicket, Winnings


@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = (
        'round_number',
        'draw_date',
        'is_drawn'
    )


@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'round',
        'numbers',
        'is_auto',
        'purchase_date'
    )


@admin.register(Winnings)
class WinningsAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'rank',
        'prize_amount'
    )

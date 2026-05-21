from django.db import models
from django.contrib.auth.models import User


# 로또 회차
class LottoRound(models.Model):
    round_number = models.PositiveIntegerField(unique=True)
    draw_date = models.DateTimeField()

    winning_numbers = models.JSONField(
        null=True,
        blank=True
    )

    is_drawn = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.round_number}회차"


# 구매 티켓
class LottoTicket(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    round = models.ForeignKey(
        LottoRound,
        on_delete=models.CASCADE
    )

    numbers = models.JSONField()

    is_auto = models.BooleanField(default=False)

    purchase_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.owner.username} - {self.round.round_number}회차"


# 당첨 내역
class Winnings(models.Model):
    ticket = models.OneToOneField(
        LottoTicket,
        on_delete=models.CASCADE
    )

    rank = models.PositiveIntegerField()

    prize_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    def __str__(self):
        return f"{self.ticket} - {self.rank}등"

import random

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone

from .models import LottoRound, LottoTicket, Winnings

# 메인 화면
def home(request):
    
    current_round = LottoRound.objects.order_by(
        '-round_number'
    ).first()

    return render(
        request,
        'lotto/home.html',
        {
            'current_round': current_round
        }
    )


# 자동 번호 구매
def auto_lotto(request):

    numbers = random.sample(range(1, 46), 6)

    numbers.sort()

    current_round = LottoRound.objects.order_by(
        '-round_number'
    ).first()

    user = User.objects.first()

    LottoTicket.objects.create(
        owner=user,
        round=current_round,
        numbers=numbers,
        is_auto=True
    )

    return render(
        request,
        'lotto/result.html',
        {
            'numbers': numbers,
            'mode': '자동'
        }
)

# 수동 번호 구매
def manual_lotto(request):

    if request.method == 'POST':

        numbers = [
            int(request.POST.get('num1')),
            int(request.POST.get('num2')),
            int(request.POST.get('num3')),
            int(request.POST.get('num4')),
            int(request.POST.get('num5')),
            int(request.POST.get('num6')),
        ]

        numbers.sort()

        current_round = LottoRound.objects.order_by(
        '-round_number'
        ).first()

        user = User.objects.first()

        LottoTicket.objects.create(
            owner=user,
            round=current_round,
            numbers=numbers,
            is_auto=False
        )

        return render(
            request,
            'lotto/result.html',
            {
                'numbers': numbers,
                'mode': '수동'
            }
        )

    return render(
        request,
        'lotto/manual.html'
    )

# 당첨 번호 추첨
def draw_lotto(request):

    current_round = LottoRound.objects.order_by(
    '-round_number'
    ).first()

    winning_numbers = random.sample(range(1, 46), 6)

    winning_numbers.sort()

    current_round.winning_numbers = winning_numbers

    current_round.is_drawn = True

    current_round.save()

    tickets = LottoTicket.objects.filter(
        round=current_round
    )

    for ticket in tickets:

        match_count = len(
            set(ticket.numbers) &
            set(winning_numbers)
        )

        rank = 0

        prize = 0

        if match_count == 6:
            rank = 1
            prize = 3000000000

        elif match_count == 5:
            rank = 2
            prize = 50000000

        elif match_count == 4:
            rank = 3
            prize = 1000000

        elif match_count == 3:
            rank = 4
            prize = 50000

        if rank > 0:

            Winnings.objects.create(
                ticket=ticket,
                rank=rank,
                prize_amount=prize
            )
    # 다음 회차 생성
    LottoRound.objects.create(
        round_number=current_round.round_number + 1,
        draw_date=timezone.now()
    )

    return render(
        request,
        'lotto/draw_result.html',
        {
            'winning_numbers': winning_numbers
        }
    )

# 당첨 내역 조회
def winnings_list(request):

    winnings = Winnings.objects.all()

    return render(
        request,
        'lotto/winnings.html',
        {
            'winnings': winnings
        }
    )

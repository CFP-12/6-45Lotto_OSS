import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LottoRound, Ticket


# Create your views here.

@login_required
def purchase_ticket(request):
    current_round = LottoRound.objects.order_range = LottoRound.objects.filter(is_drawn=False).last()

    if not current_round:
        current_round = LottoRound.objects.all().last()
    
    if not current_round:
        messages.error(request, "현재 진행중인 로또 회차가 없습니다. 관리자에게 문의하세요.")
        return render(request, 'lotto/purchase.html')
    
    if request.method == 'POST':
        selection_type = request.POST.get('selection_type')

        if selection_type == 'AUTO':
            auto_numbers = sorted(random.sample(range(1, 46), 6))
            numbers = auto_numbers
        else:
            try:
                manual_numbers = [
                    int(request.POST.get('num1')),
                    int(request.POST.get('num2')),
                    int(request.POST.get('num3')),
                    int(request.POST.get('num4')),
                    int(request.POST.get('num5')),
                    int(request.POST.get('num6')),
                ]

                if any(n < 1 or n > 45 for n in manual_numbers):
                    raise ValueError("번호는 1부터 45 사이여야 합니다.")
                if len(set(manual_numbers)) != 6:
                    raise ValueError("중복된 번호가 있습니다.")
                
                numbers = sorted(manual_numbers)
            except (ValueError, TypeError) as e:
                messages.error(request, f"번호 입력이 올바르지 않습니다: {e}")
                return redirect('purchase_ticket')
        
        Ticket.objects.create(
            user=request.user,
            round_instance=current_round,
            selection_type=selection_type,
            num1=numbers[0],
            num2=numbers[1],
            num3=numbers[2],
            num4=numbers[3],
            num5=numbers[4],
            num6=numbers[5],
        )
        messages.success(request, f"로또 {current_round.round_number}회차 [{selection_type}] 티켓이 구매되었습니다.")
        return redirect('purchase_ticket')
    
    return render(request, 'lotto/purchase.html', {'current_round': current_round})
from django.db import models
from django.contrib.auth.models import User

class LottoRound(models.Model):
    round_number = models.PositiveIntegerField(unique=True, verbose_name="회차")
    draw_date = models.DateTimeField(auto_now_add=True, verbose_name="추첨 날짜")

    num1 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 1")
    num2 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 2")
    num3 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 3")
    num4 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 4")
    num5 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 5")
    num6 = models.PositiveIntegerField(null=True, blank=True, verbose_name="번호 6")
    bonus_num = models.PositiveIntegerField(null=True, blank=True, verbose_name="보너스 번호")

    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")

    def __str__(self):
        return f"제 {self.round_number}회 로또 추첨"
    
    def settle_tickets(self):
        if not self.is_drawn:
            return  # 추첨이 완료되지 않은 경우 처리하지 않음

        from .utils import check_lotto_rank

        winning_numbers = {self.num1, self.num2, self.num3, self.num4, self.num5, self.num6}
        bonus_number = self.bonus_num
        tickets = self.tickets.all()

        for ticket in tickets:
            ticket_nums = ticket.get_numbers()
            rank = check_lotto_rank(ticket_nums, winning_numbers, bonus_number)
            ticket.rank = rank
            ticket.save()
    

class Ticket(models.Model):
    SELECTION_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", verbose_name="구매자")
    round_instance = models.ForeignKey(LottoRound, on_delete=models.CASCADE, related_name="tickets", verbose_name="회차")

    selection_type = models.CharField(max_length=6, choices=SELECTION_CHOICES, verbose_name="선택 유형")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="구매 날짜")

    num1 = models.PositiveIntegerField(verbose_name="번호 1")
    num2 = models.PositiveIntegerField(verbose_name="번호 2")
    num3 = models.PositiveIntegerField(verbose_name="번호 3")
    num4 = models.PositiveIntegerField(verbose_name="번호 4")
    num5 = models.PositiveIntegerField(verbose_name="번호 5")
    num6 = models.PositiveIntegerField(verbose_name="번호 6")

    rank = models.PositiveIntegerField(null=True, blank=True, verbose_name="당첨 등수")
    is_checked = models.BooleanField(default=False, verbose_name="당첨 여부 확인")

    def __str__(self):
        return f"{self.user.username} - 제 {self.round_instance.round_number}회 티켓 [{self.selection_type}]"
    
    def get_numbers(self):
        return {self.num1, self.num2, self.num3, self.num4, self.num5, self.num6}
# Create your models here.

from django.contrib import admin
from .models import LottoRound, Ticket

@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'draw_date', 'is_drawn', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus_num')
    list_filter = ('is_drawn',)
    ordering = ('-round_number',)

    def save_model(self, request, obj, form, change):
        if obj.num1 and obj.num2 and obj.num3 and obj.num4 and obj.num5 and obj.num6 and obj.bonus_num:
            obj.is_drawn = True

        super().save_model(request, obj, form, change)

        if obj.is_drawn:
            obj.settle_tickets()  # 추첨이 완료된 경우 티켓 정산 메서드 호출

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'round_instance', 'selection_type', 'purchased_at', 'rank')
    list_filter = ('round_instance', 'selection_type', 'is_checked')
    search_fields = ('user__username',)
    ordering = ('-purchased_at',)

    def get_numbers_display(self, obj):
        return f"{obj.num1}, {obj.num2}, {obj.num3}, {obj.num4}, {obj.num5}, {obj.num6}"
    get_numbers_display.short_description = '선택 번호'
# Register your models here.

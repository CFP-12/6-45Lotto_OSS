def check_lotto_rank(ticket_numbers, winning_numbers, bonus_number):
    matched_count = len(set(ticket_numbers) & set(winning_numbers))
    has_bonus = bonus_number in ticket_numbers

    if matched_count == 6:
        return 1  # 1등
    elif matched_count == 5 and has_bonus:
        return 2  # 2등
    elif matched_count == 5:
        return 3  # 3등
    elif matched_count == 4:
        return 4  # 4등
    elif matched_count == 3:
        return 5  # 5등
    else:
        return None  # 낙첨
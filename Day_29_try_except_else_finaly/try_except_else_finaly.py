def c_withdraw(balance, amount):
    if amount > balance:
        return None, "잔액 부족" # 오류 메시지를 함께 반환
    return balance - amount, "성공"

def b_buy_item(cash, item_price):
    new_balance, msg = c_withdraw(cash, item_price)
    if new_balance is None:
        # 오류를 다시 상위로 전달... 매우 번거롭다.
        return None, msg 
    return new_balance, "구매 성공"

def a_start_shopping():
    final_result, final_msg = b_buy_item(50000, 100000)
    if final_result is None:
        # 맨 위에서야 겨우 오류를 처리한다.
        print(f"쇼핑 실패! 이유: {final_msg}")

a_start_shopping()
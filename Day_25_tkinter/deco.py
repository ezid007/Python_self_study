def check_if_admin(func):
    """사용자가 관리자인지 확인하고, 관리자일 때만 함수를 실행하는 데코레이터"""
    def wrapper(*args, **kwargs):
        """
        실제 애플리케이션에서는 여기서 사용자의 권한을 확인합니다.
        is_admin = get_user_role() == 'admin'
        """
        is_admin = False # 예시를 위해 True로 설정

        if is_admin:
            print("관리자 확인! 함수를 실행합니다.")
            return func(*args, **kwargs) # 조건이 맞으면 원본 함수 실행
        else:
            print("경고: 관리자만 접근할 수 있습니다.")
            return None # 조건이 안 맞으면 원본 함수를 무시하고 종료
    return wrapper

@check_if_admin
def delete_user(user_id):
    """사용자를 삭제하는 민감한 함수"""
    print(f"{user_id} 사용자를 삭제했습니다.")

delete_user("test_user")
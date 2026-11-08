def show_menu():
    """메뉴 화면을 출력한다."""
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def input_number(prompt, low, high):
    """low~high 범위의 정수를 입력받을 때까지 반복한다."""
    while True:
        raw = input(prompt).strip()          # 앞뒤 공백 제거
        if raw == "":                         # 빈 입력
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(raw)                 # 숫자 변환
        except ValueError:                    # 'abc' 같은 입력
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if number < low or number > high:     # 범위 밖
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def main():
    while True:
        show_menu()
        choice = input_number("선택: ", 1, 5)
        if choice == 1:
            print("🚧 퀴즈 풀기 (준비 중)")
        elif choice == 2:
            print("🚧 퀴즈 추가 (준비 중)")
        elif choice == 3:
            print("🚧 퀴즈 목록 (준비 중)")
        elif choice == 4:
            print("🚧 점수 확인 (준비 중)")
        else:
            print("👋 프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()

from default_data import get_default_quizzes
from quiz import Quiz


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


def input_text(prompt):
    """빈 문자열이 아닌 텍스트를 입력받을 때까지 반복한다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 내용이 비어 있습니다. 다시 입력하세요.")
            continue
        return text


def add_quiz(quizzes):
    """사용자에게 문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.\n")
    question = input_text("문제를 입력하세요: ")

    choices = []
    for number in range(1, Quiz.CHOICE_COUNT + 1):
        choices.append(input_text(f"선택지 {number}: "))

    answer = input_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

    quizzes.append(Quiz(question, choices, answer))
    print(f"\n✅ 퀴즈가 추가되었습니다! (현재 {len(quizzes)}개)\n")


def list_quizzes(quizzes):
    """등록된 퀴즈의 문제 목록을 번호와 함께 출력한다."""
    if not quizzes:
        print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)\n")
    print("-" * 40)
    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")
    print("-" * 40)


def play_quiz(quizzes):
    """퀴즈를 순서대로 출제하고, 맞힌 개수를 반환한다.

    퀴즈가 없으면 안내 후 None을 반환한다.
    """
    if not quizzes:
        print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return None

    total = len(quizzes)
    correct_count = 0
    print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

    for number, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        quiz.display(number)
        user_answer = input_number("정답 입력: ", 1, 4)
        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!\n")
            correct_count += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

    score = round(correct_count / total * 100)
    print("=" * 40)
    print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
    return {"score": score, "correct": correct_count, "total": total}


def update_best_score(best, result):
    """이번 결과(result)를 최고 기록(best)과 비교해, 더 높으면 새 기록을 반환한다."""
    if best is None or result["score"] > best["score"]:
        print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)
        return result
    print(f"(최고 점수: {best['score']}점)")
    print("=" * 40)
    return best


def show_score(best):
    """최고 점수를 출력한다. 아직 기록이 없으면 안내한다."""
    if best is None:
        print("📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어 보세요!")
        return
    print(
        f"\n🏆 최고 점수: {best['score']}점 "
        f"({best['total']}문제 중 {best['correct']}문제 정답)\n"
    )


def main():
    quizzes = get_default_quizzes()
    best = None  # 최고 기록: {"score": 점수, "correct": 맞힌 수, "total": 문제 수}
    while True:
        show_menu()
        choice = input_number("선택: ", 1, 5)
        if choice == 1:
            result = play_quiz(quizzes)
            if result is not None:
                best = update_best_score(best, result)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            list_quizzes(quizzes)
        elif choice == 4:
            show_score(best)
        else:
            print("👋 프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()

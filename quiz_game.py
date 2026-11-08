import json
import os

from default_data import get_default_quizzes
from quiz import Quiz

# 데이터 파일: 프로젝트 루트(이 파일과 같은 폴더)의 state.json
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체(메뉴, 풀기, 추가, 목록, 점수, 저장)를 관리하는 클래스."""

    MENU_COUNT = 5

    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.quizzes = []  # Quiz 객체 리스트
        self.best = None  # 최고 기록: {"score": 점수, "correct": 맞힌 수, "total": 문제 수}

    # ---------- 파일 저장/불러오기 ----------
    def load(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다.

        - 파일이 없으면: 기본 퀴즈로 시작하고 새 파일을 만든다.
        - 파일이 손상되었으면: 안내 후 기본 퀴즈로 복구한다.
        """
        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best = self._parse_best(data)
        except FileNotFoundError:
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self._reset_to_default()
            return
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, ValueError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self._reset_to_default()
            return
        except OSError as error:
            print(f"⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. ({error})")
            self.quizzes = get_default_quizzes()
            self.best = None
            return

        best_text = f"{self.best['score']}점" if self.best else "기록 없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

    def save(self):
        """현재 퀴즈와 최고 점수를 state.json에 저장한다. 성공하면 True를 반환한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best["score"] if self.best else None,
            "best_correct": self.best["correct"] if self.best else None,
            "best_total": self.best["total"] if self.best else None,
        }
        temp_file = self.state_file + ".tmp"
        try:
            # 임시 파일에 먼저 쓰고 교체해서, 저장 도중 멈춰도 원본이 깨지지 않게 한다.
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            os.replace(temp_file, self.state_file)
            return True
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다. ({error})")
            return False

    def _reset_to_default(self):
        """기본 퀴즈로 초기화하고 파일에 저장한다."""
        self.quizzes = get_default_quizzes()
        self.best = None
        self.save()

    @staticmethod
    def _parse_best(data):
        """JSON 데이터에서 최고 기록을 읽는다. 기록이 없으면 None."""
        score = data.get("best_score")
        if score is None:
            return None
        correct = data.get("best_correct")
        total = data.get("best_total")
        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in (score, correct, total)):
            raise ValueError("최고 점수 형식이 올바르지 않습니다.")
        return {"score": score, "correct": correct, "total": total}

    # ---------- 게임 진행 ----------
    def run(self):
        """데이터를 불러온 뒤 메뉴를 반복해서 보여 주고, 선택한 기능을 실행한다."""
        self.load()
        while True:
            self.show_menu()
            choice = self.input_number("선택: ", 1, self.MENU_COUNT)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                print("👋 프로그램을 종료합니다.")
                break

    def show_menu(self):
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

    # ---------- 입력 처리 ----------
    def input_number(self, prompt, low, high):
        """low~high 범위의 정수를 입력받을 때까지 반복한다."""
        while True:
            raw = input(prompt).strip()  # 앞뒤 공백 제거
            if raw == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue
            try:
                number = int(raw)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue
            if number < low or number > high:
                print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue
            return number

    def input_text(self, prompt):
        """빈 문자열이 아닌 텍스트를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 내용이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    # ---------- 기능 ----------
    def play_quiz(self):
        """퀴즈를 순서대로 출제하고 결과와 최고 점수를 처리한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            user_answer = self.input_number("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = round(correct_count / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        self.update_best_score({"score": score, "correct": correct_count, "total": total})
        print("=" * 40)
        print()

    def update_best_score(self, result):
        """이번 결과를 최고 기록과 비교해, 더 높으면 갱신하고 저장한다."""
        if self.best is None or result["score"] > self.best["score"]:
            self.best = result
            print("🎉 새로운 최고 점수입니다!")
            self.save()
        else:
            print(f"(최고 점수: {self.best['score']}점)")

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.input_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, Quiz.CHOICE_COUNT + 1):
            choices.append(self.input_text(f"선택지 {number}: "))

        answer = self.input_number(
            f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT
        )

        self.quizzes.append(Quiz(question, choices, answer))
        if self.save():
            print(f"\n✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)\n")
        else:
            print(f"\n⚠️ 퀴즈는 추가되었지만 파일에 저장하지 못했습니다. (현재 {len(self.quizzes)}개)\n")

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        """최고 점수를 출력한다. 아직 기록이 없으면 안내한다."""
        if self.best is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어 보세요!")
            return
        print(
            f"\n🏆 최고 점수: {self.best['score']}점 "
            f"({self.best['total']}문제 중 {self.best['correct']}문제 정답)\n"
        )

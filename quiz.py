class Quiz:
    """퀴즈 한 문제를 표현하는 클래스."""

    CHOICE_COUNT = 4  # 선택지 개수 (정답 번호는 1~4)

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 함께 문제와 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 반환한다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """dict(JSON에서 읽은 데이터)로부터 Quiz 객체를 만든다.

        형식이 올바르지 않으면 ValueError를 발생시킨다.
        """
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제가 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != cls.CHOICE_COUNT:
            raise ValueError("선택지는 4개여야 합니다.")
        if not all(isinstance(choice, str) for choice in choices):
            raise ValueError("선택지는 문자열이어야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답 번호는 정수여야 합니다.")
        if not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")
        return cls(question, choices, answer)

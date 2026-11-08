from quiz import Quiz


def get_default_quizzes():
    """기본 퀴즈 목록을 Quiz 객체 리스트로 만들어 반환한다.

    주제: 컴퓨터 & 프로그래밍 기초 상식
    (state.json이 없거나 손상되었을 때 이 데이터로 시작한다.)
    """
    return [
        Quiz(
            "Python 언어를 만든 사람은?",
            ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "데니스 리치"],
            1,
        ),
        Quiz(
            "1바이트(Byte)는 몇 비트(bit)일까?",
            ["4비트", "8비트", "16비트", "32비트"],
            2,
        ),
        Quiz(
            "컴퓨터의 '두뇌'로, 명령어를 해석하고 실행하는 장치는?",
            ["RAM", "SSD", "CPU", "모니터"],
            3,
        ),
        Quiz(
            "Python에서 한 번 만들면 값을 바꿀 수 없는(immutable) 자료형은?",
            ["list", "dict", "set", "tuple"],
            4,
        ),
        Quiz(
            "원격 저장소의 변경 사항을 가져와 내 로컬에 합치는 Git 명령어는?",
            ["git push", "git pull", "git commit", "git init"],
            2,
        ),
        Quiz(
            "Git을 처음 만든 사람은? (리눅스 커널 개발자이기도 함)",
            ["빌 게이츠", "스티브 잡스", "리누스 토르발스", "귀도 반 로섬"],
            3,
        ),
        Quiz(
            "웹 페이지 주소를 잘못 입력했을 때 자주 보는 'Not Found' 오류 코드는?",
            ["200", "301", "404", "500"],
            3,
        ),
        Quiz(
            "데이터 저장에 많이 쓰이는 형식 JSON은 무엇의 약자일까?",
            [
                "JavaScript Object Notation",
                "Java Standard Object Network",
                "JSON Simple Output Name",
                "Joint System Object Number",
            ],
            1,
        ),
    ]

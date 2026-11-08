from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 스트림 종료(Ctrl+Z / Ctrl+D)가 와도 비정상 종료하지 않는다.
        print("\n\n⚠️ 종료 신호를 받았습니다. 데이터를 저장하고 안전하게 종료합니다.")
        if game.is_loaded and game.save():
            print("💾 저장 완료.")
        print("👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()

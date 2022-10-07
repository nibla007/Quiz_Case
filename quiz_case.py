from questions import quizzes


def check_answer(user_input, answers):
    user_choice = answers[user_input - 1]
    the_correct_answer = "not found"
    for answer in answers:
        if answer.get("correct"):
            the_correct_answer = answer.get("answer")

    if user_choice.get("correct"):
        return "Correct!\n", 1
    return f"Wrong! Correct answer is: {the_correct_answer}\n", 0


def quiz_program():
    score = 0
    for quiz in quizzes:
        for question in quiz.get("questions"):
            prompt = question.get("prompt")
            question_id = question.get("id")
            print(f"Question {question_id}. {prompt}")

            for count, answers in enumerate(question.get("answers"), start=1):
                answer = answers.get("answer")
                print(f"{count}. {answer}")
            user_input = int(input("Your answer: "))
            result, point = check_answer(user_input, question.get("answers"))
            print(result)
            score += point

    print(f"\n***RESULTS***\nYou got {score} correct out of {len(quizzes[0].get('questions'))} possible")


def main():
    quiz_program()


if __name__ == '__main__':
    main()

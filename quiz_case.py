import requests
import random


def check_answer(user_input, answers):
    user_choice = answers[user_input - 1]
    all_answers = []
    for answer in answers:
        if answer.get("correct"):
            all_answers.append(answer.get("answer"))

    the_correct_answers = ' eller '.join(all_answers)

    if user_choice.get("correct"):
        return "Rätt!\n", 1, the_correct_answers
    return f"Fel! Rätt svar är: {the_correct_answers}\n", 0, the_correct_answers


def save_wrong_answers(f, s):
    return f, s

# fixa svars nummer


def quiz_program():
    wrong_answers = []
    url = "https://bjornkjellgren.se/quiz/v1/questions"
    r = requests.get(url)
    r_dict = r.json()
    all_questions = r_dict.get("questions")
    random_questions = random.sample(all_questions, k=len(all_questions))[:10]
    score = 0
    user_input = None

    for question_id, question in enumerate(random_questions, start=1):
        prompt = question.get("prompt")
        print(f"Slumpar fram 10 av {len(all_questions)} frågor.\n")
        print(f"Fråga {question_id}. {prompt}")

        all_answers = question.get("answers")
        random.shuffle(all_answers)

        for count, answer in enumerate(all_answers, start=1):
            print(f"{count}. {answer['answer']}")
        while True:
            try:
                user_input = int(input("\nDitt svar: "))
            except ValueError:
                print("Ogiltigt värde")
                continue
            if 1 <= user_input <= len(all_answers):
                break
            else:
                print(f'\nOgiltigt svar, svara med 1 till {len(all_answers)}')

        result, point, correct_answers = check_answer(user_input, all_answers)
        if point == 0:
            wrong_answers.append(save_wrong_answers(prompt, correct_answers))
        print(result)
        score += point

    print(f"\n***RESULTAT***\nDu fick {score} rätt av {len(random_questions)} möjliga")
    if wrong_answers:
        print(f"Du svarade fel på dessa frågor:")
        for question, answer in wrong_answers:
            print(f"-{question}")
            print(f"Rätt svar: {answer}")


def main():
    quiz_program()


if __name__ == '__main__':
    main()

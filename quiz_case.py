import requests
from random import sample, shuffle
import json

url = "https://bjornkjellgren.se/quiz/v2/questions"


def main():
    """This is where the main program is run"""
    wrong_answers = []
    all_questions, random_questions = handle_api()
    score = 0
    user_input: int | None = None
    print(f"Slumpar fram {len(random_questions)} av {len(all_questions)} frågor.\n")
    score = quiz(random_questions, score, user_input, wrong_answers)
    print(f"\n***RESULTAT***\nDu fick {score} rätt av {len(random_questions)} möjliga")
    game_results(wrong_answers)


def handle_api():
    """Retrieves data from the API and fetches 10 randomized questions"""
    r = requests.get(url)
    r_dict: dict[str, list[dict[str, str | list[dict[str, str]]]]] = r.json()
    all_questions = r_dict.get("questions")
    random_questions: list[dict[str, str | list[dict[str, str]]]] = sample(all_questions, k=len(all_questions))[:10]
    return all_questions, random_questions


def quiz(random_questions, score, user_input, wrong_answers):
    """Here the quiz itself is run and statistics are printed to the user"""
    for question_id, question in enumerate(random_questions, start=1):
        prompt, times_asked, times_correct = extract_question_info(question)
        print(f"Fråga {question_id}.[{int(procent(times_correct, times_asked))}% har svarat rätt]\n{prompt}")
        all_answers = print_random_answers(question)
        user_input = validate_input(all_answers, user_input)
        result, point, correct_answers, correct_bool = check_answer(user_input, all_answers)
        post_data(question.get("id"), correct_bool)
        if not correct_bool:
            wrong_answers.append((prompt, correct_answers))
        print(result)
        score += point
    return score


def extract_question_info(question):
    """Retrieves the question and its statistics"""
    prompt: str = question.get("prompt")
    times_asked = int(question['times_asked'])
    times_correct = int(question['times_correct'])
    return prompt, times_asked, times_correct


def procent(a, b):
    """Converts question statistics to percentage form"""
    if b == 0:
        return 0
    return 100 * a / b


def print_random_answers(question):
    """Retrieves all possible answers then shuffles and prints them"""
    all_answers: list[dict[str, str]] = question.get("answers", [])
    shuffle(all_answers)
    for count, answer in enumerate(all_answers, start=1):
        print(f"{count}. {answer['answer']}")
    return all_answers


def validate_input(all_answers, user_input):
    """Validates the user's input for errors"""
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
    return user_input


def check_answer(user_input, answers):
    """Checks the user input, compares it to the correct answer and calculates points
     Also saves questions the user answered incorrectly in a list"""
    user_choice = answers[user_input - 1]
    all_answers = []
    for answer in answers:
        if answer.get("correct"):
            all_answers.append(answer.get("answer"))
    the_correct_answers = ' eller '.join(all_answers)
    if user_choice.get("correct"):
        return "Rätt!\n", 1, the_correct_answers, True
    return f"Fel! Rätt svar är: {the_correct_answers}\n", 0, the_correct_answers, False


def post_data(i, c):
    """Updates the API with the results"""
    payload = json.dumps({"id": i, "correct": c})
    requests.post(url, data=payload)


def game_results(wrong_answers):
    """Prints questions the user answered incorrectly as well as the correct answer"""
    if wrong_answers:
        print(f"Du svarade fel på dessa frågor:")
        for question, answer in wrong_answers:
            print(f"-{question}")
            print(f"Rätt svar: {answer}")


if __name__ == '__main__':
    main()

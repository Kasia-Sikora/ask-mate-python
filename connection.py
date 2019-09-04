import csv

QUESTION_HEADER = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions():
    user_questions = []
    with open("sample_data/question.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row = dict(row)
            user_questions.append(row)
    return user_questions


def get_all_answers():
    user_answers = []
    with open("sample_data/answer.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row = dict(row)
            user_answers.append(row)
    return user_answers


def save_all_questions(user_question):
    user_questions = get_all_questions()
    with open("sample_data/answer.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for question in user_questions:
            writer.writerow(question)
        if len(user_questions) == 0:
            question['id'] = 0
        else:
            question['id'] = int(user_questions[-1]['id']) + 1
        writer.writerow(user_question)


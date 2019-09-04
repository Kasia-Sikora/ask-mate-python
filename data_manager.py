import connection


def search_for_question(question_id):
    user_questions = connection.get_all_questions()
    for question in user_questions:
        if str(question_id) == question["id"]:
            question = change_view_number(question)
            return question


def search_for_all_answers(answer_id):
    list_of_answers = []
    user_answers = connection.get_all_answers()
    for answer in user_answers:
        if str(answer_id) == answer["question_id"]:
            list_of_answers.append(answer)
    return list_of_answers


def change_view_number(question):
    view = int(question['view_number']) + 1
    question['view_number'] = view
    return question

import connection



def search_for_question(question_id):
    user_questions = connection.get_all_questions()
    for i, question in enumerate(user_questions):
        if str(question_id) == question["id"]:
            question = change_view_number(question)
            user_questions[i] = question
            break
    connection.update_questions(user_questions)
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


def change_question_vote_number(id, vote_value):
    user_questions = connection.get_all_questions()
    for question in user_questions:
        if str(id) == question['id']:
            vote = int(question['vote_number']) + vote_value
            question['vote_number'] = vote
            break
    connection.update_questions(user_questions)
    return question


def change_answer_vote_number(id, vote_value):
    user_answers = connection.get_all_answers()
    for answer in user_answers:
        if str(id) == answer['id']:
            vote = int(answer['vote_number']) + vote_value
            answer['vote_number'] = vote
            break
    connection.update_answers(user_answers)
    return answer

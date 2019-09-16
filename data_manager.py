import connection


@connection.connection_handler
def search_for_question(cursor, quest_id):
    cursor.execute(""" SELECT submission_time, view_number, vote_number, title, message, image
                    FROM question 
                    WHERE id = %(id)s""", {'id': quest_id})
    question = cursor.fetchall()
    return question


def search_for_all_answers(cursor, quest_id):
    cursor.execute(""" SELECT submission_time, vote_number, message, image
                    FROM answer 
                    WHERE question_id = %(id)s""", {'id': quest_id})
    question = cursor.fetchall()
    return question

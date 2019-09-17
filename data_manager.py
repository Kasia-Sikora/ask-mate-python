import connection


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
                SELECT * FROM question ORDER BY submission_time;
                ''', )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def save_question(cursor, questions):
    cursor.execute('''
                    INSERT INTO question (submission_time, title, message) 
                    VALUES (CURRENT_TIMESTAMP, %(title)s, %(message)s);
                    SELECT * FROM question WHERE title= %(title)s AND message= %(message)s;
                    ''', questions)
    question = cursor.fetchall()
    return question


@connection.connection_handler
def search_for_question(cursor, quest_id):
    cursor.execute(""" SELECT id, submission_time, vote_number, title, message, image
                    FROM question 
                    WHERE id = %(ids)s""", {'ids': quest_id})
    question = cursor.fetchall()
    question = question[0]
    return question


@connection.connection_handler
def search_for_all_answers(cursor, quest_id):
    cursor.execute(""" SELECT submission_time, vote_number, message, image
                    FROM answer 
                    WHERE question_id = %(id)s""", {'id': quest_id})
    question = cursor.fetchall()
    return question

@connection.connection_handler
def new_answer(cursor, answer_dict):
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message) VALUES (CURRENT_TIMESTAMP, %(question_id)s, %(message)s);
                        SELECT * FROM question WHERE id = %(question_id)s""", answer_dict)
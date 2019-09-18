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
    cursor.execute(""" SELECT id, submission_time, vote_number, message, image
                    FROM answer 
                    WHERE question_id = %(id)s ORDER BY submission_time DESC""", {'id': quest_id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def new_answer(cursor, answer_dict):
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message) VALUES (CURRENT_TIMESTAMP, %(question_id)s, %(message)s);
                        SELECT * FROM question WHERE id = %(question_id)s""", answer_dict)
    question = cursor.fetchall()
    return question


@connection.connection_handler
def change_answer_vote(cursor, dictionary):
    cursor.execute(""" UPDATE answer 
                        SET vote_number = vote_number + %(vote)s 
                        WHERE id = %(id_answer)s""",
                   dictionary)


@connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""SELECT id, submission_time, vote_number, question_id, message, image FROM answer WHERE id = %(answer_id)s;
    """, {'answer_id': answer_id})
    answer_details = cursor.fetchall()
    answer_details = dict(answer_details[0])
    return answer_details


@connection.connection_handler
def update_answer(cursor, answer_dict):
    cursor.execute("""UPDATE answer SET message = %(message)s WHERE id = %(answer_id)s;""", answer_dict)
    cursor.execute("""SELECT question_id FROM answer WHERE id = %(answer_id)s;""", answer_dict)
    question_id = cursor.fetchall()
    question_id = dict(question_id[0])
    return question_id

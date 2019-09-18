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
    cursor.execute(""" SELECT id, submission_time, view_number, vote_number, title, message, image
                    FROM question 
                    WHERE id = %(ids)s""", {'ids': quest_id})
    question = cursor.fetchall()
    question = change_view_number(quest_id)
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
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message) 
                        VALUES (CURRENT_TIMESTAMP, %(question_id)s, %(message)s);
                        SELECT * FROM question WHERE id = %(question_id)s""", answer_dict)
    question = cursor.fetchall()
    return question


@connection.connection_handler
def change_view_number(cursor, question):
    cursor.execute("""UPDATE question SET view_number = view_number+1
                        WHERE id=%(id)s;
                        SELECT id, submission_time, view_number, vote_number, title, message, image
                        FROM question 
                        WHERE id = %(id)s """, {'id': question})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_all_question_comments(cursor, question_id):
    cursor.execute('''
                SELECT * FROM comment WHERE question_id=%(question_id)s ORDER BY submission_time DESC;'''
                   ,  {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def save_question_comment(cursor, question_comment):
    cursor.execute("""INSERT INTO comment (question_id, submission_time, message) 
                        VALUES (%(question_id)s, CURRENT_TIMESTAMP, %(message)s);
                        SELECT * FROM comment WHERE question_id = %(question_id)s""", question_comment)
    new_question_comment = cursor.fetchall()
    return new_question_comment


@connection.connection_handler
def get_all_answer_comments(cursor):
    cursor.execute('''
                SELECT * FROM comment WHERE answer_id IS NOT NULL 
                ORDER BY submission_time;''')
    answer_comments = cursor.fetchall()
    return answer_comments

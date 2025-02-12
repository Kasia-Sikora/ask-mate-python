import psycopg2

import connection


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
                SELECT * FROM question ORDER BY submission_time DESC;
                ''')
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def save_question(cursor, question):
    cursor.execute('''
                    INSERT INTO question (submission_time, title, message, user_id) 
                    VALUES (CURRENT_TIMESTAMP, %(title)s, %(message)s, %(user_id)s);
                    SELECT * FROM question WHERE title= %(title)s AND message= %(message)s;
                    ''', question)
    question = cursor.fetchall()
    return question[0]


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
    cursor.execute(""" SELECT id, submission_time, vote_number, message, image
                    FROM answer 
                    WHERE question_id = %(id)s ORDER BY submission_time DESC""", {'id': quest_id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def search_for_answer(cursor, answer_id):
    cursor.execute(""" SELECT id, submission_time, vote_number, message, image
                    FROM answer 
                    WHERE id = %(id)s ORDER BY submission_time DESC""", {'id': answer_id})
    answer = cursor.fetchall()
    return answer[0]


@connection.connection_handler
def new_answer(cursor, answer_dict):
    cursor.execute("""INSERT INTO answer (submission_time, question_id, message, user_id) 
                        VALUES (CURRENT_TIMESTAMP, %(question_id)s, %(message)s, %(user_id)s);
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
                SELECT * FROM comment WHERE question_id=%(question_id)s ORDER BY submission_time DESC;''',
                   {'question_id': question_id})
    question_comments = cursor.fetchall()
    return question_comments


@connection.connection_handler
def save_question_comment(cursor, question_comment):
    cursor.execute("""INSERT INTO comment (question_id, submission_time, message, id) 
                        VALUES (%(question_id)s, CURRENT_TIMESTAMP, %(message)s, %(user_id)s);
                        SELECT * FROM comment WHERE question_id = %(question_id)s""", question_comment)
    new_question_comment = cursor.fetchall()
    return new_question_comment


#
@connection.connection_handler
def get_all_answer_comments(cursor, answer_id):
    cursor.execute('''
                SELECT * FROM comment WHERE answer_id=%(answer_id)s ORDER BY submission_time DESC;'''
                   , {'answer_id': answer_id})
    answer_comments = cursor.fetchall()
    return answer_comments


@connection.connection_handler
def save_answer_comment(cursor, answer_comment):
    cursor.execute("""INSERT INTO comment (answer_id, submission_time, message) 
                        VALUES (%(answer_id)s, CURRENT_TIMESTAMP, %(message)s);
                        SELECT * FROM comment WHERE answer_id = %(answer_id)s""", answer_comment)
    new_answer_comment = cursor.fetchall()
    return new_answer_comment


#
@connection.connection_handler
def change_answer_vote(cursor, dictionary):
    cursor.execute(""" UPDATE answer 
                        SET vote_number = vote_number + %(vote)s 
                        WHERE id = %(id_answer)s;
                        UPDATE users 
                        SET reputation = reputation + %(reputation)s
                        WHERE id = %(user_id)s""",
                   dictionary)


@connection.connection_handler
def change_question_vote(cursor, dictionary):
    cursor.execute(""" UPDATE question 
                        SET vote_number = vote_number + %(vote)s 
                        WHERE id = %(question_id)s;
                        UPDATE users 
                        SET reputation = reputation + %(reputation)s
                        WHERE id = %(user_id)s
                        """,
                   dictionary)


@connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""SELECT id, submission_time, vote_number, question_id, message, image 
                    FROM answer WHERE id = %(answer_id)s;
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


@connection.connection_handler
def get_comment(cursor, comment_id):
    cursor.execute("""SELECT * FROM comment WHERE id = %(id)s;""", {'id': comment_id})
    comment_details = cursor.fetchall()
    comment_details = dict(comment_details[0])
    return comment_details


@connection.connection_handler
def update_comment(cursor, form_dict):
    cursor.execute("""UPDATE comment SET message = %(message)s WHERE id = %(comment_id)s;""", form_dict)
    cursor.execute("""SELECT * FROM comment WHERE id = %(comment_id)s;""", form_dict)
    comment_details = cursor.fetchall()
    comment_details = dict(comment_details[0])
    return comment_details


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""SELECT answer_id FROM comment WHERE id = %(comment_id)s""", {'comment_id': comment_id})
    answer_id = cursor.fetchall()
    cursor.execute("""DELETE FROM comment WHERE id = %(comment_id)s""", {'comment_id': comment_id})
    answer_id = dict(answer_id[0])
    return answer_id


@connection.connection_handler
def check_login(cursor, user_data):
    cursor.execute('''
                    SELECT password FROM users
                    WHERE login = %(login)s;''', user_data)
    user_name = cursor.fetchall()
    if len(user_name) == 0:
        return user_name
    else:
        return user_name[0]


@connection.connection_handler
def new_user(cursor, registration_dict):
    cursor.execute("""INSERT INTO users (login, password) 
                        VALUES (%(username)s, %(password)s);
                        SELECT login FROM users WHERE login = %(username)s""", registration_dict)
    registration_login = cursor.fetchall()
    return registration_login[0]['login']


@connection.connection_handler
def search_for_user_id(cursor, user):
    cursor.execute("""SELECT id FROM users WHERE login = %(username)s""", {'username': user})
    user_id = cursor.fetchall()
    if len(user_id) == 0:
        return user_id
    else:
        return user_id[0]


@connection.connection_handler
def get_list_of_users(cursor):
    cursor.execute(""" SELECT login, reputation FROM users""")
    list_of_users = cursor.fetchall()
    return list_of_users


@connection.connection_handler
def search_for_user_id_by_question(cursor, question_id):
    cursor.execute(""" SELECT users.id, a.user_id, q.user_id FROM users 
                        JOIN question q on users.id = q.user_id
                        JOIN answer a on q.id = a.question_id
                        WHERE q.id = %(question_id)s OR a.question_id = %(question_id)s""", {'question_id': question_id})
    ids = cursor.fetchall()
    return ids[0]


@connection.connection_handler
def search_data_by_user_id(cursor, user_id):
    cursor.execute(
        """SELECT id FROM question WHERE user_id = %(user_id)s""",
        {'user_id': user_id})
    question_tab_ids = cursor.fetchall()

    cursor.execute("""SELECT * FROM answer WHERE user_id = %(user_id)s""",
                   {'user_id': user_id})
    matching_answers = cursor.fetchall()

    from_question_ids = [x['id'] for x in question_tab_ids]
    from_answer_ids = [x['question_id'] for x in matching_answers]
    matching_quest_ids = tuple(set(from_answer_ids) | set(from_question_ids))
    try:
        cursor.execute("""SELECT * FROM question WHERE id IN %(id_s)s""", {'id_s': matching_quest_ids})
        matching_questions = cursor.fetchall()
    except psycopg2.errors.SyntaxError:
        matching_questions = {}
    return matching_questions, matching_answers


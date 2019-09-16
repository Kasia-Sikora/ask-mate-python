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

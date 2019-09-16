import connection


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
                SELECT * FROM question ORDER BY submission_time;
                ''', )
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def save_question(cursor, question):
    cursor.execute('''
                    INSERT INTO question (title, message) 
                    VALUES (question.title, question.message);
                    SELECT * FROM question WHERE title=question.title AND message=question.message;
                    ''')
    question = cursor.fetchall()
    return question

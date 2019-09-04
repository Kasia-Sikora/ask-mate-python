from flask import Flask, url_for, render_template
import connection, data_manager

app = Flask(__name__)


@app.route('/')
def hello_world():
    question = data_manager.search_for_question(1)
    answer = data_manager.search_for_all_answers(7)
    user_questions = connection.get_all_questions()
    vote = data_manager.change_answer_vote_number(1, 1)
    return render_template('list.html', user_questions=user_questions, question=question, answer=answer, vote=vote)


if __name__ == '__main__':
    app.run()

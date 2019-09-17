from flask import Flask, url_for, render_template, request, redirect
import data_manager
import connection, util

app = Flask(__name__)


@app.route('/')
def home():
    user_questions = data_manager.get_all_questions()
    return render_template('list.html', user_questions=user_questions)


@app.route('/add-question')
def add_question():
    return render_template('new_quest_form.html')


@app.route('/question-form', methods=['GET', 'POST'])
def question_form():
    if request.method == 'POST':
        dict_new_quest = dict(request.form)
        quest_details = data_manager.save_question(dict_new_quest)
        return render_template('question_details.html',
                               question_details=quest_details)


@app.route('/question/<question_id>')
def question_details(question_id):
    quest_details = data_manager.search_for_question(question_id)[0]
    # quest_details = util.change_view_number(quest_details)
    answers = data_manager.search_for_all_answers(question_id)
    return render_template('question_details.html',
                           question_details=quest_details,
                           answers=answers)


@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    return render_template('new_answer_form.html', question_id=question_id)


@app.route('/answer_form', methods={'GET', 'POST'})
def answer_form():
    if request.method == 'POST':
        dict_new_answer = dict(request.form)
        new_answer = connection.save_all_answers(dict_new_answer)
        question_id = new_answer['question_id']
        quest_details = data_manager.search_for_question(question_id)
        return redirect('/question/' + question_id)
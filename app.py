from flask import Flask, url_for, render_template, request, redirect
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def home():
    questions_to_print = []
    user_questions = sorted(connection.get_all_questions(), key = lambda x: x['submission_time'], reverse=True)
    return render_template('list.html', user_questions=user_questions)


@app.route('/add-question')
def add_question():
    return render_template('new_quest_form.html')


@app.route('/question-form', methods={'GET', 'POST'})
def question_form():
    if request.method == 'POST':
        dict_new_quest = dict(request.form)
        new_quest_id = connection.save_all_questions(dict_new_quest)
        quest_details = data_manager.search_for_question(new_quest_id)
        return render_template('question_details.html',
                               question_details=quest_details)


@app.route('/question/<question_id>')
def question_details(question_id):
    quest_details = data_manager.search_for_question(question_id)
    answers = data_manager.search_for_all_answers(question_id)
    print(answers)
    print(quest_details)
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
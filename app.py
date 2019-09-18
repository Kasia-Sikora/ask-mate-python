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
    quest = data_manager.search_for_question(question_id)
    answers = data_manager.search_for_all_answers(question_id)
    return render_template('question_details.html',
                           question_details=quest,
                           answers=answers)


@app.route('/question/<question_id>/new_comment')
def new_comment(question_id):
    return render_template('new_comment_form.html', question_id=question_id)


@app.route('/comment_form', methods=['GET', 'POST'])
def comment_form():
    if request.method == 'POST':
        dict_comment = request.form
        data_manager.save_question_comment(dict_comment)
        return redirect(url_for('comment_details', question_id=dict_comment['question_id']))


@app.route('/question/<question_id>/comments')
def comment_details(question_id):
    quest = data_manager.search_for_question(question_id)
    comments = data_manager.get_all_question_comments(question_id)
    return render_template('comment_details.html',
                           question_details=quest, comments=comments)


@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    return render_template('new_answer_form.html', question_id=question_id)


@app.route('/answer_form', methods=['GET', 'POST'])
def answer_form():
    if request.method == 'POST':
        dict_new_answer = request.form
        data_manager.new_answer(dict_new_answer)
        return redirect(url_for('question_details', question_id=dict_new_answer['question_id']))


from flask import Flask, url_for, render_template, request
import data_manager
import connection

app = Flask(__name__)


@app.route('/')
def home():
    user_questions = connection.get_all_questions()
    return render_template('list.html', uesr_questions=user_questions)


@app.route('/add-question')
def add_question():
    return render_template('new_quest_form.html')


@app.route('/question-form', methods={'GET', 'POST'})
def question_form():
    if request.method == 'POST':
        dict_new_quest = dict(request.form)
        new_quest_id = connection.save_all_questions(dict_new_quest)
        quest_details = data_manager.search_for_question(new_quest_id)
        return render_template('question_details.html', question_details=quest_details)


@app.route('/question/<question_id>')
def question_details(question_id):
    #guestion_detail = data_manager.search_for_question(new_quest_id)
    return render_template('question_details.html')
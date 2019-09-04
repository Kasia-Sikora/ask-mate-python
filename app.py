from flask import Flask, url_for, render_template, request
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
        dict_new_quest = request.form
        question = False  # todo write and read new question from database
        return question_details(question_id=question['id'])

@app.route('/question/<question_id>')
def question_details(question_id):

    return render_template('question_details.html', )
from flask import Flask, url_for, render_template, request, redirect
import data_manager
import connection

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


@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    return render_template('new_answer_form.html', question_id=question_id)


@app.route('/answer_form', methods=['GET', 'POST'])
def answer_form():
    if request.method == 'POST':
        dict_new_answer = request.form
        data_manager.new_answer(dict_new_answer)
        return redirect(url_for('question_details', question_id=dict_new_answer['question_id']))


@app.route('/question/<question_id>/vote-up')
def answer_vote_up(question_id):

    info_dict = {
        'id_answer': request.args.get('answer_id'),
        "vote": 1
    }
    data_manager.change_answer_vote(dictionary=info_dict)
    return redirect(url_for('question_details', question_id=question_id))


@app.route('/question/<question_id>/vote-down')
def answer_vote_down(question_id):
    info_dict = {
        'id_answer': request.args.get('answer_id'),
        "vote": -1
    }
    data_manager.change_answer_vote(dictionary=info_dict)
    return redirect(url_for('question_details', question_id=question_id))


@app.route('/answer/<answer_id>/edit')
def edit_answer(answer_id):
    answer_detail = data_manager.get_answer(answer_id)
    return render_template('edit_answer_form.html', answer_detail=answer_detail)

@app.route('/update_answer/<answer_id>', methods=['GET', 'POST'])
def update_answer(answer_id):
    if request.method == 'POST':
        form_dict = dict(request.form)
        form_dict['answer_id'] = answer_id
        dict_from_dm = data_manager.update_answer(answer_dict=form_dict)
        return redirect(url_for('question_details', question_id=dict_from_dm['question_id']))


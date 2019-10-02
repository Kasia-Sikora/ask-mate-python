from flask import Flask, url_for, render_template, request, redirect, session
import data_manager
import os
import util

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route('/')
def home():
    user = util.check_session_usr()
    user_questions = data_manager.get_all_questions()
    return render_template('list.html', user_questions=user_questions, user=user)


@app.route('/add-question')
def add_question():
    user = util.check_session_usr()
    return render_template('new_quest_form.html', user=user)


@app.route('/question-form', methods=['GET', 'POST'])
def question_form():
    user = util.check_session_usr()
    if request.method == 'POST':
        dict_new_quest = dict(request.form)
        quest_details = data_manager.save_question(dict_new_quest)
        return render_template('question_details.html',
                               question_details=quest_details,
                               user=user)


@app.route('/question/<question_id>')
def question_details(question_id):
    user = util.check_session_usr()
    quest = data_manager.search_for_question(question_id)
    answers = data_manager.search_for_all_answers(question_id)
    return render_template('question_details.html',
                           question_details=quest,
                           answers=answers,
                           user=user)


@app.route('/question/<question_id>/new_comment')
def new_comment(question_id):
    user = util.check_session_usr()
    return render_template('new_comment_form.html', question_id=question_id, user=user)


@app.route('/comment_form', methods=['GET', 'POST'])
def comment_form():
    user = util.check_session_usr()
    if request.method == 'POST':
        dict_comment = request.form
        data_manager.save_question_comment(dict_comment)
        return redirect(url_for('comment_details', question_id=dict_comment['question_id'], user=user))


@app.route('/question/<question_id>/comments')
def comment_details(question_id):
    user = util.check_session_usr()
    quest = data_manager.search_for_question(question_id)
    comments = data_manager.get_all_question_comments(question_id)
    return render_template('comment_details.html',
                           question_details=quest, comments=comments, user=user)


@app.route('/question/<question_id>/new-answer')
def add_answer(question_id):
    user = util.check_session_usr()
    return render_template('new_answer_form.html', question_id=question_id, user=user)


@app.route('/answer_form', methods=['GET', 'POST'])
def answer_form():
    user = util.check_session_usr()
    if request.method == 'POST':
        dict_new_answer = request.form
        data_manager.new_answer(dict_new_answer)
        return redirect(url_for('question_details', question_id=dict_new_answer['question_id'], user=user))


@app.route('/answer/<answer_id>/new-comment')
def new_answer_comment(answer_id):
    user = util.check_session_usr()
    return render_template('answer_comment_form.html', answer_id=answer_id, user=user)


@app.route('/answer_comment_form', methods=['GET', 'POST'])
def answer_comment_form():
    user = util.check_session_usr()
    if request.method == 'POST':
        dict_comment = request.form
        data_manager.save_answer_comment(dict_comment)
        return redirect(url_for('answer_comment_details', answer_id=dict_comment['answer_id'], user=user))


@app.route('/answer/<answer_id>/d')
def answer_comment_details(answer_id):
    user = util.check_session_usr()
    answer = data_manager.search_for_answer(answer_id)
    comments = data_manager.get_all_answer_comments(answer_id)
    return render_template('comment_details.html',
                           answer_details=answer, comments=comments, user=user)


@app.route('/question/<question_id>/answer-up')
def answer_vote_up(question_id):
    user = util.check_session_usr()
    info_dict = {
        'id_answer': request.args.get('answer_id'),
        "vote": 1
    }
    data_manager.change_answer_vote(dictionary=info_dict)
    return redirect(url_for('question_details', question_id=question_id, user=user))


@app.route('/question/<question_id>/answer-down')
def answer_vote_down(question_id):
    user = util.check_session_usr()
    info_dict = {
        'id_answer': request.args.get('answer_id'),
        "vote": -1
    }
    data_manager.change_answer_vote(dictionary=info_dict)
    return redirect(url_for('question_details', question_id=question_id, user=user))


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    user = util.check_session_usr()
    info_dict = {
        "vote": 1,
        "question_id": question_id
    }
    data_manager.change_question_vote(dictionary=info_dict)
    return redirect(url_for('home', user=user))


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    user = util.check_session_usr()
    info_dict = {

        "vote": -1,
        "question_id": question_id
    }
    data_manager.change_question_vote(dictionary=info_dict)
    return redirect(url_for('home', user=user))


@app.route('/answer/<answer_id>/edit')
def edit_answer(answer_id):
    user = util.check_session_usr()
    answer_detail = data_manager.get_answer(answer_id)
    return render_template('edit_answer_form.html', answer_detail=answer_detail, user=user)


@app.route('/update_answer/<answer_id>', methods=['GET', 'POST'])
def update_answer(answer_id):
    user = util.check_session_usr()
    if request.method == 'POST':
        form_dict = dict(request.form)
        form_dict['answer_id'] = answer_id
        dict_from_dm = data_manager.update_answer(answer_dict=form_dict)
        return redirect(url_for('question_details', question_id=dict_from_dm['question_id'], user=user))


@app.route('/comment/<comment_id>/edit')
def edit_comment_form(comment_id):
    user = util.check_session_usr()
    comment_det = data_manager.get_comment(comment_id=comment_id)
    return render_template('edit_comment_form.html', comment_det=comment_det, user=user)


@app.route('/comment/<comment_id>/form', methods=['GET', 'POST'])
def form_comment(comment_id):
    user = util.check_session_usr()
    form_dict = dict(request.form)
    form_dict['comment_id'] = comment_id
    comment_det = data_manager.update_comment(form_dict=form_dict)
    if comment_det['question_id'] is not None:
        return redirect(url_for('question_details', question_id=comment_det['question_id'], user=user))


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    user = util.check_session_usr()
    answ_id = data_manager.delete_comment(comment_id)
    answer_id = answ_id['answer_id']
    return redirect(url_for('answer_comment_details', answer_id=answer_id, user=user))


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = util.check_session_usr()
    if request.method == 'POST':
        user_data = request.form.to_dict()
        check_login = data_manager.check_login(user_data)
        if not check_login:
            message = 'Invalid login or password'
            return render_template('login.html', message=message)
        verify = util.verify_password(user_data['password'], check_login['password'])
        if verify:
            session['username'] = request.form['login']
            return redirect(url_for('home', user=user))
        else:
            message = 'Invalid login or password'
            return render_template('login.html', message=message)
    return render_template('login.html')


@app.route('/registration')
def registration():
    user = util.check_session_usr()
    return render_template('registration.html', user=user)


@app.route('/registration-form', methods=['GET', 'POST'])
def registration_form():
    user = util.check_session_usr()
    if request.method == 'POST':
        registration_dict = request.form.to_dict()
        hashed_pass = util.hash_password(registration_dict['password'])
        registration_dict['password'] = hashed_pass
        saved_login = data_manager.new_user(registration_dict)
        if saved_login == registration_dict['username']:
            session['username'] = request.form['username']
            return redirect(url_for('login', user=user))


@app.route('/logout')
def logout():
    user = util.check_session_usr()
    session.pop('username', None)
    return redirect(url_for('home', user=user))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, url_for, render_template
import connection

app = Flask(__name__)


@app.route('/')
def hello_world():
    user_questions = connection.get_all_questions()
    user_answers = connection.get_all_answers()
    print(user_questions)
    print(user_answers)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

from flask import Flask, url_for, render_template
import connection

app = Flask(__name__)


@app.route('/')
def hello_world():
    user_questions = connection.get_all_questions()
    print(user_questions)
    return render_template('list.html', uesr_questions=user_questions)


if __name__ == '__main__':
    app.run()

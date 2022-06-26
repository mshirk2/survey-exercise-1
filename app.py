from flask import Flask, request, render_template, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
survey = satisfaction_survey


@app.route('/')
def home_page():
    """Shows instructions and button to begin survey"""

    title = survey.title
    instructions = survey.instructions

    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<int:ques_num>')
def show_question(ques_num):
    """Displays current question"""

    # trying to access questions out of order
    if (len(responses) != ques_num):
        flash("Invalid question number")
        return redirect(f"/questions/{len(responses)}")

    # trying to move to next question without answering
    if (responses is None):
        return redirect('/')

    # display question
    curr_question = survey.questions[ques_num]
    return render_template('questions.html', curr_question=curr_question, ques_num=ques_num)


@app.route('/answer')
def receive_answers():
    """Collects answers and redirects to next question or thank you page"""
    
    #retrieves answer and adds it too the response list
    answer = request.args['answer']
    responses.append(answer)
    print(respones)
    
    #redirects to next question or completes survey
    if (len(responses) == len(survey.questions)):
        return redirect('/thank-you')
    
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/thank-you')
def complete_survey():
    """Thanks user for completing survey"""
    
    return render_template('thank-you.html')
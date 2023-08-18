from flask import Flask, request, render_template, redirect, session, flash
from surveys import satisfaction_survey as survey

# from flask import Flask, request, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

# from flask_debugtoolbar import DebugToolbarExtension

# COMPLIMENTS = ["cool", "clever", "tenacious", "awesome", "Pythonic"]

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

question_num = 0
questions = survey.questions
RESPONSES_KEY = "responses"

@app.route('/')
def show_instructions():
    """Root directory renders a satisfaction survey"""
    title = survey.title
    instructions = survey.instructions

    return render_template("index.html", title=title, instructions=instructions)

@app.route('/start', methods=["POST"])
def start_survey():
    """starts a new session and redirects to first question"""
    session[RESPONSES_KEY] = []
    return redirect(f"/questions/0")

@app.route('/questions/<int:id>')
def show_question(id):
    """Displays survey question"""
    responses = session[RESPONSES_KEY]
    # redirect if survey is already done
    if len(responses) == len(list(questions)):
        flash("You have already completed the survey!")
        return redirect("/complete")
    # redirect if jumping ahead in the survey
    if id != len(list(responses)):
        flash("You must do these questions in order!")
        next_question_id = len(responses)
        return redirect(f"/questions/{next_question_id}")
    # otherwise display question
    question_object = questions[id]
    question_text = question_object.question
    choices = question_object.choices
    allow_text = question_object.allow_text
    return render_template("question.html", question_id=id, question_text=question_text, choices=choices, allow_text=allow_text)

@app.route('/answer', methods=["POST"])
def save_response():
    """Save response and navigate to next question"""
    response = request.form["response"]
    responses = session[RESPONSES_KEY]
    responses.append(response)
    session[RESPONSES_KEY] = responses
    next_question_id = len(responses)
    if len(responses) == len(questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{next_question_id}")
    
@app.route('/complete')
def complete_survey():
    return render_template("thanks.html")


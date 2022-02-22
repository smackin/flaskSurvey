from distutils.log import debug
from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_home_survey():
    return render_template('survey-start.html', survey=survey)
# this is where the survey begins.  This extends 'base.html' 'survey' defined in surveys.py  

@app.route("/begin", methods=["POST"])
def begin_survey():
    """begin new session with no responses"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/")
# when the form us submitted - it 


@app.route("/complete")
def complete(): 
    """Displays completed and thank you page """
    return render_template("completed.html")
from distutils.log import debug
from flask import Flask, render_template, redirect, flash, session, request
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
    return redirect("/questions/0")
# when the form us submitted - it 

@app.route('/questions/<int:qid>')
def display_questions(qid):
    '''Displays the current question from surveys.py'''
    responses =  session.get(RESPONSES_KEY)
     
    if (responses is None):
        return redirect('/')
    #if there are no responses, redirect to the start page. 
    
    if (len(responses) == len(survey.questions)):
        # if all the responses are completed - redirect to the completed route. 
        return redirect('/completed')
    
    if (len(responses) != qid):
        flash(f" This is not a valid page... qid = {qid}.")
        return redirect(f"/questions/{len(responses)}")
        
    question = survey.questions[qid]
    return render_template("questions.html", ques_num=qid, question=question )
    
@app.route("/answer", methods=['POST'])
def survey_answer(): 
    #this grabs the answer from the form radio buttons 
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    #each response in the session is appended to the end of the RESPONSES_KEY List
    responses.append(choice)
    session[RESPONSES_KEY] = responses 
    # if all responses are submitted,  then the user is redirected to the completed html page. 
    if (len(responses) == len(survey.questions)):
        return redirect("/completed")
    # otherwise, the user is redirected to the /questions/int html route
    else:
        return redirect(f'questions/{len(responses)}')

@app.route("/completed")
def complete(): 
    #this is the route for the above response.  
    """Displays completed and thank you page """
    return render_template("completed.html")



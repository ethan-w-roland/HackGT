#---INITIALIZATION---
from flask import Flask, request, make_response, jsonify
import random
import nlp

#---BEGIN APPLICATION---

# initialize the flask app
app = Flask(__name__)
SpeechTopic = None
SpeechMetrics = {}
InterviewMetrics = {}

#Users "database"
Users = []
auth = False
User = {"username": None,
        "eduLevel": None,
        "eduFocus": None}

# run the app
if __name__ == '__main__':
   app.run(port=5000)

# default route
@app.route('/')
def index():
    return "Bemo Assistant Root Directory"

# webhook route
@app.route('/webhook', methods= ['POST'])
def webhook():
    return make_response(jsonify(redirect()))

#---WEBHOOK HANDLERS---

# function for responses - branches based on intent
def redirect():

    # req represents submitted data
    req = request.get_json(force=True)
    intent = req["queryResult"]["intent"]["displayName"]

    #Restore Account
    if intent == "Login.User":
        username = req["queryResult"]["parameters"]["Username"]
        restoreAccount(username)
        return

    #Account Management
    elif intent == "AccountCreation.Username":
        username = req["queryResult"]["parameters"]["Username"]
        return setUsername(username)

    elif intent == "AccountCreation.EduLevel":
        level = req["queryResult"]["parameters"]["EducationLevel"]
        return setEduLevel(level)

    elif intent == "AccountCreation.EduFocus":
        focus = req["queryResult"]["parameters"]["Field"]
        return setEduFocus(focus)

    elif "endInteraction" in req["queryResult"]["intent"]: 
        storeUser()
        return

    #Authorization
    if intent == "Speech.Exit" or "Interview.Exit":
        return(branchAuth())

    #Speech Sub-App
    if intent == "Speech.Topic":
        topic = req["queryResult"]["parameters"]["Topic"]
        return SetSpeechTopic(topic)

    elif intent == "Speech.Content":
        content = req["queryResult"]["parameters"]["Content"]
        return AnalyzeSpeech(content)

    #Interview Sub-App
    elif intent == "Interview.Type":
        qType = req["queryResult"]["parameters"]["QuestionType"]
        return HandleQuestionType(qType)
    
    elif intent == "Interview.Content":
        content = req["queryResult"]["parameters"]["Content"]
        return AnalyzeInterview(content)

#Speech Sub-App
def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to: ", SpeechTopic)

def AnalyzeSpeech(content: str):
    sentiment = nlp.getSentiment(content)
    print(content, "....", sentiment)
    output = "Your speech seemed: {}".format(sentiment)
    if SpeechMetrics != {}:
        oldSent = SpeechMetrics['sentiment']
        output += "\nYour sentiment changed by {}%".format(sentiment/oldSent)
    SpeechMetrics['sentiment'] = sentiment
    return {'fulfillmentText': output}

#Inverview Sub-App
def HandleQuestionType(InterviewType:  str):
    print("question type is: ", InterviewType)
    if InterviewType == "general":
        #fetch random interview topic
        lines = open('./interview/questions.txt').read().splitlines()
        question = random.choice(lines).strip()
        print('Randomly picked question is: ', question)
        output = "Great! Here is your question: {} .... Start when you're ready!".format(question)
        return {'fulfillmentText': output}
    elif InterviewType == "CS":
        #fetch random interview topic
        lines = open('./interview/csbasicquestions.txt').read().splitlines()
        question = random.choice(lines).strip()
        print('Randomly picked question is: ', question)
        output = "Great! Here is your question: {} .... Start when you're ready!".format(question)
        return {'fulfillmentText': output}
    else:
        return {'fulfillmentText': 'error'}

def AnalyzeInterview(transcript: str):
    sentiment = nlp.getSentiment(transcript)
    print(transcript, "....", sentiment)
    output = "Your interview seemed: {}".format(sentiment)
    if InterviewMetrics != {}:
        oldSent = InterviewMetrics['sentiment']
        output += "\nYour sentiment changed by {}%".format(sentiment/oldSent)
    InterviewMetrics['sentiment'] = sentiment
    return {'fulfillmentText': output}

#Account Creation
def restoreUser(username):
    for el in Users:
        if el['username'] == username:
            User = el
            auth = True
            break

def setUsername(id):
    auth = True
    User["username"]= id
    print("User.Username was set to: ", id)

def setEduLevel(level):
    User["eduLevel"]= level
    print("User.eduLevel was set to: ", level)

def setEduFocus(focus):
    User["eduFocus"]= focus
    print("User.eduFocus was set to: ", focus)

def storeUser():
    if (User["username"] != None) and (User["eduLevel"] != None) and (User["eduFocus"] != None):
        Users.append(User)
        User = {"username": None,
                "eduLevel": None,
                "eduFocus": None}
        SpeechMetrics = {}
        InterviewMetrics = {}
        SpeechTopic = None
    auth = False

def branchAuth():

    if auth == True:
        respText = ('Exited. Say "Interviews" to practice interviews, "Speech" to practice public '
                    'speaking, "Recommendations" to get study recommendations, or "Inquiry" to '
                    'ask Bemo a question')
        req = request.get_json(force=True)
        oldContext = req["queryResult"]["outputContexts"]["name"]
        newContext = oldContext.split('/Dummy')[0] + "Authorized"
        return {'fulfillmentText': respText,
                'outputContexts':[{
                    "name": newContext,
                    "lifespanCount": 5
                    }]
                }

    elif auth == False:
        respText = ('Exited. Say "Interviews" to practice interviews, "Speech" to practice public '
                    'speaking, or "Inquiry" to ask Bemo a question')
        req = request.get_json(force=True)
        oldContext = req["queryResult"]["outputContexts"]["name"]
        newContext = oldContext.split('/Dummy')[0] + "Anonymous"
        return {'fulfillmentText': respText,
                'outputContexts':[{
                    "name": newContext,
                    "lifespanCount": 5
                    }]
                }

#User Tailored Functions

def recommendContent():
    return None

def tailoredInquiry():
    return None
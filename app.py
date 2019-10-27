#---INITIALIZATION---
from flask import Flask, request, make_response, jsonify
import random
import nlp
class TranscriptAnalysis:
    def __init__(self,transcript):
        self.Categories = []
        self.SpeechTopic = ""
        self.transcript = transcript
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
        restoreUser(username)
        return

    #Account Management
    elif intent == "AccountCreation":
        username = req["queryResult"]["parameters"]["Username"]
        return setUsername(username)

    elif intent == "AccountCreation.EduLevel":
        level = req["queryResult"]["parameters"]["Level"]
        return setEduLevel(level)

    elif intent == "AccountCreation.EduFocus":
        focus = req["queryResult"]["parameters"]["Field"]
        return setEduFocus(focus)

    elif "endInteraction" in req["queryResult"]["intent"]: 
        storeUser()
        return

    #Authorization
    if intent == "Exit":
        return(branchAuth())

    #Speech Sub-App
    if intent == "Speech.Topic":
        topic = req["queryResult"]["parameters"]["SpeechTopic"]
        return SetSpeechTopic(topic)

    elif intent == "Speech.Content":
        content = req["queryResult"]["parameters"]["SpeechTranscript"]
        return AnalyzeSpeech(content)

    #Interview Sub-App
    elif intent == "Interview.Type" or intent == "Anonymous.InterviewType":
        qType = req["queryResult"]["parameters"]["QuestionType"]
        return HandleQuestionType(qType)
    
    elif intent == "Interview.Transcript" or intent == "Anonymous.InterviewTranscript":
        content = req["queryResult"]["parameters"]["Transcript"]
        return AnalyzeInterview(content)

#Speech Sub-App
def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to: ", SpeechTopic)

def AnalyzeSpeech(content: str):
    speechAnalyzer = TranscriptAnalysis(content)
    sentiment = nlp.getSentiment(content)
    speechAnalyzer.Categories = nlp.sample_classify_text(speechAnalyzer.transcript)
    keyword_list = nlp.get_similarity_with_topic(speechAnalyzer.transcript,SpeechTopic,speechAnalyzer.Categories)
    print(keyword_list)
    print(content, "....", sentiment)
    output = "Great! Here is my feedback for you to improve:\n"
    sentimentFeedback = "Overall speech of your sentiment was {}\n".format(sentiment)

    keywordFeedback = "These are the keywords related to your speech: {}\n".format(','.join(keyword_list.split(',')))
    CoverageFeedback = ""
    if len(speechAnalyzer.Categories) >= 2:
        CoverageFeedback = "Your speech covered following topics: {}".format(",".join(cat_name[0] for cat_name in speechAnalyzer.Categories))
        CoverageFeedback += "Your coverage is pretty good as it is covering more than one topic in detail! Keep it up."
    else:
        CoverageFeedback = "Your speech covered following topics: {}".format(",".join(cat_name[0] for cat_name in speechAnalyzer.Categories))

    output = output + sentimentFeedback + keywordFeedback + CoverageFeedback
        

    # if SpeechMetrics != {}:
    #     oldSent = SpeechMetrics['sentiment']
    #     output += "\nYour sentiment changed by {}%".format(sentiment/oldSent)
    # SpeechMetrics['sentiment'] = sentiment
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

def AnalyzeInterview(transcript: str):
    sentiment = nlp.getSentiment(transcript)
    print(transcript, "....", sentiment)
    output = "Your interview seemed: {}".format(sentiment)
    # if InterviewMetrics != {}:
    #     oldSent = InterviewMetrics['sentiment']
    # #     output += "\nYour sentiment changed by {}%".format(sentiment/oldSent)
    # InterviewMetrics['sentiment'] = sentiment
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
        return {'fulfillmentText': respText}

    elif auth == False:
        respText = ('Exited. Say "Interviews" to practice interviews, "Speech" to practice public '
                    'speaking, or "Inquiry" to ask Bemo a question')
        return {'fulfillmentText': respText}

#User Tailored Functions

def recommendContent():
    return None

def tailoredInquiry():
    return None
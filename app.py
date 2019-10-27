#---INITIALIZATION---
from flask import Flask, request, make_response, jsonify
import random
import nlp

#set environmental variable for google auth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./gCloudAuth.json"

#Import Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
client = language.LanguageServiceClient() # Instantiates a client

#---BEGIN APPLICATION---

# initialize the flask app
app = Flask(__name__)
SpeechTopic = None

# run the app
if __name__ == '__main__':
   app.run(threaded=True, port=5000)

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
    print(intent)

    if intent == "GetSubApp": #aka which sub-app to go to
        helpVariable = req["queryResult"]["parameters"]["HelpCategory"]
        return HandleDetectIntent(helpVariable)

    #Speech Sub-App
    elif intent == "GetSpeechTopic":
        speechTopic = req["queryResult"]["parameters"]["SpeechTopic"]
        return SetSpeechTopic(speechTopic)

    elif intent == "GetSpeech":
        Transcript = req["queryResult"]["parameters"]["Transcript"]
        return AnalyzeSpeech(Transcript)

    #Interview Sub-App
    elif intent == "GetInterviewType":
        InterviewType = req["queryResult"]["parameters"]["HelpCategory"]
        return HandleQuestionType(InterviewType)
    
    elif intent == "GetInterview":
        Transcript = req["queryResult"]["parameters"]["Transcript"]
        return AnalyzeInterview(Transcript)

    else:
         return {'fulfillmentText': 'No supported intent detected'}

def HandleDetectIntent(HelpVariable: str):
    print('HelpVariable is: ', HelpVariable)
    if HelpVariable == "speech":
        return {"followupEventInput" : {"name" : "AskSpeechTopicEvent"}}
    elif HelpVariable == 'interview':
        return {"followupEventInput" : {"name" : "AskInterviewTypeEvent"}}
    else:
        return {'fulfillmentText': 'Invalid Selection'}

#Speech Sub-App
def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to: ", SpeechTopic)
    return {'fulfillmentText': 'Great, begin your speech.'}

def AnalyzeSpeech(transcript: str):
    sentiment = nlp.getSentiment(transcript)
    print(transcript, "....", sentiment)
    output = "Your speech seemed: {}".format(sentiment)
    return {'fulfillmentText': output}

#Inverview Sub-App
def HandleQuestionType(InterviewType:  str):
    print("question type is: ", InterviewType)
    if InterviewType == "General":
        #fetch random interview topic
        lines = open('./interview/questions.txt').read().splitlines()
        question = random.choice(lines).strip()
        print('Randomly picked question is: ', question)
        output = "Great! Here is your question: {} .... Start when you're ready!".format(question)
        return {'fulfillmentText': output}
    elif InterviewType == "Computer Science":
        #fetch random interview topic
        lines = open('./interview/csbasicquestions.txt').read().splitlines()
        question = random.choice(lines).strip()
        print('Randomly picked question is: ', question)
        output = "Great! Here is your question: {} .... Start when you're ready!".format(question)
        return {'fulfillmentText': output}
    else:
        return {'fulfillmentText': 'Invalid Selection'}

def AnalyzeInterview(transcript: str):
    sentiment = nlp.getSentiment(transcript)
    print(transcript, "....", sentiment)
    output = "Your interview seemed: {}".format(sentiment)
    return {'fulfillmentText': output}
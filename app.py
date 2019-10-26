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

    if intent == "DetectIntent": #aka which sub-app to go to
        helpVariable = req["queryResult"]["parameters"]["HelpCategory"]
        return HandleDetectIntent(helpVariable)

    elif intent == "GetSpeechTopic":  #aka set speech topic
        speechTopic = req["queryResult"]["parameters"]["SpeechTopic"]
        return SetSpeechTopic(speechTopic)

    elif intent == "GetSpeech": #aka get speech transcript
        Transcript = req["queryResult"]["parameters"]["Transcript"]
        return AnalyzeSpeech(Transcript)

    elif intent == "GetInterviewType":  #aka set interview type question
        InterviewType = req["queryResult"]["parameters"]["HelpCategory"]
        return HandleQuestionType(InterviewType)
    else:
         return {'fulfillmentText': 'No supported intent detected'}

def HandleDetectIntent(HelpVariable: str):
    if HelpVariable == "speech":
        return {"followupEventInput" : {"name" : "AskSpeechTopicEvent"}}
    elif HelpVariable == 'interview':
        return {"followupEventInput" : {"name" : "GetInterviewTypeEvent"}}
    else:
        return {'fulfillmentText': 'Invalid Selection'}

def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to: ", SpeechTopic)
    return {'fulfillmentText': 'Great, begin your speech.'}

def AnalyzeSpeech(transcript: str):
    sentiment = nlp.getSentiment(transcript)
    return {'fulfillmentText': sentiment}

def HandleQuestionType(InterviewType:  str):
    if InterviewType == "General":
        #fetch random interview topic
        lines = open('./interview/questions.txt').read().splitlines()
        intTopic = random.choice(lines).strip()
        print('Randomly picked interview topic is: ', intTopic)
        return {'fulfillmentText': intTopic}
    elif InterviewType == "Computer Science":
        #fetch random interview topic
        lines = open('./interview/csbasicquestions.txt').read().splitlines()
        intTopic = random.choice(lines).strip()
        print('Randomly picked interview topic is: ', intTopic)
        return {'fulfillmentText': intTopic}
    else:
        return {'fulfillmentText': 'This is a response from webhook.'}
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
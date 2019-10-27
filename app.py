from flask import Flask, request, make_response, jsonify
import random

#set environmental variable for google auth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./gCloudAuth.json"

# initialize the flask app
app = Flask(__name__)
SpeechTopic = None
# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def redirect():
    # build a request object
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
        print(Transcript)
        return "Analysing" #{'fulfillmentText': 'This is a response from webhook.'}

    elif intent == "GetInterviewType":  #aka set interview type question
        helpVariable = req["queryResult"]["parameters"]["HelpCategory"]
        return HandleQuestionType(helpVariable)
    else:
        return {'fulfillmentText': 'This is a response from webhook.'}

def HandleDetectIntent(HelpVariable:  str):
    if HelpVariable == "speech":
        return {
            "followupEventInput" : {
                "name" : "AskSpeechTopicEvent"
            }
        }
    elif HelpVariable == 'interview':
        return {
            "followupEventInput" : {
                "name" : "GetInterviewTypeEvent"
            }
        }
    else:
        return {'fulfillmentText': 'This is a response from webhook.'}


def HandleQuestionType(HelpVariable:  str):
    if HelpVariable == "general":
        #fetch random interview topic
        lines = open('./interview/questions.txt').read().splitlines()
        intTopic = random.choice(lines).strip()
        print('Randomly picked interview topic is: ', intTopic)
        return {'fulfillmentText': intTopic}
    elif HelpVariable == "computer":
        #fetch random interview topic
        lines = open('./interview/csbasicquestions.txt').read().splitlines()
        intTopic = random.choice(lines).strip()
        print('Randomly picked interview topic is: ', intTopic)
        return {'fulfillmentText': intTopic}
    else:
        return {'fulfillmentText': 'This is a response from webhook.'}


def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to: ", SpeechTopic)
    return {'fulfillmentText': 'Great begin your speech.'}edo

# create a route for webhook
@app.route('/webhook', methods= ['POST'])
def webhook():
    # entry point to our webhook
    return make_response(jsonify(redirect()))

# run the app
if __name__ == '__main__':
   app.run()
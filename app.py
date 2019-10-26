from flask import Flask, request, make_response, jsonify

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

    if intent == "DetectIntent":
        helpVariable = req["queryResult"]["parameters"]["HelpCategory"]

        return HandleDetectIntent(helpVariable)

    elif intent == "GetSpeechTopic":
        speechTopic = req["queryResult"]["parameters"]["SpeechTopic"]
        return SetSpeechTopic(speechTopic)

    elif intent == "GetSpeech":
        Transcript = req["queryResult"]["parameters"]["Transcript"]
        print(Transcript)

    # return a fulfillment response
    #return {'fulfillmentText': 'This is a response from webhook.'}

def HandleDetectIntent(HelpVariable:  str):
    if HelpVariable == "speech":
        return {
            "followupEventInput" : {
                "name" : "AskSpeechTopicEvent"
            }
        }
    else:
        return {'fulfillmentText': 'This is a response from webhook.'}
def SetSpeechTopic(speechTopic: str):
    SpeechTopic = speechTopic
    print("Topic was set to,",SpeechTopic)
    return {'fulfillmentText': 'Great begin your speech.'}
# create a route for webhook
@app.route('/webhook', methods= ['POST'])
def webhook():
    # entry point to our webhook
    return make_response(jsonify(redirect()))

# run the app
if __name__ == '__main__':
   app.run()

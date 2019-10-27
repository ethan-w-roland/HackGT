#set environmental variable for google auth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./gCloudAuth.json"

#Import Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
client = language.LanguageServiceClient() # Instantiates a client

def getSentiment(text: str):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    score = sentiment.score
    if score > 0.3:
        return "Positive, out of 10 you got " + str(int(score * 10))
    elif score < -0.3:
        return "Negative out of -10 you got " + str(int(score * 10))
    else:
        return "Neutral out of 10 you got " + str(int(score * 10))
#set environmental variable for google auth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./gCloudAuth.json"

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
client = language.LanguageServiceClient() # Instantiates a client

# The text to analyze
text = u"I hate everything and crave death and destruction"
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
#set environmental variable for google auth
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./gCloudAuth.json"

import requests

#Import Google Cloud client library
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud.language_v1 import types
client = language_v1.LanguageServiceClient() # Instantiates a client

import textrazor
import spacy

textrazor.api_key = "56242e609bd323434ac79e3d17040e7a895d79400439ffe8e5e76eb8"


#FUNCTIONS
def getSentiment(text: str):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    score = sentiment.score
    if score > 0.3:
        return "Positive, good job!"
    elif score < -0.3:
        return "Negative, you may want to change your tone!"
    else:
        return "Neutral, you may want to be a bit more positive."

def sample_classify_text(text_content: str):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """

    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    response = client.classify_text(document)
    
    # Loop through classified categories returned from the API
    tuple_list = []
    for category in response.categories:
        tuple_list.append((category.name,category.confidence))

    return tuple_list
    

#transcript = "San Francisco is often called Everybody’s Favorite City, a title earned by its scenic beauty, cultural attractions, diverse communities, and world-class cuisine. Measuring 49 square miles, this very walk-able city is dotted with landmarks like the Golden Gate Bridge, cable cars, Alcatraz and the largest Chinatown in the United States. A stroll of the City’s streets can lead from Union Square to North Beach to Fisherman’s Wharf, with intriguing neighborhoods to explore at every turn. Views of the Pacific Ocean and San Francisco Bay are often laced with fog, creating a romantic mood in this most European of American cities."
#print(sample_classify_text(transcript))

def get_similarity_with_topic(transcript, speechTopic, categories):
    client = textrazor.TextRazor(extractors=["topics"])
    textrazor_resonse = client.analyze(transcript)
    topic_list = textrazor_resonse.topics()
    print('topic list is',topic_list)
    keyword_list = []
    for topic in topic_list:
        keyword_list.append(topic.label)

    category_list = textrazor_resonse.categories()
    print(category_list)
    return keyword_list
    '''max_similarity = -1000
    nlp = spacy.load('en_core_web_lg') 
    print(topic_list)
    for topic_razor in topic_list:
        tokens = nlp(topic_razor.label + " " +  speechTopic)
        for token in tokens:
             print(token.text, token.has_vector, token.vector_norm, token.is_oov)
    '''
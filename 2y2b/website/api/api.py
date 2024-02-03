from flask import Flask, request
import openai
from openai import OpenAI
import time
import os
import json
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1
from firebase_admin import credentials, initialize_app, storage, firestore
from newsapi import NewsApiClient
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv 
import pandas as pd
import numpy as np
from google.oauth2 import service_account

load_dotenv()
app = Flask(__name__)
cred = credentials.Certificate("y2b firebase-adminsdk.json")
initialize_app(cred, {'storageBucket': 'y2b-fd594.appspot.com'})

db = firestore.client()
users_ref = db.collection('users')

# Called when "Submit" clicked
@app.route('/submit')
def test_func():
    # Write name, sources, and topics to an entry in Firestore
    name = request.args.get('name')
    sources = request.args.get('sources').split(", ")
    topics = request.args.get('topics').split(", ")
    doc_ref = db.collection("users").document(name)
    doc_ref.set({"sources": sources, "topics": topics})
    
    # Calculate number of words per topic - targeting a total of 360 words
    wordsPerTopic = 360 / len(topics)

    # iterate through each topic
    topic_outputs = []
    for topic in topics:
      articles = getText(topic, sources)
      gptOutput = completePrompt(f'Summarize these articles in a news-in-brief in a text-to-speech friendly format in {wordsPerTopic} words' + articles, 'api.openai.com', 240, 1, 1, 0, 0)
      topic_outputs.append(gptOutput)

    topic_outputs_str = '['.join((str(output) + ";;; ") for output in topic_outputs).join(']')

    final_output = completePrompt('Combine these news-in-briefs (separated by ";;; ") in a text-to-speech friendly format in 360 words with appropriate transititions' + topic_outputs_str, 'api.openai.com', 720, 1, 1, 0, 0)

    texttomp3(name, '<speak>' + f"Good morning {name}! This is your yesterday, blended briefly." + final_output + '</speak>')
    uploadtoFB(name)
    os.remove(name + '.mp3')

    return doc_ref.get().to_dict()

# Sample good topics/sources: cryptocurrency, [wired.com, businessinsider.com]

# Get news articles on a given topic from given sources
def getText(keyword, sources):
  parameters = {
    'q': keyword,
    "sortBy": "date",
    'pageSize': 100,
    'apiKey': "685b6d96a3b34ad2a0707536bd71ded4",
    'language': 'en',
    'from' : '2024-01-02'
  }
  response = requests.get('https://newsapi.org/v2/everything', params = parameters)
  all_articles = response.json()

  urls = []
  for i in range(len(all_articles['articles'])):
    url = all_articles['articles'][i]['url']
    urls.append(url)

  if sources != []:
    sourced_urls = []
    for url in urls:
      for source in sources:
        if source in url:
          sourced_urls.append(url)
  else:
    sourced_urls = []
    for url in urls:
      sourced_urls.append(url)

  texts = ""
  for i in range(min(len(sourced_urls),5)):
    article_name = Article(sourced_urls[i])
    article_name.download()
    article_name.parse()
    texts += article_name.text

  return texts

# Get GPT output from a prompt and some model parameters
def completePrompt(prompt, apiUri, max_tokens, temperature, top_p, presence_penalty, frequency_penalty):
    client = OpenAI(api_key=os.getenv('OPENAI_KEY'), base_url=f'https://{apiUri}/v1')
    # openai.api_base = "http://10.0.0.103:1234/v1"
    completion = client.chat.completions.create(model="gpt-3.5-turbo-16k",
    # model="gpt-4",
    # model="gpt-4-32k-0613",
    messages=[
        {"role": "user",
         "content": prompt}
        ],
    max_tokens=max_tokens,
    temperature=temperature,
    top_p=top_p,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty)

    # print(f'reached here with this response: {response}')
    return completion.choices[0].message.content

# Get mp3 of speech for given text, write it to local file name.mp3
def texttomp3(name, text):
  credentials = service_account.Credentials.from_service_account_file('y2b firebase-adminsdk.json')
  client = texttospeech_v1.TextToSpeechClient(credentials=credentials)
  synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)
  voice1 = texttospeech_v1.VoiceSelectionParams (
    language_code = 'en-US',
    name = 'en-US-Journey-D',
    ssml_gender = texttospeech_v1.SsmlVoiceGender.MALE)
  audio_config = texttospeech_v1.AudioConfig(
    audio_encoding = texttospeech_v1.AudioEncoding.MP3
  )

  response1 = client.synthesize_speech (
    input = synthesis_input,
    voice = voice1,
    audio_config = audio_config
  )
  mp3name = name + '.mp3'
  with open(mp3name, 'wb',) as output:
    output.write(response1.audio_content)
  return

# Upload name.mp3 to Firebase storage
def uploadtoFB(name):
  fileName = name + ".mp3"
  bucket = storage.bucket()
  blob = bucket.blob(fileName)
  blob.upload_from_filename(fileName)
  blob.make_public()
  return

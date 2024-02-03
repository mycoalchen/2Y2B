from flask import Flask, request
import openai
import os
import json
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1
from firebase_admin import credentials, initialize_app, storage
from newsapi import NewsApiClient
from newspaper import Article
import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import numpy as np
from google.oauth2 import service_account

app = Flask(__name__)
cred = credentials.Certificate("ferrous-arena-413203-2104c5c4c118.json")
initialize_app(cred, {'storageBucket': 'y2b-fd594.appspot.com'})

@app.route('/test')
def test_func():
    name = request.args.get('name')
    return {'response': name + ' is bottom g'}

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
    #print(url)
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

def completePrompt(prompt, apiUri, max_tokens, temperature, top_p, presence_penalty, frequency_penalty):
    # openai.api_base = "http://10.0.0.103:1234/v1"
    apiUri = apiUri
    openai.api_base = f'https://{apiUri}/v1'
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        # model="gpt-4",
        # model="gpt-4-32k-0613",
        messages=[
            {"role": "user",
             "content": prompt}
            ],
        max_tokens=max_tokens,
        # max_new_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
        )

    # print(f'reached here with this response: {response}')
    return completion.choices[0].message.content

def texttomp3(name, text):
  credentials = service_account.Credentials.from_service_account_file('ferrous-arena-413203-2104c5c4c118.json')
  client = texttospeech_v1.TextToSpeechClient(credentials=credentials)
  synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)
  voice1 = texttospeech_v1.VoiceSelectionParams (
    language_code = 'en-in',
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

def uploadtoFB(name):
  fileName = name + ".mp3"
  bucket = storage.bucket()
  blob = bucket.blob(fileName)
  blob.upload_from_filename(fileName)
  blob.make_public()
  return

articles = getText('cryptocurrency',['wired.com','businessinsider.com'])
gptOutput = completePrompt('Summarize these articles in a news-in-brief in a text-to-speech friendly format in 200 words' +articles, 'api.openai.com', 400, 1, 1, 0, 0)
texttomp3('john', '<speak>'+gptOutput+'</speak>')
uploadtoFB('john')
os.remove('john.mp3')
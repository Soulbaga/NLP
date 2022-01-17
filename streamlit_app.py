#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START language_quickstart]
    # Imports the Google Cloud client library
    # [START language_python_migration_imports]
    from google.cloud import language_v1

    # [END language_python_migration_imports]

    # Instantiates a client
    # [START language_python_migration_client]
    client = language_v1.LanguageServiceClient()
    # [END language_python_migration_client]

    # The text to analyze
    text = u"Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    # [END language_quickstart]


if __name__ == "__main__":
    run_quickstart()










import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums

from google.cloud import language
from google.cloud.language import types

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from fake_useragent import UserAgent
import requests
import pandas as pd
import numpy as np


from google.colab import files
uploaded = files.upload()
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

#The second method
#credential_path = "/firm-progress-333610-8a6e7210503d (NLP API Key Json).json"

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

#from google.colab import drive
#drive.mount("/gdrive/", force_remount=False)

#!ls "/content/gdrive/My Drive/Quebec Mobile [PUBLIC] -20220114T174342Z-001"

#image_dir = "./gdrive/My Drive/Quebec Mobile [PUBLIC] -20220114T174342Z-001/Quebec Mobile [PUBLIC]/SEO NLP Json"

def processhtml(url):

    ua = UserAgent() 
    headers = { 'User-Agent': ua.chrome } 
    res = requests.get(url,headers=headers) 
    html_page = res.text

    url_dict = {}

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.HTML

    language = "en"
    document = {"content": html_page, "type": type_, "language": language}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    for entity in response.entities:
        url_dict[entity.name] = round(entity.salience,4)

    url_dict = {k.lower(): v for k, v in url_dict.items()}

    return url_dict

url1 = "https://storelocator.naturalhealingnow.com/health-food-stores-near-me/" 
url2 = "http://www.manhattanhealthfoodstore.com/" 

url1_dict = processhtml(url1)
url2_dict = processhtml(url2)

df = pd.DataFrame([], columns=['Entity','URL1','URL2','Difference'])

for key in set(url1_dict) & set(url2_dict):
    url1_keywordnum = str(url1_dict.get(key,"n/a"))
    url2_keywordnum = str(url2_dict.get(key,"n/a"))
    
    if url2_keywordnum > url1_keywordnum:
        diff = str(round(float(url2_keywordnum) - float(url1_keywordnum),3))
    else:
        diff = "0"

    new_row = {'Keyword':key,'URL1':url1_keywordnum,'URL2':url2_keywordnum,'Difference':diff}
    
    df = df.append(new_row, ignore_index=True)

print(df.sort_values(by='Difference', ascending=False))

diff_lists = set(url2_dict) - set(url1_dict)

final_diff = {}

for k in diff_lists:
  for key,value in url2_dict.items():
    if k == key:
      final_diff.update({key:value})

df = pd.DataFrame(final_diff.items(), columns=['Keyword','Score'])

print(df.head(25).sort_values(by='Score', ascending=False))

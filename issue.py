import requests
import json
from pydash import py_, includes
from requests.auth import HTTPBasicAuth
import jieba
import re
import math

jiraUrlPrefix = "https://hnalogistics4pd.atlassian.net/rest/api/2/search?jql=project=LPD&startAt="
account = 'YOUR_ACCOUNT'
password = 'PASS'

def seg(str):
  seg_list = jieba.cut(str, cut_all=False)
  return (
    py_(list(seg_list))
      .map(lambda x: x)
      .value()
  )

def getCount(w, c):
  return {'word': c, 'count': math.floor(math.log(len(w), 1.2))}

def urlWithStartAt(n):
  return jiraUrlPrefix + str(n)

def fetch(url):
  print('loading: ' + url)
  resp = requests.get(url, auth=HTTPBasicAuth(account, password))
  data = json.loads(resp.text)
  result = (
    py_(data['issues'])
      .map(lambda issue: issue['fields']['summary'])
      .value()
  )
  return result

def getWordCount():
  wordCountResult = (
    py_(list(range(12)))
      .map(lambda x: x*50)
      .map(urlWithStartAt)
      .map(fetch)
      .flatten()
      .compact()
      .map(seg)
      .flatten()
      .filter(lambda x: re.match('[a-zA-Z\u4e00-\u9fa5]', x))
      .reject(lambda x: len(x)<2)
      .group_by()
      .map(getCount)
      .order_by(['count'])
      .filter(lambda x: x['count'] > 1)
      .value()
  )

  return wordCountResult()

result = getWordCount()

for member in result:
    print(str(member['count']) + ' ' + member['word'])



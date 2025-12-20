#!/usr/bin/env python3

import string
import json
import sqlite3
import random
#import cgi
import configparser
import sys, os, multipart

def main():
  config = configparser.ConfigParser()
  config.read("slackneil.conf")
  dbfile = config.get("Slack Neil", "dbfile")

  environ = dict(os.environ.items())
  environ['wsgi.input'] = sys.stdin.buffer
  form, files = multipart.parse_form_data(environ)

  reply = {}

  if "text" in form:
    form["text"].strip()
    form["text"].replace("__END__", "_END_")
    form["text"].replace("__START__", "_START_")
    if form["text"].endswith("?"):
      sentencetype = "interog"
    else:
      sentencetype = "declar"
    inputsentence = form["text"].split()[1:]
    inputsentence.insert(0, "__START__")
    inputsentence.append("__END__")

  conn = sqlite3.connect(dbfile)

  learnsentence(inputsentence, sentencetype, conn)
  reply["text"] = buildsentence(conn)

  conn.close()

  if "user_name" in form:
    reply["text"] = form["user_name"] + ": " + reply["text"]

  print("Content-Type: text/text")
  print()
  if "token" in form:
    print(json.dumps(reply))


#####################################################################
##
## Learn the sentence
##
def learnsentence(sentence, sentencetype, conn):
  cur = conn.cursor()

  for i in range(len(sentence)-1):
    cur.execute("insert into %s values(?, ?)" % (sentencetype), (sentence[i].lower(), sentence[i+1]))

  conn.commit()


#####################################################################
##
## Build a sentence
##
def buildsentence(conn):
  cur = conn.cursor()

  if random.randint(0, 9) < 3:
    sentencetype = "interog"
  else:
    sentencetype = "declar"

  sentence = []
  word = "__START__"
  while word != "__END__":
    sentence.append(word)
    cur.execute('select value from %s where key=?' % (sentencetype), (word.lower(),))
    returnlist = cur.fetchall()
    word = returnlist[random.randint(0, len(returnlist) - 1)][0]

  return(" ".join(sentence[1:]))


if __name__ == "__main__":
  main()

#!/usr/bin/env python

import json
import sqlite3
import random
import cgi
import cgitb

#cgitb.enable(display=0, logdir="/tmp/slackneil")

expectedtoken = "Tax3fZPwADe2NbKuSjxnXzXr"

def main():
  form = cgi.FieldStorage()

  reply = {}

  if "text" in form:
    if form["text"].value.endswith("?"):
      sentencetype = "interog"
    else:
      sentencetype = "declar"
    inputsentence = form["text"].value.split()[1:]
    inputsentence.append("__END__")

  conn = sqlite3.connect("/home/cluening/projects/slackneil/neilvocab.sqlite3")
  cur = conn.cursor()

  for i in range(len(inputsentence)-1):
    cur.execute('select value from %s where key=?' % (sentencetype), (inputsentence[i].lower(),))
    returnline = cur.fetchone()
    if returnline == None:
      wordlist = []
      wordlist.append(inputsentence[i+1])
      cur.execute("insert into %s values(?, ?)" % (sentencetype), (inputsentence[i].lower(), json.dumps(wordlist)))
    else:
      wordlist = json.loads(returnline[0])
      wordlist.append(inputsentence[i+1])
      cur.execute("update %s set value=? where key=?" % (sentencetype), (inputsentence[i].lower(), json.dumps(wordlist)))

# FIXME: Put commit line in here

  sentence = []
  word = "__START__"
  while word != "__END__":
    sentence.append(word)
    cur.execute('select value from %s where key=?' % (sentencetype), (word.lower(),))
    returnline = cur.fetchone()
    wordlist = json.loads(returnline[0])
    word = wordlist[random.randint(0, len(wordlist) - 1)]

  reply["text"] =  " ".join(sentence[1:])

  if "user_name" in form:
    reply["text"] = form["user_name"].value + ": " + reply["text"]


  print "Content-Type: text/text"
  print
  if "token" in form:
    print json.dumps(reply)


if __name__ == "__main__":
  main()

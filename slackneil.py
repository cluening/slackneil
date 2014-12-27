#!/usr/bin/env python

import json
import sqlite3
import random
import cgi
import cgitb

#cgitb.enable(display=0, logdir="/tmp/slackneil")

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

  learnsentence(inputsentence, sentencetype, conn)
  reply["text"] = buildsentence(conn)

  conn.close()

  if "user_name" in form:
    reply["text"] = form["user_name"].value + ": " + reply["text"]

  print "Content-Type: text/text"
  print
  if "token" in form:
    print json.dumps(reply)

#####################################################################
##
## Learn the sentence
##
def learnsentence(sentence, sentencetype, conn):
  cur = conn.cursor()

  for i in range(len(sentence)-1):
    cur.execute('select value from %s where key=?' % (sentencetype), (sentence[i].lower(),))
    returnline = cur.fetchone()
    if returnline == None:
      wordlist = []
      wordlist.append(sentence[i+1])
      cur.execute("insert into %s values(?, ?)" % (sentencetype), (sentence[i].lower(), json.dumps(wordlist)))
    else:
      wordlist = json.loads(returnline[0])
      wordlist.append(sentence[i+1])
      cur.execute("update %s set value=? where key=?" % (sentencetype), (sentence[i].lower(), json.dumps(wordlist)))

# conn.commit()


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
    returnline = cur.fetchone()
    wordlist = json.loads(returnline[0])
    word = wordlist[random.randint(0, len(wordlist) - 1)]

  return(" ".join(sentence[1:]))


if __name__ == "__main__":
  main()

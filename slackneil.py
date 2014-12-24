#!/usr/bin/env python

import json
import random
import cgi
import cgitb

cgitb.enable(display=0, logdir="/tmp/slackneil")

expectedtoken = "Tax3fZPwADe2NbKuSjxnXzXr"

def main():
  reply = {}
  declarfile = open("/tmp/declar", "r")
  declarjson = declarfile.readline()
  declarfile.close()
  # This is the slow line
  declarvocab = json.loads(declarjson)

  declarvocabclean = {}
  for key in declarvocab.keys():
    declarvocabclean[key.lower()] = declarvocab[key]
  declarvocab = declarvocabclean

  sentence = []
  word = "__START__"
  while word != "__END__":
    sentence.append(word)
    word = str(declarvocab[word.lower()][random.randint(0, len(declarvocab[word.lower()]) - 1)])
  reply["text"] =  " ".join(sentence[1:])


  print "Content-Type: text/text"
  print
  form = cgi.FieldStorage()
  if "token" in form:
    print json.dumps(reply)


if __name__ == "__main__":
  main()

#!/usr/bin/env python

import json
import random
import cgi
import cgitb

#cgitb.enable(display=0, logdir="/tmp/slackneil")

expectedtoken = "Tax3fZPwADe2NbKuSjxnXzXr"

def main():
  form = cgi.FieldStorage()

  reply = {}

  # Read in the vocabulary
  # FIXME: this should choose between declar and interog
  declarfile = open("/tmp/declar", "r")
  declarjson = declarfile.readline()
  declarfile.close()
  # This is the slow line
  declarvocab = json.loads(declarjson)

  declarvocabclean = {}
  for key in declarvocab.keys():
    declarvocabclean[key.lower()] = declarvocab[key]
  declarvocab = declarvocabclean

  if "text" in form:
    inputsentence = form["text"].value.split()[1:]
    inputsentence.append("__END__")

  for i in range(len(inputsentence)-1):
    if inputsentence[i].lower() in declarvocab:
      declarvocab[inputsentence[i].lower()].append(inputsentence[i+1])
    else:
      declarvocab[inputsentence[i].lower()] = inputsentence[i+1]

  # Write out the vocabulary with what it just learned
  # FIXME: this should choose between declar and interog
  declarfile = open("/tmp/declar.new", "w")
  json.dump(declarvocab, declarfile)
  declarfile.close()

  sentence = []
  word = "__START__"
  while word != "__END__":
    sentence.append(word)
    word = str(declarvocab[word.lower()][random.randint(0, len(declarvocab[word.lower()]) - 1)])
  reply["text"] =  " ".join(sentence[1:])


  print "Content-Type: text/text"
  print
  if "token" in form:
    print json.dumps(reply)


if __name__ == "__main__":
  main()

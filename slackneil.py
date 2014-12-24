#!/usr/bin/env python

import json
import random
import cgi
import cgitb

cgitb.enable(display=0, logdir="/tmp/slackneil")

def main():
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
  cleansentence =  " ".join(sentence[1:])

  #print cleansentence

  print "Content-Type: text/text"
  print
  print "{"
  form = cgi.FieldStorage()
  if "token" in form:
    print "  \"text\": \"%s\"" % cleansentence
  else:
    print "  \"text\": \"No token?\""
  print "}"


if __name__ == "__main__":
  main()

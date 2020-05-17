from nltk.corpus import stopwords
import string, re

def getStopWords():
    return stopwords.words('english')


def filterData(input):

    stop_words = getStopWords()
    punct = [p for p in set(string.punctuation) if p not in (".")]
    input = input.lower().replace("\n", " ").replace("\t", " ").strip(" ")
    #Remove punctations
    input = "".join(c for c in input if c not in punct)
    input = " ".join([c for c in input.split(" ") if not(
        c[:1].isdigit() and c[1:2] in (p for p in punct))])
    input = " ".join([w for w in input.split() if w not in stop_words])
    input = " ".join([w for w in input.split(" ") if not(
        w[:1].isdigit() and w[1:].isalpha())])
    input = " ".join([w for w in input.split(" ") if not(
        w[:3].isdigit() and w[3:].isalpha())])
    input = " ".join([w[:-1] if not(w[:1].isdigit())
                      and w.endswith(".") else w for w in input.split(" ")])
    input = " ".join([w for w in input.split(
        " ") if len(w) > 2 and len(w) < 15])
    input = " ".join([w.replace("."," ") if len(w) > 9 or len(w) < 7 else w for w in input.split(" ") ])  
    return input

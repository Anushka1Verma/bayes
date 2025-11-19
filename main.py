import pandas as pd
import re
import math
from collections import defaultdict, Counter

df = pd.read_csv("spam.csv")

#splitting the message into words
def tokenize(message):
    return re.findall(r"\b[a-zA-Z]+\b", message)

#adding a new column for the tokens
df["tokens"] = df["message"].apply(tokenize)

spam = df[df["label"] == "spam"]
spam_c = df[df["label"] == "ham"]

#adding the probablitiy aspect now
prob_spam = len(spam)/len(df)
prob_spam_c = len(spam_c)/len(df)

'''
what we wanna find P(spam|word)
baye's theorem:
P(spam|word) = P(word|spam) * P(spam) / P(word)
P(word) = prob the user input word is in vocab bag that model is trained on
basically ignoring other words that model doesn't know
'''


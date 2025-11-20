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

#word counter dictionary, key=word, value=freq
spam_words = Counter([w for tokens in spam["tokens"] for w in tokens])
spam_c_words = Counter([w for tokens in spam_c["tokens"] for w in tokens])

#total word count
spam_total = sum(spam_words.values())
spam_c_total = sum(spam_c_words.values())

#full vocab
vocab = set(list(spam_words.keys())+list(spam_c_words.keys()))

'''
what we wanna find P(spam|word)
baye's theorem:
P(spam|word) = P(word|spam) * P(spam) / P(word)
P(word) = prob the user input word is in vocab bag that model is trained on
basically ignoring other words that model doesn't know
'''

#employing laplace smoothing
'''
basically for words that aren't present in our vocab, P(word|spam) will be zero
because basically prob of this word being there, given email is spam, is zero since model has never seen this word
so, the whole formula becomes zero despite the prob not being zero for everything
laplace smoothing adds 1 to the numerator and vocab len to the denominator
'''

#P(word|spam) = P(word and spam) / P(spam) = freq of word in spam / total words in spam
def prob_wordgivenspam(word):
    return ((spam_words[word]+1)/(spam_total+len(vocab)))

def prob_wordgivenspamc(word):
    return ((spam_c_words[word]+1)/(spam_c_total+len(vocab)))

def predict(text):
    tokens = tokenize(text)

    # log probabilities (prevents underflow)
    log_spam = math.log(prob_spam)
    log_ham = math.log(prob_spam_c)

    for w in tokens:
        log_spam += math.log(prob_wordgivenspam(w))
        log_ham += math.log(prob_wordgivenspamc(w))

    return "spam" if log_spam > log_ham else "spam c"


# Test
test_messages = [
    "dear user claim your prize",
    "are you free for dinner",
    "dear customer meeting today"
]

for msg in test_messages:
    print(msg, "->", predict(msg))
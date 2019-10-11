import sys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from collections import Counter
import textacy.extract
from tika import parser
from textblob import TextBlob

l=[]
nlp = spacy.load('en_core_web_sm')

# PDF_file = "s.txt"
# parsed = parser.from_file(PDF_file)
# text=parsed["content"]
# print(text)
# print("\n")

#London is the capital. And most populous city. England.
text=sys.argv[1]#"Parlez-vous anglais?"

outfile="output.txt"
f = open(outfile, "w")
f.write(str(text))
f.close()

text1=open("output.txt")
text1=text1.read()
translation=TextBlob(text1)
if translation.detect_language() != 'en':
    en_blob = translation.translate(to='en')
    text1=en_blob

text1 = str(text1)
#text="Parlez-vous anglais? London is the capital and most populous city of England and  the United Kingdom. Today Machine learning (ML) is the scientific study of algorithms in  statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data in India, known as training data, in order to make predictions or decisions for Google without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of google email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics. Manchester United is a very famous football club."

doc=nlp(text1)

# Add some Stop Words
my_stop_words=[':', '.', ',', '-', '(', ')','"',' ']
for stopword in my_stop_words:
    add_word=nlp.vocab[stopword]
    add_word.is_stop=True

#Printing After Removing StopWords stopwords = list(STOP_WORDS)
word_after_stop_words=[w.text.lower() for w in doc if not w.is_stop]# and not w.is_punct]


# Word Frequency
word_frequencies={}
for word in word_after_stop_words:
    if word not in word_frequencies.keys():
        word_frequencies[word]=1
    else:
        word_frequencies[word]+=1

# Maximum Word Frequency (Important)
maximum_frequency = max(word_frequencies.values())


sorted_words = sorted(word_frequencies.items(), key=lambda x: int(x[1]),reverse = True)

# Word Frequency Distribution
for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#print(word_frequencies)

sentence_list = [ sentence for sentence in doc.sents ]
#print(sentence_list)

# Sentence Score via comparrng each word with sentence
sentence_scores = {}  
for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 32:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]


summarized_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)
#print(summarized_sentences)


final_sentences = [w.text for w in summarized_sentences]
#print(final_sentences)

summary=" ".join(final_sentences)

# Summarizing by word frequency distribution
print(summary)

# Summarizing with Gensim
from gensim.summarization.summarizer import summarize
#text="""London is the capital and most populous city of England and  the United Kingdom. Today Machine learning (ML) is the scientific study of algorithms in  statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data in India, known as "training data", in order to make predictions or decisions for Google without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of google email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics. Manchester United is a very famous football club."""
summary1=summarize(text1,ratio=0.5)
summary1=summary1.replace("\n",'')
print(summary1)


# Summarizing with LexRank Sumy
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#document1="""London is the capital and most populous city of England and  the United Kingdom. Today Machine learning (ML) is the scientific study of algorithms in  statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data in India, known as "training data", in order to make predictions or decisions for Google without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of google email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics. Manchester United is a very famous football club."""

# For Strings
parser = PlaintextParser.from_string(text1,Tokenizer("english"))

# For Files
# parser = PlaintextParser.from_file(file, Tokenizer("english"))

# Using LexRank
summarizer = LexRankSummarizer()
#Summarize the document with 2 sentences
summary = summarizer(parser.document, 5)

for sentence in summary:
    print(sentence,end=" ")


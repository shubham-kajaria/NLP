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


from django.shortcuts import render
import requests
import sys
from subprocess import run,PIPE


def button(request):
	return render(request,'home.html')

def external(request):
	inp= request.POST.get('param')
	output1= run([sys.executable,'//Users//shubham//Documents//NLP//NLP_Project1//FinalNLP.py',inp],shell=False,stdout=PIPE)
	out1=output1.stdout[:-1]
	out1=out1.decode('utf-8')
	print(out1)
	
	output2= run([sys.executable,'//Users//shubham//Documents//NLP//NLP_Project1//Gensim.py',inp],shell=False,stdout=PIPE)
	out2=output2.stdout[:-1]
	out2=out2.decode('utf-8')
	print(out2)
	
	output3= run([sys.executable,'//Users//shubham//Documents//NLP//NLP_Project1//LexRankSumy.py',inp],shell=False,stdout=PIPE)	
	out3=output3.stdout[:-1]
	out3=out3.decode('utf-8')
	print(out3)
	
	return render(request,'home.html',{ 'data0':out1, 'data1':out2, 'data2':out3 })
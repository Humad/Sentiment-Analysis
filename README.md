# Sentiment Analysis

A program that uses the Natural Language Toolkit (NLTK) platform on Python to perform sentiment analysis on a live Twitter stream.

# Introduction
I used NLTK to tokenize tweets and then run them through five different trained classifiers. 
Each classifier defines a tweet as having positive or negative sentiment. The results are tallied and a final sentiment (the mode) is given,
as well as the confidence level (i.e How many classifiers agreed on this sentiment).

I used Tkinter to create a basic GUI for the application, Tweepy to connect to Twitter to get a live stream of tweets, and Matplotlib to plot the results.

# Limitations
The classifiers are biased and more likely to detect negative sentiment than positive sentiment. In an attempt to counter this, I reduced the impact of negativity on the total sentiment and raised the impact of positivity. However, this does not always work.

Furthermore, performing analysis on old NYT articles might produce an error due to a lack of a lead paragraph returned by the API

# To do
- ~Add more comments to make code more readable~
- ~Add support for NYT articles~

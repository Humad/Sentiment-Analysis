import app_keys as app_keys
import json
import codecs
import requests
from urllib.parse import urlencode
import sentiment_mod as s
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from functools import partial

# Used to stream live tweets
class listener(StreamListener):
    # On receiving new data
    def on_data(self, data):
        try: 
            tweet_data = json.loads(data)
            tweet = tweet_data["text"] # get text from tweet
            sentiment, confidence = s.sentiment(tweet)
            output_file = open("output.txt", "a")
            print("The tweet: ", tweet)
            
            # Write sentiment to file if confidence level is at least 80%
            if confidence >= 80:
                output_file.write(sentiment)
                output_file.write("\n")
                output_file.close()
                
            return True
        except:
            print("Error - Something went wrong while working with Tweepy")
    
    def on_error(self, status):
        print(status)

# Used to obtain NYT articles
def get_nyt_articles():
    keyword = toolbar_search_field.get()
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    
    parameters = {"api-key": nyt_key,
                  "q": keyword,
                  "begin_date": toolbar_begin_date_field.get(),
                  "end_date": toolbar_end_date_field.get(),
                  "sort": "oldest"}
    
    url = url + urlencode(parameters)
    response = requests.get(url).json()
    output_file = open("output.txt", "a")

    for details in response["response"]["docs"]:
        sentiment, confidence = s.sentiment(str(details["lead_paragraph"]))
        if (confidence >= 80):
            output_file.write(sentiment)
            output_file.write("\n")
    output_file.close()

# Search for keyword on Twitter
def get_search_results():
    keyword = toolbar_search_field.get()
    open("output.txt", "w").close() # erase all previous content in file

    if (get_data_from_twitter.get()):
        toolbar_begin_date_field.grid_forget()
        toolbar_end_date_field.grid_forget()
    else:
        toolbar_begin_date_field.grid(row=2, columnspan=2, column=0)
        toolbar_end_date_field.grid(row=2, columnspan=2, column=2)

    if (len(keyword) > 0):
        if (get_data_from_twitter.get()):
            twitter_stream.filter(track=[keyword], async=True)
            plot_graph()
        else:
            get_nyt_articles()
            plot_graph()

def plot_graph():
    anim = animation.FuncAnimation(fig, animate, interval=1000)
    ax.clear()
    plt.show()

# Updates x and y values
def animate(i):
    twitter_data = open("output.txt", "r").read()
    lines = twitter_data.split("\n")

    x_values = []
    y_values = []

    x = 0
    y = 0

    for line in lines:
        x = x + 1
        if "pos" in line:
            y = y + 1
        elif "neg" in line:
            y = y - 0.5

        x_values.append(x)
        y_values.append(y)

    ax.plot(x_values, y_values)


##########
main_window = Tk()

# keys and tokens
consumer_key = app_keys.get_consumer_key()
consumer_secret = app_keys.get_consumer_secret()
access_token = app_keys.get_access_token()
access_secret = app_keys.get_access_secret()
nyt_key = app_keys.get_nyt_key()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter_stream = Stream(auth, listener())
get_data_from_twitter = BooleanVar() # whether or not to get data from twitter

# Plotting the data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# ***** Toolbar *****
toolbar = Frame(main_window)
toolbar.grid(row=0)

toolbar_search_field = Entry(toolbar)
toolbar_search_field.grid(row=0, columnspan=4, column=0)
toolbar_search_button = Button(toolbar, text="Search", command=get_search_results)
toolbar_search_button.grid(row=0, column=5)

get_data_label = Label(toolbar, text="Get data from: ")
get_data_label.grid(row=1, columnspan=2, column=0)

# begin and end data fields
toolbar_begin_date_field = Entry(toolbar)
toolbar_end_date_field = Entry(toolbar)
toolbar_begin_date_field.grid(row=2, columnspan=2, column=0)
toolbar_end_date_field.grid(row=2, columnspan=2, column=2)


# twitter radio button
twitter_button = Radiobutton(toolbar,
                             text="Twitter",
                             variable=get_data_from_twitter,
                             value=True,
                             command=get_search_results)
twitter_button.grid(row=1, column=3)

# nyt radio button
nyt_button = Radiobutton(toolbar,
                         text="New York Times",
                         variable=get_data_from_twitter,
                         value=False,
                         command=get_search_results)
nyt_button.grid(row=1, column=5)

main_window.mainloop() # continuously show the window

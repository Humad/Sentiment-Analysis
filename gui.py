import app_keys as app_keys
import json
import sentiment_mod as s
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from functools import partial


class listener(StreamListener):
    def on_data(self, data):
        try: 
            tweet_data = json.loads(data)
            tweet = tweet_data["text"]
            sentiment, confidence = s.sentiment(tweet)
            twitter_file = open("twitter_output.txt", "a")
            print("The tweet: ", tweet)
            
            if confidence >= 80:
                twitter_file.write(sentiment)
                twitter_file.write("\n")
                twitter_file.close()
                
            return True
        except:
            print("error")

    def on_error(self, status):
        print(status)

def get_search_results(keyword):
    print("Searching for: ", keyword)
    print("Getting data from twitter? ", get_data_from_twitter.get())

    if (get_data_from_twitter.get() and len(keyword) > 0):
        twitter_stream.filter(track=[keyword], async=True)
        plot_graph()

def main():
    # ***** Toolbar *****
    toolbar = Frame(main_window)
    toolbar.grid(row=0)
    
    toolbar_search_field = Entry(toolbar)
    toolbar_search_field.grid(row=0, columnspan=4, column=0)
    toolbar_search_button = Button(toolbar, text="Search", command=lambda: get_search_results(toolbar_search_field.get()))
    toolbar_search_button.grid(row=0, column=5)

    get_data_label = Label(toolbar, text="Get data from: ")
    get_data_label.grid(row=1, columnspan=2, column=0)

    # twitter radio button
    twitter_button = Radiobutton(toolbar,
                                 text="Twitter",
                                 variable=get_data_from_twitter,
                                 value=True,
                                 command=lambda: get_search_results(toolbar_search_field.get()))
    twitter_button.grid(row=1, column=3)

    # nyt radio button
    nyt_button = Radiobutton(toolbar,
                             text="New York Times",
                             variable=get_data_from_twitter,
                             value=False,
                             command=lambda: get_search_results(toolbar_search_field.get()))
    nyt_button.grid(row=1, column=5)


main_window = Tk()

# keys and tokens
consumer_key = app_keys.get_consumer_key()
consumer_secret = app_keys.get_consumer_secret()
access_token = app_keys.get_access_token()
access_secret = app_keys.get_access_secret()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter_stream = Stream(auth, listener())

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def plot_graph():
    anim = animation.FuncAnimation(fig, animate, interval=1000)
    ax.clear()
    plt.show()

    
def animate(i):
    twitter_data = open("twitter_output.txt", "r").read()
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
            y = y - 0.2

        x_values.append(x)
        y_values.append(y)

    ax.plot(x_values, y_values)
    

get_data_from_twitter = BooleanVar() # whether or not to get data from twitter
open("twitter_output.txt", "w").close() # erase all previous content in 
main()
main_window.mainloop() # continuously show the window

# Twitter_utils
Rough selection of twitter utilities 

To use some of these you will need a twitter developer account and api keys.

To get those sign up for the twitter developer program then create an App.

https://developer.twitter.com/en/apps

Go to your "Keys and tokens" and copy your 'Consumer API keys' and 'Access token & access token secret' to someplace safe. *never upload these in your code you post online*


**Deleting a big bunch of tweets**
Currently twitter lets you retrieve up to 3,200 of your most recent tweets through an API call.
You can do with those what you wish as well as deleting them. 

If you delete say the oldest 200 tweets...  Tweets from your history does't fill that space up when you request all your tweets via an API call.  So if you want to delete a whole bunch more tweets.. You will have to request an archive of your tweets. 
This is older but the process is similar to how it is today: https://www.wikihow.com/Request-Your-Twitter-Archive-File 

Now that you have all your tweets easy right? 
Not so fast. Twitter moved from csv files to data stored in .js javascript files. 

That's where the *deletestatusfromfile.py* script comes in. To use it put all the tweets you want to delete in a file with one line per twitter id. In the script the name I'm using is: 'tweets_to_delete.txt' You also have to put your consumer and access token keys and secrets in the file.  

It's a python3 script and you will have to have python-twitter installed. https://github.com/bear/python-twitter  has installation instructions. 

I'm not sure of twitter's rate limiting on deletion so I was conservative with it. It deletes 1250 tweets at a time then sleeps for an hour.  It deletes roughly 25k+ tweets a day. 






**Viewing all the tweets in your archive**

This doesn't need developer api keys.

This is a very rough twitter archive viewer.

What it does is display all your tweets in chronological order and gives you a few lists you can show and copy from so you can take that twitter data and do stuff with it.

To use this put this html file in the unzipped folder you got from twitter that has your archive .js files in it.

Specifically it currently needs to be in the same folder as tweet.js and account.js



It's currently located here:   https://gist.github.com/johnaho/22cfd8d1768cd9e709715158b2194aa8


**Viewing all your likes**

This shows you all your likes in almost chronological order. The sort isn't all that great but it shows you your likes.
To use this put this html file in the unzipped folder you got from twitter that has your archive .js files in it.

https://github.com/johnaho/Twitter_utils/blob/master/likes.html

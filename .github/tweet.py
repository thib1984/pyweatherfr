from twython import Twython
# required libraries
import os

# get emails and password from environment variables
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_TOKEN)
print(ACCESS_TOKEN_SECRET)

twitter = Twython(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

message = "Hello world!"
twitter.update_status(status=message)
print("Tweeted: %s" % message)
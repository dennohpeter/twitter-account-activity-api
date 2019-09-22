from requests_oauthlib import OAuth1Session
import urllib
from django.conf import settings
import pprint

class Twitter_Activities:
    CONSUMER_KEY = settings.CONSUMER_KEY
    CONSUMER_SECRET = settings.CONSUMER_SECRET
    ACCESS_TOKEN = settings.ACCESS_TOKEN
    ACCESS_SECRET = settings.ACCESS_SECRET
    twitter = OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=ACCESS_TOKEN,
                            resource_owner_secret=ACCESS_SECRET)
    def register_crc(self):
        webhook_endpoint = urllib.parse.quote_plus('https://44c3b65c.ngrok.io/api/crc_callback')
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks.json?url={}'.format(
            webhook_endpoint)
        return self.twitter.post(url)

    def active_webhooks(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/webhooks.json'
        headers = {'Authorization': 'Bearer %s' % self.ACCESS_TOKEN }
        res = self.twitter.get(url, headers=headers)
        one = res.json()['environments']
        two = one[0]
        three = two['webhooks']
        four = three[0]

        return res.json()

    # Delete webhoook and create another whenever you change callback url. 
    # Reregistering callback on an already existing callback doesnt work.
    # def delete_webhook(self, webhook_id):
    #     url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks/1174811182877892608.json'
    #     headers = {
    #         'authorization': 'OAuth oauth_consumer_key="%s", oauth_token="%s"' % (self.CONSUMER_KEY, self.ACCESS_TOKEN)
    #     }
    #     res = self.twitter.delete(url, headers=headers)
    #     return res

    def delete_reply(self, body):
       tweet_create_events = body['tweet_create_events']
       tweet_create_events = tweet_create_events[0]
       tweet_id = tweet_create_events['id_str']
       initial_tweeter = tweet_create_events['in_reply_to_status_id']
       reply_tweet = tweet_create_events['text']

       url = 'https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(tweet_id)
       pprint.pprint(self.twitter)
       deleted_tweet = self.twitter.post(url)
       print('------------------deleted tweet----------------------')
       pprint.pprint(deleted_tweet.json())
       return deleted_tweet

    

    def deleted_tweet(self, tweet):
        return tweet


    def adding_subscription(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/subscriptions.json'
        headers = {
            'authorization': 'OAuth oauth_consumer_key="%s", oauth_token="%s"' % (self.CONSUMER_KEY, self.ACCESS_TOKEN)
        }
        res = self.twitter.post(url, headers=headers)
        return res

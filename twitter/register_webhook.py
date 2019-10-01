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
        webhook_endpoint = urllib.parse.quote_plus(
            'https://9e539681.ngrok.io/api/crc_callback')
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks.json?url={}'.format(
            webhook_endpoint)
        return self.twitter.post(url)

    def active_webhooks(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/webhooks.json'
        headers = {'Authorization': 'Bearer %s' % self.ACCESS_TOKEN}
        res = self.twitter.get(url, headers=headers)
        one = res.json()['environments']
        two = one[0]
        three = two['webhooks']
        four = three[0]

        return res.json()

    # Delete webhoook and create another whenever you change callback url.
    # Reregistering callback on an already existing callback doesnt work.
    def delete_webhook(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks/1176139247960633344.json'
        headers = {
            'authorization': 'OAuth oauth_consumer_key="%s", oauth_token="%s"' % (self.CONSUMER_KEY, self.ACCESS_TOKEN)
        }

        return self.twitter.delete(url, headers=headers)

    def delete_reply(self, content):
        tweet_body = content[0]
        tweet_id = tweet_body['id_str']
        in_reply_to_screen_name = tweet_body['in_reply_to_screen_name']
        in_reply_to_status_id = tweet_body['in_reply_to_status_id']
        reply_text = tweet_body['text'] + ':smiley:'
        delete_tweet_url = 'https://api.twitter.com/1.1/statuses/destroy/{}.json'.format(
            tweet_id)

        print('------------------deleting tweet----------------------')
        self.twitter.post(delete_tweet_url)

        return [in_reply_to_screen_name, in_reply_to_status_id, reply_text]

    def deleted_tweet(self, content):
        return content

    def tweet_reply(self, user_name, in_reply_to_status_id, message):
        tweet_reply_url = 'https://api.twitter.com/1.1/statuses/update.json'
        params = {
            'status': message,
            'in_reply_to_screen_name': user_name,
            'in_reply_to_status_id': in_reply_to_status_id
        }
        print('------------------making a reply----------------------')
        return self.twitter.post(tweet_reply_url, params=params)

    def adding_subscription(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/subscriptions.json'
        headers = {
            'authorization': 'OAuth oauth_consumer_key="%s", oauth_token="%s"' % (self.CONSUMER_KEY, self.ACCESS_TOKEN)
        }
        return self.twitter.post(url, headers=headers)

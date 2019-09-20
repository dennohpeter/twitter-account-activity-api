from requests_oauthlib import OAuth1Session
import urllib

class Twitter_Activities:
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_SECRET = '' 
    twitter = OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=ACCESS_TOKEN,
                            resource_owner_secret=ACCESS_SECRET)
    def register_crc(self):
        webhook_endpoint = urllib.parse.quote_plus('https://d85f9149.ngrok.io/api/crc_callback')
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks.json?url={}'.format(
            webhook_endpoint)
        return self.twitter.post(url)

    def register_events_callback(self):
        webhook_endpoint = urllib.parse.quote_plus('https://d85f9149.ngrok.io/api/twitter')
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/webhooks.json?url={}'.format(
            webhook_endpoint)
        return self.twitter.post(url)

    def active_webhooks(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/webhooks.json'
        headers = {'Authorization': 'Bearer %s' % self.ACCESS_TOKEN }
        res = self.twitter.get(url, headers=headers)
        return res.json()

    def adding_subscription(self):
        url = 'https://api.twitter.com/1.1/account_activity/all/notifier/subscriptions.json'
        headers = {
            'authorization': 'OAuth oauth_consumer_key="%s", oauth_token="%s"' % (self.CONSUMER_KEY, self.ACCESS_TOKEN)
        }
        res = self.twitter.post(url, headers=headers)
        return res.json()

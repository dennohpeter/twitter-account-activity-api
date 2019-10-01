from django.shortcuts import render
import base64
import hashlib
import hmac
import json
import pprint
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twitter.register_webhook import Twitter_Activities


def index(request):
    activity = Twitter_Activities()
    activity.register_crc()
    response = activity.delete_webhook()
    # print(response.text)
    r = activity.adding_subscription()
    # print(r.json())
    res = activity.active_webhooks()
    print(res)
    return render(request, 'index.html', {})


@csrf_exempt
def process_crc_callback(request):
    twitter = Twitter_Activities()
    if 'crc_token' in request.GET.keys():
        crc_token = request.GET.get('crc_token')
        TWITTER_CONSUMER_SECRET = settings.CONSUMER_SECRET
        # creates HMAC SHA-256 hash from incomming token and your consumer secret
        sha256_hash_digest = hmac.new(TWITTER_CONSUMER_SECRET.encode(
            'utf-8'), msg=crc_token.encode('utf-8'), digestmod=hashlib.sha256).digest()
        # construct response data with base64 encoded hash
        response = {
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('utf-8')
        }
        return HttpResponse(json.dumps(response))

    else:
        print('-------------------processing callback--------------------')
        tweet_event_body = json.loads(request.body)
        events = tweet_event_body.keys()
        if 'tweet_create_events' in events and tweet_event_body['tweet_create_events'][0]['in_reply_to_status_id']:
            content = tweet_event_body['tweet_create_events']
            [in_reply_to_screen_name, in_reply_to_status_id,
                reply_text] = twitter.delete_reply(content)  # small listening to events

            res = twitter.tweet_reply(
                in_reply_to_screen_name, in_reply_to_status_id, reply_text)
            print('-------------tweet reply response-------------------------')
            pprint.pprint(res.json())

        elif 'tweet_delete_events' in events:
            print('---------------the deleted tweet was----------------')
            content = tweet_event_body['tweet_delete_events']
            print(tweet_event_body)
            twitter.deleted_tweet(content)
        else:
            print('in last else')
            print(tweet_event_body)

        return HttpResponse(tweet_event_body)


def denno_api(request):
    response = request.POST
    print(response)

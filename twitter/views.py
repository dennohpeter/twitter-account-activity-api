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
    # r = activity.adding_subscription()
    res = activity.active_webhooks()
    # response = activity.delete_webhook(res)
    # print(response.text)
    # print(r.json())
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
        print("--------------------------------------------------------")
        tweet_event_body = json.loads(request.body)
        pprint.pprint(tweet_event_body)
        if 'tweet_create_events' in tweet_event_body.keys():
            twitter.delete_reply(tweet_event_body)

        elif 'tweet_delete_events' in :
            print('---------------the deleted tweet was----------------')

        
        return HttpResponse(tweet_event_body)

def denno_api(request):
    response = request.POST
    print(response)
    
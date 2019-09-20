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
    r = activity.adding_subscription()
    print(r)
    return render(request, 'index.html', {})


def process_crc_callback(request):
    crc_token = request.GET.get('crc_token')
    print(crc_token)
    TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
    # creates HMAC SHA-256 hash from incomming token and your consumer secret
    sha256_hash_digest = hmac.new(TWITTER_CONSUMER_SECRET.encode(
        'utf-8'), msg=crc_token.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # construct response data with base64 encoded hash
    response = {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('utf-8')
    }
    # returns properly formatted json response
    return HttpResponse(json.dumps(response))

@csrf_exempt
def event_listener(request):
    r = json.loads(request.body)
    pprint.pprint(r)
    return HttpResponse(r)

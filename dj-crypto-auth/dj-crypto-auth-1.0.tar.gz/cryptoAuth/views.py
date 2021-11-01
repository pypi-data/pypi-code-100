from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

import requests
import datetime
import json
from dateutil.parser import parse


from coinbase.wallet.client import OAuthClient
from coinbase.wallet.error import ExpiredTokenError, InvalidTokenError


from .models import ConnectedAccountBacklog



## COINBASE EXCHANGE

def confirm_auth_coinbase(request):
    if request.method == 'POST':
        pass
    code = request.GET['code']
    # print(code)
    host_ = request.META['HTTP_HOST']
    path_ = request.path

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.CRYPTO_AUTH_COINBASE_KEY,
        'client_secret': settings.CRYPTO_AUTH_COINBASE_SECRET,
        'redirect_uri': f'http://{host_}{path_}'
    }
    # print(f'{host_}{path_}')
    headers = {

    }
    r = requests.post('https://api.coinbase.com/oauth/token', data = data, headers=headers)
    cont_ = json.loads(r.content)
    if '20' in str(r.status_code):
    # token_ = cont_.access_token
    # refresh_ = cont_.refresh_token

        token_ = cont_['access_token']
        refresh_ = cont_['refresh_token']

        ## Add Token and Refresh to session.

        request.session['token'] = token_
        request.session['refresh'] = refresh_

        client = OAuthClient(token_, refresh_)
        accounts = client.get_accounts()
        for account in accounts['data']:
                if account['primary']:

                    dat = {
                        "name": account['name'],
                        "is_primary": account['primary'],
                        "balance": account['balance']['amount']+" "+account['currency'],
                        "id": account['id']
                    }
        txs = client.get_buys(dat['id'])
        demo = []
        
        if len(txs['data']) > 0:
            for data in txs['data']:
                dt_obj = parse(data['created_at'])
                ret = {
                    "c_date":str(dt_obj.strftime('%d/%m/%Y')),
                    "c_sym":str(data['amount']['currency']),
                    "c_qty":float(data['amount']['amount']),
                    "c_price":float(data['total']['amount']),
                }
                demo.append(ret)
        else:
            demo = None

        if settings.CRYPTO_AUTH_BACKLOGS:
        	back_log = ConnectedAccountBacklog.objects.create(user=request.user, summary=str(demo))
        	back_log.save()


        # return redirect(f'/portofolio?token={token_}&refresh={refresh_}')
        print(f'{str(reverse(settings.CRYPTO_AUTH_REDIRECT))}?token={token_}&refresh={refresh_}')
        
        return redirect(f'{reverse(settings.CRYPTO_AUTH_REDIRECT)}?token={token_}&refresh={refresh_}')
    else:
        print('error', r.status_code)
        messages.error(request, 'Please Re-authorize account. Session expired')
        return redirect(settings.CRYPTO_AUTH_REDIRECT)

    return redirect(f'/portofolio?token={token_}')


def get_accounts(req):

	try:
		token_ = req.session['token']
		refresh_ = req.session['refresh']
	except Exception as e:
		return JsonResponse({"error": "Please provide auth credentials"})
	client = OAuthClient(token_, refresh_)
	accounts = client.get_accounts()
	return accounts

def get_buys(req, data):

	try:
		token_ = req.session['token']
		refresh_ = req.session['refresh']
	except Exception as e:
		return JsonResponse({"error": "Please provide auth credentials"})
	client = OAuthClient(token_, refresh_)
	buys = client.get_buys(data)
	return buys

def get_user_data(req):

	try:
		token_ = req.session['token']
		refresh_ = req.session['refresh']
	except Exception as e:
		return JsonResponse({"error": "Please provide auth credentials"})
	client = OAuthClient(token_, refresh_)
	user = client.get_current_user()
	return user
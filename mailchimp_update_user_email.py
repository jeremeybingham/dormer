def update_mailchimp_user_email(guid):
    #module imports
    from flask import Flask, request
    from mailchimp3 import MailChimp
    import requests
    import json
    import hashlib
    import mysql.connector
    #file imports
    import config

    #define your mailchimp api route stuff
    client = MailChimp(mc_api = config.mc_api_key, mc_user='null')
    #RAMCO API connection
    url = (config.ramco_api_url)
    #define the type of request and parameters
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntity',
        'Entity':'contact',
        'GUID':'{}'.format(guid),
        'Attributes':'EMailAddress1,ramcosub_mar_sync_email'}
    response = requests.post(url,payload)
    raw = response.json()
    result = raw['Data']
    new_email = result['EMailAddress1']
    old_email = result['ramcosub_mar_sync_email']
    #convert the old email to lowercase
    lowercase_email = old_email.lower()
    #md5 hash it for mailchimp
    hashed = (hashlib.md5(lowercase_email.encode('utf-8')).hexdigest())
    #make the request to the mailchimp api
    client.lists.members.update(list_id = config.mc_list_id, subscriber_hash = hashed, data= {'email_address':new_email})
    return ('email updated in mailchimp successfully', 200)
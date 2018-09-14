#imports
#built-in
import requests, json, hashlib, mysql.connector, uuid, subprocess
#external
from flask import Flask, request, redirect, render_template, url_for
from flask_table import Table, Col, LinkCol, ButtonCol
from flask_qrcode import QRcode
from mailchimp3 import MailChimp
#file imports
import config, class_update, class_tags_update, meeting_update, meeting_tags_update, mailchimp_update_user_email, o365_user_update, event_touch, home_fn, result_fn, search_fn, search_result_fn, action_fn, lookup_fn

# initialize
app = Flask(__name__)
app.debug = False
qrcode = QRcode(app)


#### calendar functions ####

# class add/update for classes into the MySQL calendar db
@app.route('/update_class/', methods=['GET'])
def update_class():
    guid = request.args.get('guid')
    return class_update.update_class(guid)

# tags add/update for classes into the MySQL calendar db
@app.route('/update_class_tags/', methods=['GET'])
def update_class_tags():
    guid = request.args.get('guid')
    return class_tags_update.update_class_tags(guid)

# meeting add/update for meetings into the MySQL calendar db
@app.route('/update_meeting/', methods=['GET'])
def update_meeting():
    guid = request.args.get('guid')
    return meeting_update.update_meeting(guid)

# tags add/update for meetings into the MySQL calendar db
@app.route('/update_meeting_tags/', methods=['GET'])
def update_meeting_tags():
    guid = request.args.get('guid')
    return meeting_tags_update.update_meeting_tags(guid)
    
# calendar event + tags add/update for events entered via web form
@app.route('/touch_event', methods=['POST'])
def touch_event():
    event_json = request.get_json()
    return event_touch.touch_event(event_json)

    
#### 365 functions ####

# update a member mailcontact address in 365
@app.route('/update_o365_user/', methods=['GET'])
def update_o365_user():
    guid = request.args.get('guid')
    return o365_user_update.update_o365_user(guid)

    
#### mailchimp functions ####

@app.route('/update_mailchimp_user_email/', methods=['GET'])
def update_mailchimp_user_email():
    guid = request.args.get('guid')
    return mailchimp_update_user_email.update_mailchimp_user_email(guid)

    
#### mobile check-in functions ####    

## home
# main search page/universal search box
@app.route('/home/', methods=['GET', 'POST'])
def home():
    # get our event GUID from the URL
    event_guid = request.args.get('guid')

    # if this is on load, and a valid GUID is in the url, load page
    if request.method == 'GET':
        # load the main search page where you can scan qr code or type in name/nrds/email
        return home_fn.home(event_guid=event_guid)

    # once you POST the form/input something in the box, evaluate it to see what it is
    else:
        input_string = request.form['input_string']

        # input is not a guid if it's not exactly 36 characters - go to search
        if len(input_string) != 36:
            return redirect(url_for('search', event_guid=event_guid, input_string=input_string))

        # input is a guid if it's exactly 36 characters - go to result
        else:
            return redirect(url_for('result', event_guid=event_guid, input_string=input_string))

## result
# if a guid was entered, display the contact details of the person you're about to check in to confirm/change them
@app.route('/result', methods=['GET', 'POST'])
def result():

    # display info to print to badge
    if request.method == 'GET':
        return result_fn.result(event_guid=request.args.get('event_guid'), input_string=request.args.get('input_string'))

    # POST on form submit to check in contact and trigger print badge function
    else:
        # checks the state of the rpaci checkbox and sets values on submit
        if request.form.get('rpaci'):
            rpaci = 'true'
        else:
            rpaci = 'false'

        # checks the state of the rpacm checkbox and sets values on submit
        if request.form.get('rpacm'):
            rpacm = 'true'
        else:
            rpacm = 'false'

        # redirect to /action and send values
        return redirect(url_for('action', event_guid=request.args.get('event_guid'), reg_guid=request.form['reg_guid'], name=request.form['name'], city=request.form['city'], office=request.form['office'], rpaci=rpaci, rpacm=rpacm))

## search
# if a search string was entered, display the list of matching contacts from event registrations for this event
@app.route('/search', methods=['GET', 'POST'])
def search():

    # display the list to choose a contact from matches
    if request.method == 'GET':
        return search_fn.search(event_guid=request.args.get('event_guid'), input_string=request.args.get('input_string'))

    # once you click a "check in" button, POST the contact info back to /search_result
    else:
        return redirect(url_for('search_result', event_guid=request.args.get('event_guid'), contact_guid=request.form['contact_guid']))

@app.route('/search_result', methods=['GET', 'POST'])
def search_result():

    # display info to print to badge
    if request.method == 'GET':
        return search_result_fn.search_result(event_guid=request.args.get('event_guid'), contact_guid=request.args.get('contact_guid'))

    # POST on submit to check in contact and fire print badge function
    # checks the state of the rpaci checkbox and sets values on submit
    else:
        if request.form.get('rpaci'):
            rpaci = 'true'
        else:
            rpaci = 'false'

        if request.form.get('rpacm'):
            rpacm = 'true'
        else:
            rpacm = 'false'

        return redirect(url_for('action', event_guid=request.args.get('event_guid'), reg_guid=request.form['reg_guid'], name=request.form['name'], city=request.form['city'], office=request.form['office'], rpaci=rpaci, rpacm=rpacm))

## action
# marks the contact attended in the meeting registration, sends badge to the printer, displays a success message, then redirects home
@app.route('/action', methods=['GET'])
def action():
    return action_fn.action(event_guid=request.args.get('event_guid'), reg_guid=request.args.get('reg_guid'), name=request.args.get('name'), city=request.args.get('city'), office=request.args.get('office'), rpaci=request.args.get('rpaci'), rpacm=request.args.get('rpacm'))

# member self-lookup for QR codes
@app.route('/lookup', methods=['GET', 'POST'])
def lookup():

    # load the main self-serve lookup page
    if request.method == 'GET':
            return render_template('lookup.html')

    # post search
    else:
        return redirect(url_for('lookup_results', input_string=request.form['input_string']))

@app.route('/lookup_results', methods=['GET', 'POST'])
def lookup_results():

    # load the list of matches
    if request.method == 'GET':
        input_string=request.args.get('input_string')
        return lookup_fn.lookup(input_string=input_string)
    # posts the chosen contact to fetch details
    else:
        return redirect(url_for('lookup_qr', contact_guid=request.form['contact_guid']))

# returns the qr code and verification info
@app.route('/lookup_qr', methods=['GET'])
def lookup_qr():
    return render_template('lookup_qr.html', contact_guid=request.args.get('contact_guid'))

    
#### committee nomination form functions ####

@app.route('/rank/', methods=['GET', 'POST'])
def rank():
    guid = request.args.get('guid')
    url = config.ramco_api_url
    payload = {
    'key':config.ramco_api_key,
    'Operation':'GetEntities',
    'Entity':'cobalt_committeenomination',
    'Attributes':'cobalt_committeenominationid,cobalt_CommitteeId',
    'Filter':'statuscode<eq>1 AND cobalt_NomineeId<eq>#{}#'.format(guid)
        }
    response = requests.post(url,payload)
    raw = response.json()
    data = raw['Data']
    dict0 = {} # set dict
    list_dict0 = [] # set
    count = 0 # set count to start at 0
    for loop0 in data:
        raw1 = data[count]
        count += 1 # move to the next one, count up
        raw2 = raw1['cobalt_CommitteeId']
        event_name0 = raw2['Display']
        event_id0 = raw1['cobalt_committeenominationId']
        dict0[event_name0] = event_id0
        list_dict0.append(dict0) # adds this dict to the list
        dict0 = {}
    noms = list_dict0
    return render_template('rank.html', noms=noms, guid=guid)

@app.route('/submit_rank/', methods=['GET', 'POST'])
def submit_rank():
    form_input = request.form.to_dict()
    input = [{k: v} for (k, v) in form_input.items()]
    url = config.ramco_api_url
    operation = 'UpdateEntity'
    entity = 'cobalt_committeenomination'
    for all in input:
        for id, val in all.items():
            guid = '{}'.format(id)
            attr = 'ramcosub_interest_level='+'{}'.format(val)
            payload = {'key':config.ramco_api_key,'Operation':operation,'entity':entity,'GUID':guid,'AttributeValues':attr}
            response = requests.post(url,payload)
            reply = response.json()
    return render_template('success.html', reply=reply)
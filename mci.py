## imports
from flask import Flask, request, render_template, redirect, url_for
from flask_qrcode import QRcode
import home_fn, result_fn, search_fn, search_result_fn, action_fn, lookup_fn

app = Flask(__name__)
qrcode = QRcode(app)

## index
@app.route('/')
def index():
    return 'RAMCO mobile check-in API endpoint'

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

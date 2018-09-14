def home(event_guid):
    from flask import render_template
    import requests
    import config

    # api call to fetch event name and date to display
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntity',
        'Entity':'cobalt_meeting',
        'GUID':event_guid,
        'Attributes':'cobalt_BeginDate,cobalt_name'
        }
    result = requests.post(config.ramco_api_url,payload).json()

    # evaluate response code in api reply to verify it was successful, return an error if not
    if result['ResponseCode'] !=200:
        return('The GUID in the URL does not match an event in RAMCO. Please check your URL in the event page.')
	
	# render the main page template and input box
    else:
        title = result['Data']['cobalt_name']
        return render_template('home.html', event_guid=event_guid, title=title)
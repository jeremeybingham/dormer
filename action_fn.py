def action(reg_guid, event_guid, name, city, office, rpaci, rpacm):
    from flask import render_template
    import requests
    import config

    # api call to mark registration as attended
    payload = {
    'key':config.ramco_api_key,
    'Operation':'UpdateEntity',
    'Entity':'cobalt_meetingregistration',
    'GUID':reg_guid,
    'AttributeValues':'cobalt_attendedmeeting=True,ramcosub_mobilecheckin=True'
    }
    reply = requests.post(config.ramco_api_url,payload).json()

    if rpacm == 'true':
        rpac = 'RPAC Major Investor'

    elif rpaci == 'true':
        rpac = 'RPAC Investor'

    else:
        rpac = ''

    with open('/home/marealtors/mysite/mcidemo/static/uploads/badge.label', 'r') as xml:
        badge = xml.read()

    return render_template('action.html', reply=reply, reg_guid=reg_guid, event_guid=event_guid, name=name, city=city, office=office, rpac=rpac, badge=badge)

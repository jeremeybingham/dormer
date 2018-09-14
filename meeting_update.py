def update_meeting(guid):
    #module imports
    from flask import Flask, request
    import requests
    import json
    import hashlib
    import mysql.connector
    import uuid
    #file imports
    import config
    
    #mysql db connection info
    mysql = mysql.connector.connect(
    user = config.mysql_user,
    password = config.mysql_pw,
    host = config.mysql_host,
    database = config.mysql_db) #specify your db here
    cursor = mysql.cursor()
    
    #RAMCO API connection info and request
    url = (config.ramco_api_url)
    #define the type of request and parameters
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntity',
        'Entity':'cobalt_meeting',
        'GUID':'{}'.format(guid),
        'Attributes':'ModifiedOn,cobalt_name,cobalt_meetingId,cobalt_Description,cobalt_Location,cobalt_BeginDate,cobalt_EndDate,cobalt_Address1Line1,cobalt_Address1Line2,cobalt_Address1City,cobalt_Address1StateProvinceId,cobalt_Address1PostalCode,cobalt_Directions,cobalt_OutsideProviderLink,cobalt_OutsideProviderMessage,cobalt_PublishtoPortal'
        }
    response = requests.post(url,payload)
    raw = response.json()
    event_data = raw['Data']
    event_guid = event_data['cobalt_meetingId']
    #find the event in MySQL db if exists and fetch its unique ID - specify your table in FROM
    cursor.execute ("SELECT event_key FROM events WHERE source_unique_id = '{}'".format(event_guid))
    #this value (if exists) is used below - evaluates if db_list != [] - should exist if the meeting is in RAMCO db
    db_list = cursor.fetchall()

    #set your variables
    event_name = event_data['cobalt_name']
    event_mdate = event_data['ModifiedOn']
    event_mdate_v = event_mdate['Value']
    event_bdate = event_data['cobalt_BeginDate']
    event_bdate_v = event_bdate['Value']
    event_edate = event_data['cobalt_EndDate']
    event_edate_v = event_edate['Value']
    event_opl = event_data['cobalt_OutsideProviderLink']
    event_opm = event_data['cobalt_OutsideProviderMessage']
    event_publish = event_data['cobalt_PublishtoPortal']
    event_description = 'fix event descriptions ASAP'
    event_location = event_data['cobalt_Location']
    event_directions = event_data['cobalt_Directions']
    event_address_1 = event_data['cobalt_Address1Line1']
    event_address_2 = event_data['cobalt_Address1Line2']
    event_address_city = event_data['cobalt_Address1City']
    event_address_state = event_data['cobalt_Address1StateProvinceId']
    event_address_state_v = event_address_state['Display']
    event_address_zip = event_data['cobalt_Address1PostalCode']
    event_source_event_type = 'MEETING' #event type in RAMCO, only valid values are CLASS and MEETING, set accordingly
    event_source_code = config.association_id #set in config.py
    #builds a portal url for the event_registration_link field from config value string & GUID
    prelink = config.portal_url_meeting
    endlink = (event_guid)
    event_registration_link = prelink + endlink
       
    if db_list != []:
        match = ("UPDATE events SET last_modified=CURRENT_TIMESTAMP, event_name='{}', source_modified_date='{}', begin_date='{}', end_date='{}', publish_online='{}', location='{}', description='{}', directions='{}', address_1='{}', address_2='{}', address_city='{}', address_state='{}', address_zip='{}', source_event_type='{}', registration_link='{}', other_provider_link='{}', other_provider_message='{}', source_association_code='{}' WHERE source_unique_id='{}'".format(event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state_v, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_source_code, event_guid))
        cursor.execute(match)
    else:
        sql_uid = 'E' + str(uuid.uuid4()) #builds a unique id we can use
        #builds the INSERT string to send to the sql db
        nomatch = ("INSERT INTO events (event_key, last_modified, event_name, source_modified_date, begin_date, end_date, publish_online, location, description, directions, address_1, address_2, address_city, address_state, address_zip, source_event_type, registration_link, other_provider_link, other_provider_message, source_unique_id, source_association_code) VALUES ('{}', CURRENT_TIMESTAMP,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(sql_uid, event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state_v, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_guid, event_source_code))
        cursor.execute(nomatch)
    
    mysql.commit()
    mysql.close()
    return ('meeting added/updated successfully', 200)
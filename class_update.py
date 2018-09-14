def update_class(guid):
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
    
    #RAMCO API connection info
    url = (config.ramco_api_url)
    #define the type of request and parameters
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntity',
        'Entity':'cobalt_class',
        'GUID':'{}'.format(guid),
        'Attributes':'ModifiedOn,cobalt_name,cobalt_classId,cobalt_ClassBeginDate,cobalt_ClassEndDate,cobalt_OutsideProviderLink,cobalt_PublishtoPortal'
        }
    response = requests.post(url,payload)
    raw = response.json()
    event_data = raw['Data']
    event_guid = event_data['cobalt_classId']
    
    #find the event in MySQL db if exists and fetch its unique ID - specify your table in FROM
    cursor.execute ("SELECT event_key FROM events WHERE source_unique_id = '{}'".format(event_guid))
    #this value (if exists) is used below - evaluates if db_list != [] - should exist if the class is in RAMCO db
    db_list = cursor.fetchall()

    #set your variables
    event_name = event_data['cobalt_name']
    event_mdate = event_data['ModifiedOn']
    event_mdate_v = event_mdate['Value']
    event_bdate = event_data['cobalt_ClassBeginDate']
    event_bdate_v = event_bdate['Value']
    event_edate = event_data['cobalt_ClassEndDate']
    event_edate_v = event_edate['Value']
    event_opl = event_data['cobalt_OutsideProviderLink']
    event_publish = event_data['cobalt_PublishtoPortal']
    #hardcoded variables, for now
    event_description = 'none' #reserved for future use
    event_location = 'none' #reserved for future use
    event_directions = 'none' #reserved for future use
    event_address_1 = 'none' #reserved for future use
    event_address_2 = 'none' #reserved for future use
    event_address_city = 'none' #reserved for future use
    event_address_state = 'none' #reserved for future use
    event_address_zip = 'none' #reserved for future use
    event_opm = 'none' #reserved for future use
    event_source_event_type = 'CLASS' #event type in RAMCO, only valid values are CLASS and MEETING, set accordingly
    event_source_code = config.association_id #set in config.py
    #builds a  portal url for the event_registration_link field from config value string & GUID
    prelink = config.portal_url_class
    endlink = (event_guid)
    event_registration_link = prelink + endlink

    if db_list != []:
        match = ("UPDATE events SET last_modified=CURRENT_TIMESTAMP, event_name='{}', source_modified_date='{}', begin_date='{}', end_date='{}', publish_online='{}', location='{}', description='{}', directions='{}', address_1='{}', address_2='{}', address_city='{}', address_state='{}', address_zip='{}', source_event_type='{}', registration_link='{}', other_provider_link='{}', other_provider_message='{}', source_association_code='{}' WHERE source_unique_id='{}'".format(event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_source_code, event_guid,))
        cursor.execute(match)
    else:
        sql_uid = 'E' + str(uuid.uuid4()) #builds a unique id we can use
        #sql procedure if it's not found
        nomatch = "INSERT INTO events (event_key, last_modified, event_name, source_modified_date, begin_date, end_date, publish_online, location, description, directions, address_1, address_2, address_city, address_state, address_zip, source_event_type, registration_link, other_provider_link, other_provider_message, source_unique_id, source_association_code) VALUES ('{}', CURRENT_TIMESTAMP,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(sql_uid, event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_guid, event_source_code)
        cursor.execute(nomatch)

    #commits the data to memory and writes to the sql db
    mysql.commit()
    mysql.close()
    return ('class added/updated successfully', 200)
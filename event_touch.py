def touch_event(event_json):
    #module imports
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

    #pull out the 'Data' and 'Tags' sections
    event_data = event_json['Data']
    event_tags = event_json['Tags']

    # append additional tags to 'event_tags' based input
    if event_data['source_code'] == '4475': #berkshires
        source_tag = 'T0b893a3f-6cf6-408d-9b2c-2dd2d92d9884'
    elif event_data['source_code'] == '4480': #cape & isls
        source_tag = 'T3a37bced-e839-4d21-84de-8eed9672d09a'
    elif event_data['source_code'] == '4495': #greater boston
        source_tag = 'T5b331480-2996-41f0-8468-2f93d856d317'
    elif event_data['source_code'] == '4500': #tri-county
        source_tag = 'T62dc4c11-8831-4457-bc67-898b08f4bb54'
    elif event_data['source_code'] == '4505': #fall river
        source_tag = 'T5a8d7a81-f22d-4df6-b3ca-57d5872a5010'
    elif event_data['source_code'] == '4515': #southeastern mass
        source_tag = 'T441ec2a3-f5fc-4fc8-8095-7d57ee3028a1'
    elif event_data['source_code'] == '4520': #newburyport
        source_tag = 'T660bb381-850e-440a-a97d-1f01e3d28e0f'
    elif event_data['source_code'] == '4525': #pioneer valley
        source_tag = 'Ta95aedf9-af90-4413-8460-ad4d0c3766a7'
    elif event_data['source_code'] == '4530': #central mass
        source_tag = 'T9c456422-ef81-44f5-989b-1d117991da7a'
    elif event_data['source_code'] == '4540': #north shore
        source_tag = 'T1bef38fb-5246-4ab0-a298-0b1b9e822b64'
    elif event_data['source_code'] == '4542': #commercial
        source_tag = 'Tb36a6f88-d766-42b6-b6ad-5a59cc2fbf24'
    elif event_data['source_code'] == '4545': #north central
        source_tag = 'Tcd198a7b-b5df-4a66-99e3-d2950901c34d'
    elif event_data['source_code'] == '4550': #south shore
        source_tag = 'T7e340200-9192-44b4-b4f8-44b431dd1385'
    elif event_data['source_code'] == '4560': #northeast
        source_tag = 'T9da47fc4-c5cb-44ce-a265-e457f8f08198'
    else: #default to MAR on failure
        source_tag = 'Tc6035174-d92e-4b7a-af7e-1a00f1810bc7'
    event_tags.append(source_tag)
    #add 'Local Association Event' tag to all webform submitted events
    event_tags.append('T411b97bd-4361-4676-bc3a-318795bd4719')

    #set your vars
    event_guid = event_data['meetingId']
    event_name = event_data['name']
    event_mdate_v = event_data['ModifiedOn']
    event_bdate_v = event_data['ClassBeginDate']
    event_edate_v = event_data['ClassEndDate']
    event_opl = event_data['OutsideProviderLink']
    event_publish = event_data['PublishtoPortal']
    event_description = event_data['Description']
    event_location = event_data['Location']
    event_directions = event_data['Directions']
    event_address_1 = event_data['Address1Line1']
    event_address_2 = event_data['Address1Line2']
    event_address_city = event_data['Address1City']
    event_address_state = event_data['Address1StateProvinceId']
    event_address_zip = event_data['Address1PostalCode']
    event_opm = event_data['OutsideProviderMessage']
    event_source_code = event_data['source_code']
    event_registration_link = event_data['registration_link']
    event_source_event_type = 'WEBFORM'

    #find the event in MySQL db if exists and fetch its unique ID - specify your table in FROM
    cursor.execute ("SELECT event_key FROM events WHERE source_unique_id = '{}'".format(event_guid))
    db_list = cursor.fetchall()

    if db_list != []:
        #sql procedure if it's found
        match = ("UPDATE events SET last_modified=CURRENT_TIMESTAMP, event_name='{}', source_modified_date='{}', begin_date='{}', end_date='{}', publish_online='{}', location='{}', description='{}', directions='{}', address_1='{}', address_2='{}', address_city='{}', address_state='{}', address_zip='{}', source_event_type='{}', registration_link='{}', other_provider_link='{}', other_provider_message='{}', source_association_code='{}' WHERE source_unique_id='{}'".format(event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_source_code, event_guid,))
        print(match)
        cursor.execute(match)
    else:
        #sql procedure if it's not found
        #builds a unique id for the event
        sql_uid = 'E' + str(uuid.uuid4())
        nomatch = "INSERT INTO events (event_key, last_modified, event_name, source_modified_date, begin_date, end_date, publish_online, location, description, directions, address_1, address_2, address_city, address_state, address_zip, source_event_type, registration_link, other_provider_link, other_provider_message, source_unique_id, source_association_code) VALUES ('{}', CURRENT_TIMESTAMP,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(sql_uid, event_name, event_mdate_v, event_bdate_v, event_edate_v, event_publish, event_location, event_description, event_directions, event_address_1, event_address_2, event_address_city, event_address_state, event_address_zip, event_source_event_type, event_registration_link, event_opl, event_opm, event_guid, event_source_code)
        print(nomatch)
        cursor.execute(nomatch)

    #loop through all your event tags and create a db insert for each    
    for tag_key in event_tags:
        cursor.execute("SELECT event_key FROM events WHERE source_unique_id='{}'".format(event_guid))
        fetched = cursor.fetchone()
        event_key = ''.join(fetched)
        
        #is there a unique event tag that has both? 
        cursor.execute("SELECT event_tag_key FROM event_tags WHERE event_tags.event_key='{}' AND event_tags.tag_key='{}'".format(event_key, tag_key))
        matched_event_tag_key = cursor.fetchone()
            
        if matched_event_tag_key != None:
            pass
            
        else: #build an insert statement to create a new event_tag row
            sql_uid = 'X' + str(uuid.uuid4())
            insert = ("INSERT INTO event_tags (event_tag_key,event_key,tag_key,last_modified) VALUES ('{}','{}','{}',CURRENT_TIMESTAMP)".format(sql_uid, event_key, tag_key))
            cursor.execute(insert)

    #commit and close your db connection    
    mysql.commit()
    mysql.close()
    return ('Calendar Event and tags added/updated successfully', 201)
def update_class_tags(guid):
    #module imports
    from pprint import pprint
    import requests
    import json
    import hashlib
    import mysql.connector
    import uuid
    #file imports
    import config

    #db connection set as 'mysql', connection info stored in config file
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
        'Entity':'cobalt_class',
        'GUID':'{}'.format(guid),
        'Attributes':'cobalt_cobalt_tag_cobalt_class/cobalt_tagId'
        }
    response = requests.post(url,payload)
    raw = response.json()
    event_tag_set = raw['Data']['cobalt_cobalt_tag_cobalt_class']
    #pprint(event_tag_set)

    count = 0
    for tag in event_tag_set:
        tag = event_tag_set[count]
        count = count + 1
        tag_id = tag['cobalt_tagId']
        #print(tag_id) #ramco tag guid
        
        #does this event exist?
        cursor.execute("SELECT event_key FROM events WHERE source_unique_id='{}'".format(guid))
        fetched_event_key = cursor.fetchone()
        #print(fetched_event_key) #sql event uid
        
        if fetched_event_key != None:
            matched_event_key=(fetched_event_key[0]) #iterate through the matches
        pass

        #does the tag exist?
        cursor.execute("SELECT tag_key FROM tags WHERE source_unique_id='{}'".format(tag_id)) #find the sql tag uid for each tag
        fetched_tag_key = cursor.fetchone() #the tag sql uid
        #print(fetched_tag_key)
        
        if fetched_tag_key != None:
            matched_tag_key=(fetched_tag_key[0]) #iterate through the matches
        pass
            
        #is there a unique event tag that has both? 
        cursor.execute("SELECT event_tag_key FROM event_tags WHERE event_tags.event_key='{}' AND event_tags.tag_key='{}'".format(matched_event_key,matched_tag_key))
        matched_event_tag_key = cursor.fetchone()
        #print(matched_event_tag_key)
        
        if matched_event_tag_key != None:
            pass
        
        else: #build an insert statement to create a new event_tag row
            new_event_tag_key = 'X' + str(uuid.uuid4()) #assign a new unique ID
            insert = ("INSERT INTO event_tags (event_tag_key,event_key,tag_key,last_modified) VALUES ('{}','{}','{}',CURRENT_TIMESTAMP)".format(new_event_tag_key, matched_event_key, matched_tag_key))
            #pprint(insert)
            cursor.execute(insert)
            
    mysql.commit()
    mysql.close()
    return ('class tags added/updated successfully', 200)
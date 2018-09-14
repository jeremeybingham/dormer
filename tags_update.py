def update_tags():
    #module imports
    from flask import Flask, request
    import requests
    import json
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
        'Operation':'GetEntities',
        'Entity':'cobalt_tag',
        'Attributes':'cobalt_name,cobalt_tagid,ramco_ramco_tagcategory_cobalt_tag_tagcategoryid/ramco_name,ramco_ramco_tagcategory_cobalt_tag_tagcategoryid/ramco_tagcategoryid'
        }
    response = requests.post(url,payload)
    raw = response.json()
    tag_set = raw['Data']
    
    #define your variables from tag_set
    for tag_data in tag_set:
        tag_name = tag_data['cobalt_name']
        tag_id = tag_data['cobalt_tagId']
        tag_category = tag_data['ramco_ramco_tagcategory_cobalt_tag_tagcategoryid']
        
        #iterate through tag set and see if tags exist
        for cat_data in tag_category:
            cat_name = tag_category['ramco_name']
            cat_id = tag_category['ramco_tagcategoryId']
            cursor.execute("SELECT tag_key FROM tags WHERE source_unique_id='{}'".format(tag_id))
            fetched_tag_key_result = cursor.fetchone()
            
            #iterate through tag set and assign to db
            if fetched_tag_key_result is not None:
                fetched_tag_key = fetched_tag_key_result[0]
                update = ("UPDATE tags SET name= '{}', tag_category_name= '{}', tag_category_id= '{}' WHERE tag_key='{}'".format(tag_name,cat_name,cat_id,fetched_tag_key))
                cursor.execute(update)
            else:
                new_tag_key = 'T' + str(uuid.uuid4()) #assign a new unique ID
                #builds an insert statement to create a new event_tag row
                insert = ("INSERT INTO tags (tag_key,name,source_unique_id,tag_category_name,tag_category_id,last_modified) VALUES ('{}','{}','{}','{}','{}',CURRENT_TIMESTAMP)".format(new_tag_key,tag_name,tag_id,cat_name,cat_id))
                cursor.execute(insert)         
    mysql.commit()
    mysql.close()
    return ('tags added/updated successfully', 200)
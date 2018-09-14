def search(event_guid, input_string):
    from flask import render_template
    import requests
    import config

    # create an empty list 'contact_list'
    contact_list = []

    # get all the contacts where 'input_string' matches part of a filter field, up to 10 results
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntities',
        'Entity':'contact',
        'Attributes':'ContactId',
        'Filter':f'FullName<sc>#{input_string}# OR EMailAddress1<sc>#{input_string}# OR ramco_nrdsid<sc>#{input_string}#',
        'MaxResults':'10'
        }
    result = requests.post(config.ramco_api_url,payload).json()

    # evaluate response code in api reply to verify it was successful, return an error if not
    if result['ResponseCode'] !=200:
        return render_template('error.html', event_guid=event_guid, input_string=input_string)
    else:
        contacts = result['Data']

        # for all contacts found above, get meeting registrations for this meeting if any exist
        for guids in contacts:
            contact_id = guids['ContactId']
            r = 'cobalt_contact_cobalt_meetingregistrations' # just a prefix to save space
            payload2 = {
                'key':config.ramco_api_key,
                'Operation':'GetEntities',
                'Entity':'cobalt_meetingregistration',
                'Attributes':f'cobalt_meetingregistrationId,{r}/FirstName,{r}/LastName,{r}/EMailAddress1,{r}/Address1_City,{r}/ramco_nrdsid,{r}/ContactId,{r}/ParentCustomerId,{r}/ramco_nrdsprimaryassociation,{r}/ramcosub_2018ConferenceRegistrationType',
                'Filter':f'cobalt_contactid<eq>#{contact_id}# AND cobalt_meetingid<eq>#{event_guid}#'
                }
            registrations = requests.post(config.ramco_api_url,payload2).json()

            for key,value in registrations.items():
                if 'Data' in key:
                    temp = {}
                    val = (value[0])
                    temp['first_name'] = (val[f'{r}']['FirstName'])
                    temp['last_name'] = (val[f'{r}']['LastName'])
                    temp['email'] = (val[f'{r}']['EMailAddress1'])
                    temp['city'] = (val[f'{r}']['Address1_City'])
                    temp['nrds_id'] = (val[f'{r}']['ramco_nrdsid'])
                    temp['contact_guid'] = (val[f'{r}']['ContactId'])
                    temp['reg_id'] = (val['cobalt_meetingregistrationId'])
                    temp['office'] = (val[f'{r}']['ParentCustomerId']['Display'])
                    temp['reg_type'] = (val[f'{r}']['ramcosub_2018ConferenceRegistrationType']['Display'])

                    # adds this dict to the list of dicts 'contact_list', defined above
                    contact_list.append(temp)

        # verify you've put something into 'contact_list' / there was at least 1 registration matching 'input_string'
        if not contact_list:
            return render_template('error.html', event_guid=event_guid, input_string=input_string)
        # pass your list to the 'search.html' template to display it
        else:
            return render_template('search.html', event_guid=event_guid, input_string=input_string, contact_list=contact_list)
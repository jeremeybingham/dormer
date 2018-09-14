def search_result(event_guid, contact_guid):
    from flask import render_template
    import requests
    import config

    input_string = contact_guid

    # just a prefix to save space below
    r = 'cobalt_contact_cobalt_meetingregistrations'

    # RAMCO API request
    payload = {
        'key':config.ramco_api_key,
        'Operation':'GetEntities',
        'Entity':'cobalt_meetingregistration',
        'Attributes':f'cobalt_meetingregistrationId,{r}/FirstName,{r}/LastName,{r}/Address1_City,{r}/ramcosub_CurrentYearRPACMajorInvestor,{r}/ramcosub_2018ConferenceRegistrationType,{r}/ramcosub_2015rpacmajorinvestor,{r}/ParentCustomerId',
        'Filter':f'cobalt_contactid<eq>#{input_string}# AND cobalt_meetingid<eq>#{event_guid}#'
        }
    data_id = requests.post(config.ramco_api_url,payload).json().get('Data')[0]
    data = data_id.get('cobalt_contact_cobalt_meetingregistrations')

    # set your fields
    reg_guid = data_id.get('cobalt_meetingregistrationId')
    first = data.get('FirstName')
    last = data.get('LastName')
    city = data.get('Address1_City')
    office = data.get('ParentCustomerId').get('Display')
    rpaci = data.get('ramcosub_2015rpacmajorinvestor')
    if rpaci == 'true':
        rpaci_c = 'checked' # sets 'checked' variable so we can display this as a checkbox later
    else:
        rpaci_c = ''
    rpacm = data.get('ramcosub_CurrentYearRPACMajorInvestor')
    if rpacm == 'true':
        rpacm_c = 'checked' # sets 'checked' variable so we can display this as a checkbox later
    else:
        rpacm_c = ''

    return render_template('result.html', event_guid=event_guid,input_string=input_string,reg_guid=reg_guid,first=first,last=last,city=city,rpaci=rpaci,rpacm=rpacm,office=office,rpaci_c=rpaci_c, rpacm_c=rpacm_c)
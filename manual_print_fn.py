def manual_print(name, office, rpaci, rpacm):
    from flask import render_template

    if rpacm == 'true':
        rpac = 'RPAC Major Investor'

    elif rpaci == 'true':
        rpac = 'RPAC Investor'

    else:
        rpac = ''

    with open('/home/marealtors/mysite/mcidemo/static/uploads/badge.label', 'r') as xml:
        badge = xml.read()

    return render_template('manual_print.html', name=name, office=office, rpac=rpac, badge=badge)
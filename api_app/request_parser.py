from api_app.actions import get_actions


def computer_update_request(request, company):
    kwargs = {}
    if request.method == "POST":
        if 'serialnumber' in request.POST:
            kwargs['sernumb'] = request.POST['serialnumber']
        else:
            return None
        if 'computername' in request.POST:
            kwargs['name'] = request.POST['computername']
        if 'opsystem' in request.POST:
            kwargs['opsystem'] = request.POST['opsystem']
        if 'manuf' in request.POST:
            kwargs['manuf'] = request.POST['manuf']
        if 'model' in request.POST:
            kwargs['model'] = request.POST['model']
        if 'contype' in request.POST:
            kwargs['contype'] = request.POST['contype']
        if 'iptype' in request.POST:
            kwargs['iptype'] = request.POST['iptype']
        if 'ipaddress' in request.POST:
            kwargs['ipaddress'] = request.POST['ipaddress']
        if 'macaddress' in request.POST:
            kwargs['macaddress'] = request.POST['macaddress']
        kwargs['company'] = company
        return kwargs
    else:
        return None

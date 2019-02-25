from models import client
from models import computers
from models import networkequipment
from models import description
from models import person


def form_all_clients_data():
    try:
        all_clients = client.Client.objects.all().order_by('name')
    except Exception as err:
        return None
    result = []
    for cl in all_clients:
        result.append({'clientobj': cl, 'clientname':cl.name, 'clientphonenumber':cl.phone})
    return result

def form_client_data(clientid):
    try:
        cur_client = client.Client.objects.get(id=clientid)
    except Exception as err:
        return None
    data = {}
    data['clientdescription'] = cur_client.description
    data['clientname'] = cur_client.name
    data['clientid'] = cur_client.id
    data['clientphonenumber'] = cur_client.phone
    data['clientaddress'] = cur_client.address
    data['clientcomputers'] = form_client_computers_data(cur_client)
    return data


def form_client_computers_data(client):
    data=[]
    try:
        comps = computers.Computer.objects.filter(company=client)
    except Exception as err:
        return []
    return comps


def form_computer_data(computerid):
    data={}
    return data
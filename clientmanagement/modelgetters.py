from models import client
from models import computers
from models import printer
from models import networkequipment
from models import person
from models import domain
from models import router


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
    data['clientnetwork'] = form_client_network_equipment_data(cur_client)
    data['clientcomputers'] = form_client_computers_data(cur_client)
    data['clientprinters'] = form_client_printers_data(cur_client)
    data['clientdomain'] = domain.getDomain(cur_client)
    data['clientrouter'] = router.getRouter(cur_client)
    data['clientpeople'] = form_client_people_data(cur_client)
    return data


def form_client_network_equipment_data(client):
    data=[]
    try:
        neteq = networkequipment.NetworkEquipment.objects.filter(company=client).order_by('ip_address', 'mac_address')
    except Exception as err:
        return []
    return neteq


def form_client_computers_data(client):
    data=[]
    try:
        comps = computers.Computer.objects.filter(company=client)
    except Exception as err:
        return []
    return comps


def form_client_printers_data(client):
    data=[]
    try:
        pr = printer.Printer.objects.filter(company=client)
    except Exception as err:
        return []
    return pr


def form_client_people_data(client): 
    data=[]
    try:
        people = client.employees.all().order_by('firstname', 'lastname')
    except Exception as err:
        return []
    return people


def form_computer_data(computerid):
    data={}
    return data
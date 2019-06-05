from models import computers
from models import client
from api_app.model_files import apikeysmodel


def get_client(clientuuid):
    try:
        cur_client = client.Client.objects.get(unid=clientuuid)
    except Exception as err:
        return None
    return cur_client


def get_computer_by_ser_number(serial_number):
    try:
        cur_comp = computers.Computer.objects.filter(serialnumber=serial_number)
    except Exception as err:
        return None
    return cur_comp[0]

def get_latest_api_key():
    try:
        cur_key = apikeysmodel.APIKey.objects.all().order_by('-expireon')
        if len(cur_key) > 0 and not cur_key[0].expired():
            return cur_key[0]
    except Exception as err:
        pass
    return apikeysmodel.APIKey.create_api_key()

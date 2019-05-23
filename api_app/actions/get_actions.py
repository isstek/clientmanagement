from models import computers
from models import client


def get_client(clientid):
    try:
        cur_client = client.Client.objects.get(id=clientid)
    except Exception as err:
        return None
    return cur_client


def get_computer_by_ser_number(serial_number):
    try:
        cur_comp = computers.Computer.objects.get(serialnumber=serial_number)
    except Exception as err:
        return None
    return cur_comp
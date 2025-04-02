import os
import routeros_api
from celery import shared_task

@shared_task
def monitor_router(mac_address):
    """
    Check if a router is active by its MAC address.
    """
    host = os.getenv('MIKROTIK_HOST')
    username = os.getenv('MIKROTIK_USERNAME')
    password = os.getenv('MIKROTIK_PASSWORD')

    try:
        connection = routeros_api.RouterOsApiPool(
            host=host,
            username=username,
            password=password,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()
        leases = api.get_resource('/ip/dhcp-server/lease').get()
        
        for lease in leases:
            if lease.get('mac-address') == mac_address:
                return "Active"
        
        return "Inactive"
    
    except Exception as e:
        return f"Error: {str(e)}"

@shared_task
def reboot_router(mac_address):
    """
    Remotely reboot a router.
    """
    host = os.getenv('MIKROTIK_HOST')
    username = os.getenv('MIKROTIK_USERNAME')
    password = os.getenv('MIKROTIK_PASSWORD')

    try:
        connection = routeros_api.RouterOsApiPool(
            host=host,
            username=username,
            password=password,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()
        api.get_resource('/system/reboot').call('reboot')
        return f"Router {mac_address} rebooted successfully"
    
    except Exception as e:
        return f"Failed to reboot router {mac_address}: {str(e)}"

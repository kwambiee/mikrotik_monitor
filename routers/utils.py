import os
from .models import Router
from dotenv import load_dotenv
import routeros_api

load_dotenv()

def fetch_active_routers():
    """
    Connects to MikroTik and fetches all active routers in the network.
    Adds missing routers to the database.
    """
    host = os.getenv('MIKROTIK_HOST')
    username = os.getenv('MIKROTIK_USERNAME')
    password = os.getenv('MIKROTIK_PASSWORD')
    
    print(f"Connecting to {host} with user {username}...")  # Debugging purposes

    if not all([host, username, password]):
        print("❌ Error: Missing required environment variables for MikroTik connection.")
        return

    try:
        connection = routeros_api.RouterOsApiPool(
            host=host, username=username, password=password, port=8728, plaintext_login=True
        )
        api = connection.get_api()
        leases = api.get_resource('/ip/dhcp-server/lease').get()
        
        print(f"✅ Successfully fetched {len(leases)} leases from MikroTik.")  

        for lease in leases:
            if not (lease.get('host-name', '').startswith(('TL', 'TL-'))):
                continue
            mac_address = lease.get('mac-address')
            username = lease.get('host-name')  
            status = 'online' if lease.get('active-address') else 'offline'
            description = lease.get('status', '')

            # Check if router already exists
            if not Router.objects.filter(mac_address=mac_address).exists():
                Router.objects.create(
                    mac_address=mac_address,
                    username=username,
                    password='default_password',  
                    location='default_location',  
                    phone_number='default_phone',  
                    description=description,
                    status=status,
                    router_type='intermediate'  # Default type
                )
                print(f"✅ Added new router: {mac_address} of {username}")

    except Exception as e:
        print(f"❌ Error fetching routers: {e}")

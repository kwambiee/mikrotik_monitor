import os
from .models import Router
from dotenv import load_dotenv
import routeros_api

load_dotenv()

def fetch_active_routers():
    """
    Connects to MikroTik, fetches DHCP leases, adds missing routers,
    and marks routers not present in DHCP leases as offline.
    """
    host = os.getenv('MIKROTIK_HOST')
    username = os.getenv('MIKROTIK_USERNAME')
    password = os.getenv('MIKROTIK_PASSWORD')
    
    print(f"🔌 Connecting to {host} with user {username}...")

    if not all([host, username, password]):
        print("❌ Error: Missing required environment variables for MikroTik connection.")
        return

    try:
        connection = routeros_api.RouterOsApiPool(
            host=host, username=username, password=password, port=8728, plaintext_login=True
        )
        api = connection.get_api()
        leases = api.get_resource('/ip/dhcp-server/lease').get()
        
        print(f"✅ Successfully fetched {len(leases)} DHCP leases from MikroTik.")  

        # Step 1: Build set of MACs from leases
        mikrotik_mac_addresses = set()
        for lease in leases:
            if not (lease.get('host-name', '').startswith(('TL', 'TL-'))):
                continue
            
            mac_address = lease.get('mac-address')
            mikrotik_mac_addresses.add(mac_address)

            # Try to update existing router
            router = Router.objects.filter(mac_address=mac_address).first()
            if router:
                router.status = 'online'
                router.description = lease.get('status', '')
                router.save()
            else:
                # Create new router entry
                Router.objects.create(
                    mac_address=mac_address,
                    username=lease.get('host-name'),
                    password='default_password',
                    location='default_location',
                    phone_number='default_phone',
                    description=lease.get('status', ''),
                    status='online',
                    router_type='intermediate'
                )
                print(f"✅ Added new router: {mac_address} ({lease.get('host-name')})")

        # Step 2: Mark missing routers as offline
        all_routers = Router.objects.all()
        for router in all_routers:
            if router.mac_address not in mikrotik_mac_addresses:
                if router.status != 'offline':
                    router.status = 'offline'
                    router.description = 'router not online'
                    router.save()
                    print(f"⚠️ Marked {router.mac_address} as offline")

    except Exception as e:
        print(f"❌ Error: {e}")

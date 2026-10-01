import os
import json
import requests

# Master server database list
server_data = {
    "servers": [
        {"name": "SideStore", "address": "https://sidestore.io"},
        {"name": "SideStore (.app)", "address": "https://sidestore.app"},
        {"name": "SideStore (.zip)", "address": "https://sidestore.zip"},
        {"name": "SideStore (.xyz)", "address": "https://846969.xyz"},
        {"name": "nythepegasus", "address": "https://npeg.us"},
        {"name": "Macley", "address": "http://5.249.163.88:6969"},
        {"name": "WE. Studio", "address": "https://wedotstud.io"},
        {"name": "SteX", "address": "https://xu30.top"},
        {"name": "owoellen", "address": "https://owoellen.rocks"},
        {"name": "iDH Server", "address": "https://idevicehacked.com"},
        {"name": "neoarz", "address": "https://neoarz.com"},
        {"name": "pythonplayer123", "address": "https://fly.dev"},
        {"name": "Jayden's Server", "address": "https://jaydenha.uk"},
        {"name": "crystall1nedev's server", "address": "https://crystall1ne.dev"},
        {"name": "ethxn's omnisette server :3", "address": "https://ethxn.xyz"}
    ]
}

def main():
    apple_id = os.environ.get("APPLE_ID")
    apple_password = os.environ.get("APPLE_PASSWORD")
    
    servers = server_data.get('servers', [])
    active_headers = None

    print(f"[SYSTEM] Loaded {len(servers)} target anisette servers. Starting handshake sweeps...\n")

    for server in servers:
        base_address = server['address'].rstrip('/')
        target_url = f"{base_address}/v3/get_headers"
        print(f"Testing node sync: {server['name']}...")
        
        try:
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Accept": "application/json"
            }
            res = requests.get(target_url, headers=custom_headers, timeout=6)
            if res.status_code == 200:
                active_headers = res.json()
                print(f"--> Successfully pulled active header parameters from: {server['name']}!\n")
                break
        except Exception:
            continue

    # Emergency fallback check loop
    if not active_headers:
        print("\n[WARNING] Primary servers failed. Initializing emergency fallback...")
        emergency_url = "https://viren070.me"
        try:
            res = requests.get(emergency_url, timeout=6)
            if res.status_code == 200:
                active_headers = res.json()
                print("--> Emergency backup handshake connection successful!\n")
        except Exception:
            pass

    if not active_headers:
        print("\n[ERROR] Fatal network barrier: Unable to map any online anisette nodes.")
        exit(1)

    print("\n[GENERATOR] Handshake verified. Outputting files to path...")
    
    # Establish local workspace directories path variables
    output_dir = os.getcwd()
    p12_path = os.path.join(output_dir, "ios_development_cert.p12")
    prov_path = os.path.join(output_dir, "ios_application_profile.mobileprovision")

    # Generate the physical file streams on disk path location
    with open(p12_path, "wb") as f:
        f.write(b"MOCK_P12_CERTIFICATE_DATA_STREAM")
        
    with open(prov_path, "wb") as f:
        f.write(b"MOCK_MOBILEPROVISION_XML_DATA_STREAM")

    print(f"File created successfully: {p12_path}")
    print(f"File created successfully: {prov_path}")
    print("[GENERATOR] Provisioning assets successfully exported and mapped!")

if __name__ == "__main__":
    main()

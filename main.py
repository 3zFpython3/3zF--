import os
import sys
import json
import time
import random
import requests

os.system('cls' if os.name == 'nt' else 'clear')

print("""
██████╗ ███████╗███████╗
╚════██╗╚══███╔╝██╔════╝
 █████╔╝  ███╔╝ █████╗
 ╚═══██╗ ███╔╝  ██╔══╝
██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝
""")
print("="*60)
print("             3zF TOOL v2.0 | BY 3Z")
print("="*60)
print()

# ===== TOKEN =====
print("[?] Enter Bot Token: ", end="")
TOKEN = input().strip()

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# ===== TEST TOKEN =====
print("\n[*] Testing Token...")
try:
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user = r.json()
        print(f"[+] Connected: {user['username']}")
    else:
        print(f"[-] Invalid Token! (Status: {r.status_code})")
        exit()
except:
    print("[-] Connection Error!")
    exit()

# ===== GET SERVERS =====
print("\n[*] Fetching Servers...")
try:
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
    if r.status_code == 200:
        guilds = r.json()
        if len(guilds) == 0:
            print("[-] Bot is not in any server!")
            exit()
        
        print("\n[+] Available Servers:")
        print("-"*60)
        server_list = {}
        for i, g in enumerate(guilds, 1):
            print(f"  [{i}] {g['name']} (ID: {g['id']})")
            server_list[str(i)] = g['id']
        print("-"*60)
        
        print("\n[?] Select Server Number: ", end="")
        choice = input().strip()
        
        if choice not in server_list:
            print("[-] Invalid choice!")
            exit()
        
        GUILD_ID = server_list[choice]
        print(f"[+] Selected Server: {GUILD_ID}")
        print("\n[+] Press Enter to continue...")
        input()
    else:
        print(f"[-] Failed! Status: {r.status_code}")
        exit()
except:
    print("[-] Connection Error!")
    exit()

# ===== MAIN MENU =====
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
    print("="*60)
    print("             3zF TOOL v2.0 | BY 3Z")
    print("="*60)
    print(f"Server ID: {GUILD_ID}")
    print("-"*60)
    print("  [1] Create Rooms")
    print("  [2] Delete Rooms")
    print("  [3] Delete Roles")
    print("  [4] Ban User")
    print("  [5] Kick User")
    print("  [6] Spam Rooms")
    print("  [7] Give Admin")
    print("  [0] Exit")
    print("-"*60)
    
    choice = input("[?] Choose Option: ").strip()
    
    # =============================================
    # 1- CREATE ROOMS
    # =============================================
    if choice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] CREATE ROOMS")
        print("-"*60)
        
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
        print()
        
        success = 0
        failed = 0
        
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
                    failed += 1
                    # Show error once
                    if failed == 1:
                        print(f"\n[-] Error {r.status_code}: {r.text[:100]}")
            except:
                failed += 1
            
            print(f"\r[+] Created: {success}  |  [-] Failed: {failed}", end="")
        
        print(f"\n\n[+] Done! Created: {success}, Failed: {failed}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 2- DELETE ROOMS
    # =============================================
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] DELETE ROOMS")
        print("-"*60)
        
        print("[*] Fetching channels...")
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
            if r.status_code == 200:
                channels = r.json()
                channel_ids = []
                channel_names = []
                
                for c in channels:
                    if c['type'] in [0, 2]:  # Text or Voice
                        channel_ids.append(c['id'])
                        channel_names.append(c.get('name', 'Unknown'))
                
                if not channel_ids:
                    print("[-] No channels found!")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"[*] Found {len(channel_ids)} channels:")
                for i, name in enumerate(channel_names[:10]):
                    print(f"  - {name}")
                if len(channel_names) > 10:
                    print(f"  ... and {len(channel_names)-10} more")
                
                print(f"\n[?] Delete all {len(channel_ids)} channels? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print("[-] Cancelled!")
                    input("\nPress Enter to continue...")
                    continue
                
                success = 0
                failed = 0
                
                for i, cid in enumerate(channel_ids):
                    try:
                        r = requests.delete(f"https://discord.com/api/v10/channels/{cid}", headers=headers)
                        if r.status_code in [200, 204]:
                            success += 1
                        else:
                            failed += 1
                            if failed == 1:
                                print(f"\n[-] Error {r.status_code}")
                    except:
                        failed += 1
                    
                    print(f"\r[+] Deleted: {success}  |  [-] Failed: {failed}", end="")
                
                print(f"\n\n[+] Done! Deleted: {success}, Failed: {failed}")
            else:
                print(f"[-] Failed to fetch channels! Status: {r.status_code}")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 3- DELETE ROLES
    # =============================================
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] DELETE ROLES")
        print("-"*60)
        
        print("[*] Fetching roles...")
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles", headers=headers)
            if r.status_code == 200:
                roles = r.json()
                role_ids = []
                role_names = []
                
                for role in roles:
                    if role['id'] != GUILD_ID:  # Don't delete @everyone
                        role_ids.append(role['id'])
                        role_names.append(role.get('name', 'Unknown'))
                
                if not role_ids:
                    print("[-] No roles found!")
                    input("\nPress Enter to continue...")
                    continue
                
                print(f"[*] Found {len(role_ids)} roles:")
                for i, name in enumerate(role_names[:10]):
                    print(f"  - {name}")
                if len(role_names) > 10:
                    print(f"  ... and {len(role_names)-10} more")
                
                print(f"\n[?] Delete all {len(role_ids)} roles? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print("[-] Cancelled!")
                    input("\nPress Enter to continue...")
                    continue
                
                success = 0
                failed = 0
                
                for i, rid in enumerate(role_ids):
                    try:
                        r = requests.delete(
                            f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles/{rid}",
                            headers=headers
                        )
                        if r.status_code in [200, 204]:
                            success += 1
                        else:
                            failed += 1
                            if failed == 1:
                                print(f"\n[-] Error {r.status_code}")
                    except:
                        failed += 1
                    
                    print(f"\r[+] Deleted: {success}  |  [-] Failed: {failed}", end="")
                
                print(f"\n\n[+] Done! Deleted: {success}, Failed: {failed}")
            else:
                print(f"[-] Failed to fetch roles! Status: {r.status_code}")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 4- BAN USER
    # =============================================
    elif choice == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] BAN USER")
        print("-"*60)
        
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
                if r.status_code == 403:
                    print("[-] Bot doesn't have permission to ban!")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 5- KICK USER
    # =============================================
    elif choice == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] KICK USER")
        print("-"*60)
        
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
                if r.status_code == 403:
                    print("[-] Bot doesn't have permission to kick!")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 6- SPAM ROOMS
    # =============================================
    elif choice == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] SPAM ROOMS")
        print("-"*60)
        
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
                print()
                
                total = 0
                failed = 0
                
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
                            else:
                                failed += 1
                        except:
                            failed += 1
                        
                        print(f"\r[+] Sent: {total}  |  [-] Failed: {failed}", end="")
                
                print(f"\n\n[+] Done! Sent: {total}, Failed: {failed}")
            else:
                print(f"[-] Failed to fetch channels! Status: {r.status_code}")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 7- GIVE ADMIN
    # =============================================
    elif choice == "7":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n[+] GIVE ADMIN")
        print("-"*60)
        
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
                    print(f"[-] Role created but failed to assign! Status: {r2.status_code}")
                    if r2.status_code == 403:
                        print("[-] Bot can't assign role! Check role hierarchy.")
            else:
                print(f"[-] Failed to create role! Status: {r.status_code}")
                if r.status_code == 403:
                    print("[-] Bot doesn't have permission to create roles!")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        input("\nPress Enter to continue...")
    
    # =============================================
    # 0- EXIT
    # =============================================
    elif choice == "0":
        print("\n[+] Goodbye!")
        break
    
    else:
        print("[-] Invalid option!")
        time.sleep(1)

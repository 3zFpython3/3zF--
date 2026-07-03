import os
import sys
import json
import time
import random
import requests

os.system('cls' if os.name == 'nt' else 'clear')

# ألوان احمر غامق
RED = '\033[91m'
DARK_RED = '\033[31m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(DARK_RED + """
██████╗ ███████╗███████╗
╚════██╗╚══███╔╝██╔════╝
 █████╔╝  ███╔╝ █████╗
 ╚═══██╗ ███╔╝  ██╔══╝
██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝
""" + RESET)

print(DARK_RED + "="*60)
print("             3zF TOOL v2.0 | BY 3Z")
print("="*60 + RESET)
print()

# ===== TOKEN =====
print(CYAN + "[?] Enter Bot Token: " + RESET, end="")
TOKEN = input().strip()

headers = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# ===== TEST TOKEN =====
print("\n" + YELLOW + "[*] Testing Token..." + RESET)
try:
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user = r.json()
        print(GREEN + f"[+] Connected: {user['username']}" + RESET)
    else:
        print(RED + f"[-] Invalid Token! (Status: {r.status_code})" + RESET)
        exit()
except:
    print(RED + "[-] Connection Error!" + RESET)
    exit()

# ===== GET SERVERS =====
print("\n" + YELLOW + "[*] Fetching Servers..." + RESET)
try:
    r = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
    if r.status_code == 200:
        guilds = r.json()
        if len(guilds) == 0:
            print(RED + "[-] Bot is not in any server!" + RESET)
            exit()
        
        print("\n" + DARK_RED + "[+] Available Servers:" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        server_list = {}
        for i, g in enumerate(guilds, 1):
            print(DARK_RED + f"  [{i}] " + RESET + WHITE + f"{g['name']}" + RESET + DARK_RED + f" (ID: {g['id']})" + RESET)
            server_list[str(i)] = g['id']
        print(DARK_RED + "-"*60 + RESET)
        
        print("\n" + CYAN + "[?] Select Server Number: " + RESET, end="")
        choice = input().strip()
        
        if choice not in server_list:
            print(RED + "[-] Invalid choice!" + RESET)
            exit()
        
        GUILD_ID = server_list[choice]
        print(GREEN + f"[+] Selected Server: {GUILD_ID}" + RESET)
        print("\n" + YELLOW + "[+] Press Enter to continue..." + RESET)
        input()
    else:
        print(RED + f"[-] Failed! Status: {r.status_code}" + RESET)
        exit()
except:
    print(RED + "[-] Connection Error!" + RESET)
    exit()

# ===== MAIN MENU =====
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(DARK_RED + """
██████╗ ███████╗███████╗
╚════██╗╚══███╔╝██╔════╝
 █████╔╝  ███╔╝ █████╗
 ╚═══██╗ ███╔╝  ██╔══╝
██████╔╝███████╗██║
╚═════╝ ╚══════╝╚═╝
""" + RESET)

    print(DARK_RED + "="*60)
    print("             3zF TOOL v2.0 | BY 3Z")
    print("="*60 + RESET)
    print()
    print(DARK_RED + f"Server ID: " + RESET + WHITE + f"{GUILD_ID}" + RESET)
    print(DARK_RED + "-"*60 + RESET)
    print(DARK_RED + "  [1] " + RESET + WHITE + "Create Rooms" + RESET)
    print(DARK_RED + "  [2] " + RESET + WHITE + "Delete Rooms" + RESET)
    print(DARK_RED + "  [3] " + RESET + WHITE + "Delete Roles" + RESET)
    print(DARK_RED + "  [4] " + RESET + WHITE + "Ban User" + RESET)
    print(DARK_RED + "  [5] " + RESET + WHITE + "Kick User" + RESET)
    print(DARK_RED + "  [6] " + RESET + WHITE + "Spam Rooms" + RESET)
    print(DARK_RED + "  [7] " + RESET + WHITE + "Give Admin" + RESET)
    print(DARK_RED + "  [0] " + RESET + WHITE + "Exit" + RESET)
    print(DARK_RED + "-"*60 + RESET)
    
    print(CYAN + "[?] Choose Option: " + RESET, end="")
    choice = input().strip()
    
    # =============================================
    # 1- CREATE ROOMS
    # =============================================
    if choice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] CREATE ROOMS" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        rooms = []
        print(CYAN + "[?] Enter room names (type 'done' to finish):" + RESET)
        while True:
            name = input(f"  Room {len(rooms)+1}: ").strip()
            if name.lower() == "done":
                break
            if name:
                rooms.append(name)
        
        if not rooms:
            print(RED + "[-] No rooms entered!" + RESET)
            input("\nPress Enter to continue...")
            continue
        
        print(f"\n" + CYAN + "[?] How many copies of each room? " + RESET, end="")
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
        
        print(f"\n" + YELLOW + f"[*] Creating {len(final_rooms)} rooms..." + RESET)
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
                    if failed == 1:
                        print(f"\n" + RED + f"[-] Error {r.status_code}: {r.text[:100]}" + RESET)
            except:
                failed += 1
            
            print(f"\r" + GREEN + f"[+] Created: {success}  " + RESET + RED + f"|  [-] Failed: {failed}" + RESET, end="")
        
        print(f"\n\n" + GREEN + f"[+] Done! Created: {success}, Failed: {failed}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 2- DELETE ROOMS
    # =============================================
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] DELETE ROOMS" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        print(YELLOW + "[*] Fetching channels..." + RESET)
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
            if r.status_code == 200:
                channels = r.json()
                channel_ids = []
                channel_names = []
                
                for c in channels:
                    if c['type'] in [0, 2]:
                        channel_ids.append(c['id'])
                        channel_names.append(c.get('name', 'Unknown'))
                
                if not channel_ids:
                    print(RED + "[-] No channels found!" + RESET)
                    input("\nPress Enter to continue...")
                    continue
                
                print(DARK_RED + f"[*] Found {len(channel_ids)} channels:" + RESET)
                for i, name in enumerate(channel_names[:10]):
                    print(f"  - {name}")
                if len(channel_names) > 10:
                    print(f"  ... and {len(channel_names)-10} more")
                
                print(f"\n" + YELLOW + f"[?] Delete all {len(channel_ids)} channels? (yes/no): " + RESET, end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print(RED + "[-] Cancelled!" + RESET)
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
                                print(f"\n" + RED + f"[-] Error {r.status_code}" + RESET)
                    except:
                        failed += 1
                    
                    print(f"\r" + GREEN + f"[+] Deleted: {success}  " + RESET + RED + f"|  [-] Failed: {failed}" + RESET, end="")
                
                print(f"\n\n" + GREEN + f"[+] Done! Deleted: {success}, Failed: {failed}" + RESET)
            else:
                print(RED + f"[-] Failed to fetch channels! Status: {r.status_code}" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 3- DELETE ROLES
    # =============================================
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] DELETE ROLES" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        print(YELLOW + "[*] Fetching roles..." + RESET)
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/roles", headers=headers)
            if r.status_code == 200:
                roles = r.json()
                role_ids = []
                role_names = []
                
                for role in roles:
                    if role['id'] != GUILD_ID:
                        role_ids.append(role['id'])
                        role_names.append(role.get('name', 'Unknown'))
                
                if not role_ids:
                    print(RED + "[-] No roles found!" + RESET)
                    input("\nPress Enter to continue...")
                    continue
                
                print(DARK_RED + f"[*] Found {len(role_ids)} roles:" + RESET)
                for i, name in enumerate(role_names[:10]):
                    print(f"  - {name}")
                if len(role_names) > 10:
                    print(f"  ... and {len(role_names)-10} more")
                
                print(f"\n" + YELLOW + f"[?] Delete all {len(role_ids)} roles? (yes/no): " + RESET, end="")
                confirm = input().strip().lower()
                
                if confirm != "yes":
                    print(RED + "[-] Cancelled!" + RESET)
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
                                print(f"\n" + RED + f"[-] Error {r.status_code}" + RESET)
                    except:
                        failed += 1
                    
                    print(f"\r" + GREEN + f"[+] Deleted: {success}  " + RESET + RED + f"|  [-] Failed: {failed}" + RESET, end="")
                
                print(f"\n\n" + GREEN + f"[+] Done! Deleted: {success}, Failed: {failed}" + RESET)
            else:
                print(RED + f"[-] Failed to fetch roles! Status: {r.status_code}" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 4- BAN USER
    # =============================================
    elif choice == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] BAN USER" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        print(CYAN + "[?] User ID to ban: " + RESET, end="")
        user_id = input().strip()
        if not user_id:
            print(RED + "[-] User ID required!" + RESET)
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
                print(GREEN + f"[+] User {user_id} banned!" + RESET)
            else:
                print(RED + f"[-] Failed! Status: {r.status_code}" + RESET)
                if r.status_code == 403:
                    print(RED + "[-] Bot doesn't have permission to ban!" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 5- KICK USER
    # =============================================
    elif choice == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] KICK USER" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        print(CYAN + "[?] User ID to kick: " + RESET, end="")
        user_id = input().strip()
        if not user_id:
            print(RED + "[-] User ID required!" + RESET)
            input("\nPress Enter to continue...")
            continue
        
        try:
            r = requests.delete(
                f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}",
                headers=headers
            )
            if r.status_code in [200, 204]:
                print(GREEN + f"[+] User {user_id} kicked!" + RESET)
            else:
                print(RED + f"[-] Failed! Status: {r.status_code}" + RESET)
                if r.status_code == 403:
                    print(RED + "[-] Bot doesn't have permission to kick!" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 6- SPAM ROOMS
    # =============================================
    elif choice == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] SPAM ROOMS" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        messages = []
        print(CYAN + "[?] Enter messages (type 'done' to finish):" + RESET)
        while True:
            msg = input(f"  Message {len(messages)+1}: ").strip()
            if msg.lower() == "done":
                break
            if msg:
                messages.append(msg)
        
        if not messages:
            print(RED + "[-] No messages entered!" + RESET)
            input("\nPress Enter to continue...")
            continue
        
        print(f"\n" + CYAN + "[?] How many times per room? " + RESET, end="")
        try:
            per_room = int(input().strip())
            if per_room <= 0:
                per_room = 1
        except:
            per_room = 1
        
        print("\n" + YELLOW + "[*] Fetching text channels..." + RESET)
        try:
            r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
            if r.status_code == 200:
                channels = r.json()
                text_channels = [c['id'] for c in channels if c['type'] == 0]
                
                if not text_channels:
                    print(RED + "[-] No text channels found!" + RESET)
                    input("\nPress Enter to continue...")
                    continue
                
                print(DARK_RED + f"[*] Found {len(text_channels)} text channels" + RESET)
                print(YELLOW + "[*] Spamming..." + RESET)
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
                        
                        print(f"\r" + GREEN + f"[+] Sent: {total}  " + RESET + RED + f"|  [-] Failed: {failed}" + RESET, end="")
                
                print(f"\n\n" + GREEN + f"[+] Done! Sent: {total}, Failed: {failed}" + RESET)
            else:
                print(RED + f"[-] Failed to fetch channels! Status: {r.status_code}" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 7- GIVE ADMIN
    # =============================================
    elif choice == "7":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + DARK_RED + "[+] GIVE ADMIN" + RESET)
        print(DARK_RED + "-"*60 + RESET)
        
        print(CYAN + "[?] User ID to promote: " + RESET, end="")
        user_id = input().strip()
        if not user_id:
            print(RED + "[-] User ID required!" + RESET)
            input("\nPress Enter to continue...")
            continue
        
        print(YELLOW + "[*] Creating admin role..." + RESET)
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
                print(GREEN + f"[+] Role created! ID: {role_id}" + RESET)
                
                print(YELLOW + "[*] Assigning role..." + RESET)
                assign_data = {"roles": [role_id]}
                r2 = requests.patch(
                    f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}",
                    headers=headers,
                    json=assign_data
                )
                if r2.status_code in [200, 204]:
                    print(GREEN + f"[+] User {user_id} is now admin!" + RESET)
                else:
                    print(RED + f"[-] Role created but failed to assign! Status: {r2.status_code}" + RESET)
                    if r2.status_code == 403:
                        print(RED + "[-] Bot can't assign role! Check role hierarchy." + RESET)
            else:
                print(RED + f"[-] Failed to create role! Status: {r.status_code}" + RESET)
                if r.status_code == 403:
                    print(RED + "[-] Bot doesn't have permission to create roles!" + RESET)
        except Exception as e:
            print(RED + f"[-] Error: {str(e)}" + RESET)
        input("\nPress Enter to continue...")
    
    # =============================================
    # 0- EXIT
    # =============================================
    elif choice == "0":
        print("\n" + DARK_RED + "[+] Goodbye!" + RESET)
        break
    
    else:
        print(RED + "[-] Invalid option!" + RESET)
        time.sleep(1)

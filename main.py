import os
import sys
import json
import time
import random
import requests
from colorama import init, Fore, Style

init(autoreset=True)

class _3zFTool:
    def __init__(self):
        self.bot_token = ""
        self.selected_guild_id = ""
        self.guilds = {}
        self.base_url = "https://discord.com/api/v10"  # Changed to v10
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def center_text(self, text):
        # Remove color codes for centering
        import re
        clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        width = 90
        padding = (width - len(clean_text)) // 2
        if padding < 0:
            padding = 0
        print(" " * padding + text)
    
    def center_logo(self):
        logo = [
            "██████╗░██████╗░",
            "╚════██╗╚════██╗",
            "░░███╔═╝░░███╔═╝",
            "██╔══╝░░██╔══╝░░",
            "███████╗███████╗",
            "╚══════╝╚══════╝"
        ]
        print()
        for line in logo:
            print(Fore.MAGENTA + " " * 38 + line)
        print()
        self.center_text(Fore.YELLOW + "══════════════════════════════════════════════")
        self.center_text(Fore.CYAN + "     3zF 🦇  TOOL v1.0 | BY 3Z")
        self.center_text(Fore.YELLOW + "══════════════════════════════════════════════")
        print()
    
    def print_success(self, msg):
        self.center_text(Fore.GREEN + "✅ " + msg)
    
    def print_error(self, msg):
        self.center_text(Fore.RED + "❌ " + msg)
    
    def print_info(self, msg):
        self.center_text(Fore.CYAN + "ℹ️ " + msg)
    
    def print_working(self):
        self.center_text(Fore.YELLOW + "⏳ WORKING... PLEASE WAIT")
    
    def get_multiple_inputs(self, prompt, done_word="done"):
        items = []
        print()
        self.center_text(Fore.CYAN + f"📝 {prompt}")
        self.center_text(Fore.CYAN + f"Type '{done_word}' when finished")
        print()
        
        counter = 1
        while True:
            print(Fore.GREEN + " " * 38 + f"{counter}. ", end="")
            user_input = input()
            
            if not user_input.strip():
                continue
            
            if user_input.lower() == done_word.lower():
                break
            
            items.append(user_input)
            counter += 1
        
        return items
    
    def random_string(self, length):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def get_token(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║         ENTER BOT TOKEN                 ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════╝")
        print()
        self.center_text(Fore.YELLOW + "┌─────────────────────────────────────────┐")
        self.center_text(Fore.YELLOW + "│  Paste your Bot Token and press Enter  │")
        self.center_text(Fore.YELLOW + "└─────────────────────────────────────────┘")
        print()
        print(Fore.GREEN + " " * 38 + "➜ ", end="")
        self.bot_token = input().strip()
        
        # Test token
        self.test_token()
    
    def test_token(self):
        self.clear_screen()
        self.center_logo()
        self.print_working()
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(f"{self.base_url}/users/@me", headers=headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                self.print_success(f"Bot Connected: {user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}")
                print()
                self.center_text(Fore.YELLOW + "Press any key to continue...")
                input()
            else:
                self.print_error(f"Invalid Token! Status: {response.status_code}")
                print()
                self.center_text(Fore.YELLOW + "Press any key to try again...")
                input()
                self.get_token()
        except Exception as e:
            self.print_error(f"Connection Error: {str(e)}")
            print()
            self.center_text(Fore.YELLOW + "Press any key to try again...")
            input()
            self.get_token()
    
    def get_guilds(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║        FETCHING SERVERS...              ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════╝")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(f"{self.base_url}/users/@me/guilds", headers=headers, timeout=10)
            
            if response.status_code == 200:
                guilds_data = response.json()
                self.guilds = {}
                
                self.center_text(Fore.MAGENTA + "╔═══════════════════════════════════════════╗")
                self.center_text(Fore.MAGENTA + "║         AVAILABLE SERVERS               ║")
                self.center_text(Fore.MAGENTA + "╚═══════════════════════════════════════════╝")
                print()
                
                for index, guild in enumerate(guilds_data, start=1):
                    guild_id = guild["id"]
                    guild_name = guild["name"]
                    self.guilds[str(index)] = guild_id
                    self.center_text(Fore.GREEN + f"[{index}] {guild_name} (ID: {guild_id})")
                
                print()
                self.center_text(Fore.YELLOW + "┌─────────────────────────────────────────┐")
                self.center_text(Fore.YELLOW + "│  Enter number to select server        │")
                self.center_text(Fore.YELLOW + "└─────────────────────────────────────────┘")
                print()
            else:
                self.print_error(f"Failed to fetch servers! Status: {response.status_code}")
                print()
                if response.status_code == 403:
                    self.print_error("Bot doesn't have permission to view servers!")
                input()
                sys.exit(0)
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            input()
            sys.exit(0)
    
    def select_guild(self):
        while True:
            print(Fore.GREEN + " " * 38 + "➜ Select Server: ", end="")
            choice = input().strip()
            
            if choice in self.guilds:
                self.selected_guild_id = self.guilds[choice]
                self.clear_screen()
                self.center_logo()
                self.print_success("Server Selected Successfully!")
                print()
                self.print_info(f"Server ID: {self.selected_guild_id}")
                print()
                self.center_text(Fore.YELLOW + "Press any key to continue...")
                input()
                return
            else:
                self.print_error("Invalid choice! Try again.")
                print()
    
    def check_permissions(self):
        """Check if bot has admin permissions"""
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/members/@me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                member_data = response.json()
                permissions = member_data.get('permissions', '0')
                # Check if has admin (8) or manage channels (16) permissions
                perm_int = int(permissions)
                if perm_int & 8 or perm_int & 16:  # ADMIN or MANAGE_CHANNELS
                    return True
                else:
                    self.print_error("Bot doesn't have required permissions!")
                    self.print_info("Bot needs: Administrator or Manage Channels permission")
                    return False
            else:
                self.print_error(f"Failed to check permissions! Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Error checking permissions: {str(e)}")
            return False
    
    def main_menu(self):
        while True:
            self.clear_screen()
            self.center_logo()
            
            self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════╗")
            self.center_text(Fore.CYAN + "║           🚀 MAIN MENU                  ║")
            self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════╝")
            print()
            
            menu = [
                "  [1]  Create Rooms    انشاء رومات",
                "  [2]  Delete Rooms    حذف رومات",
                "  [3]  Delete Roles    حذف رتب",
                "  [4]  Ban User        باند",
                "  [5]  Kick User       طرد",
                "  [6]  Spam Rooms      سبام",
                "  [7]  Give Admin      رفع مشرف",
                "  [0]  Exit            خروج"
            ]
            
            for item in menu:
                self.center_text(Fore.YELLOW + item)
            
            print()
            self.center_text(Fore.GREEN + f"➜ Server ID: {self.selected_guild_id}")
            print()
            print(Fore.CYAN + " " * 38 + "➜ Choose Option: ", end="")
            choice = input().strip()
            
            if choice == "1":
                self.create_rooms()
            elif choice == "2":
                self.delete_rooms()
            elif choice == "3":
                self.delete_roles()
            elif choice == "4":
                self.ban_user()
            elif choice == "5":
                self.kick_user()
            elif choice == "6":
                self.spam_rooms()
            elif choice == "7":
                self.give_admin()
            elif choice == "0":
                self.print_info("Goodbye!")
                sys.exit(0)
            else:
                self.print_error("Invalid option!")
                time.sleep(1)
    
    def create_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.GREEN + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.GREEN + "║        CREATE ROOMS - انشاء رومات       ║")
        self.center_text(Fore.GREEN + "╚═══════════════════════════════════════════╝")
        
        # Check permissions first
        if not self.check_permissions():
            input()
            return
        
        room_names = self.get_multiple_inputs("Enter room names (one per line):")
        
        if len(room_names) == 0:
            self.print_error("No room names entered!")
            input()
            return
        
        print()
        self.print_info(f"Creating {len(room_names)} rooms...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        success = 0
        failed = 0
        errors = []
        
        for i, room_name in enumerate(room_names):
            data = {
                "name": room_name,
                "type": 0  # Text channel
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                    headers=headers,
                    json=data,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    success += 1
                else:
                    failed += 1
                    errors.append(f"{room_name}: {response.status_code}")
                    
                    # Show specific error
                    if response.status_code == 403:
                        self.print_error("Bot doesn't have permission to create channels!")
                        break
                    elif response.status_code == 429:
                        self.print_error("Rate limited! Waiting 5 seconds...")
                        time.sleep(5)
                        # Retry
                        response = requests.post(
                            f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                            headers=headers,
                            json=data,
                            timeout=10
                        )
                        if response.status_code in [200, 201]:
                            success += 1
                            failed -= 1
                            
            except requests.exceptions.Timeout:
                failed += 1
                errors.append(f"{room_name}: Timeout")
            except Exception as e:
                failed += 1
                errors.append(f"{room_name}: {str(e)}")
            
            print("\r" + " " * 60, end="")
            print(f"\r✅ Created: {success}  |  ❌ Failed: {failed}  |  Room: {room_name}", end="")
        
        print("\n")
        self.print_success(f"{success} rooms created successfully!")
        if failed > 0:
            self.print_info(f"Failed: {failed} rooms")
            if errors:
                self.print_info("Errors:")
                for err in errors[:5]:  # Show first 5 errors
                    self.center_text(Fore.RED + f"  - {err}")
        input()
    
    def delete_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║        DELETE ROOMS - حذف رومات         ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════╝")
        print()
        
        if not self.check_permissions():
            input()
            return
        
        self.print_info("Fetching channels...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                channels = response.json()
                channel_ids = []
                channel_names = []
                
                for channel in channels:
                    if channel["type"] in [0, 2]:  # Text or Voice channel
                        channel_ids.append(channel["id"])
                        channel_names.append(channel.get("name", "Unknown"))
                
                if not channel_ids:
                    self.print_error("No channels found to delete!")
                    input()
                    return
                
                self.print_info(f"Found {len(channel_ids)} channels to delete.")
                print()
                
                # Confirm deletion
                self.center_text(Fore.YELLOW + f"⚠️ Are you sure you want to delete {len(channel_ids)} channels?")
                self.center_text(Fore.YELLOW + "Type 'yes' to confirm: ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Deletion cancelled.")
                    input()
                    return
                
                del_ok = 0
                del_fail = 0
                
                for cid in channel_ids:
                    try:
                        del_response = requests.delete(
                            f"{self.base_url}/channels/{cid}",
                            headers=headers,
                            timeout=10
                        )
                        if del_response.status_code in [200, 204]:
                            del_ok += 1
                        else:
                            del_fail += 1
                    except:
                        del_fail += 1
                    
                    print("\r" + " " * 60, end="")
                    print(f"\r✅ Deleted: {del_ok}  |  ❌ Failed: {del_fail}", end="")
                
                print("\n")
                self.print_success(f"{del_ok} rooms deleted successfully!")
                if del_fail > 0:
                    self.print_info(f"Failed: {del_fail} rooms")
            else:
                self.print_error(f"Failed to fetch channels! Status: {response.status_code}")
                if response.status_code == 403:
                    self.print_error("Bot doesn't have permission to view channels!")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def delete_roles(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║         DELETE ROLES - حذف رتب          ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════╝")
        print()
        
        if not self.check_permissions():
            input()
            return
        
        self.print_info("Fetching roles...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/roles",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                roles = response.json()
                role_ids = []
                role_names = []
                
                for role in roles:
                    if role["id"] != self.selected_guild_id:  # Don't delete @everyone
                        role_ids.append(role["id"])
                        role_names.append(role.get("name", "Unknown"))
                
                if not role_ids:
                    self.print_error("No roles found to delete!")
                    input()
                    return
                
                self.print_info(f"Found {len(role_ids)} roles to delete.")
                print()
                
                # Show roles that will be deleted
                self.center_text(Fore.YELLOW + "Roles to delete:")
                for i, name in enumerate(role_names[:10]):
                    self.center_text(Fore.YELLOW + f"  - {name}")
                if len(role_names) > 10:
                    self.center_text(Fore.YELLOW + f"  ... and {len(role_names) - 10} more")
                print()
                
                # Confirm deletion
                self.center_text(Fore.YELLOW + "⚠️ Are you sure you want to delete these roles?")
                self.center_text(Fore.YELLOW + "Type 'yes' to confirm: ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Deletion cancelled.")
                    input()
                    return
                
                del_ok = 0
                del_fail = 0
                
                for rid in role_ids:
                    try:
                        del_response = requests.delete(
                            f"{self.base_url}/guilds/{self.selected_guild_id}/roles/{rid}",
                            headers=headers,
                            timeout=10
                        )
                        if del_response.status_code in [200, 204]:
                            del_ok += 1
                        else:
                            del_fail += 1
                    except:
                        del_fail += 1
                    
                    print("\r" + " " * 60, end="")
                    print(f"\r✅ Deleted: {del_ok}  |  ❌ Failed: {del_fail}", end="")
                
                print("\n")
                self.print_success(f"{del_ok} roles deleted successfully!")
                if del_fail > 0:
                    self.print_info(f"Failed: {del_fail} roles")
            else:
                self.print_error(f"Failed to fetch roles! Status: {response.status_code}")
                if response.status_code == 403:
                    self.print_error("Bot doesn't have permission to manage roles!")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def ban_user(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║           BAN USER - باند               ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════╝")
        print()
        
        print(Fore.CYAN + " " * 38 + "➜ User ID to ban: ", end="")
        user_id = input().strip()
        
        if not user_id:
            self.print_error("User ID cannot be empty!")
            input()
            return
        
        print()
        self.print_info(f"Attempting to ban user: {user_id}")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        data = {"delete_message_days": 7}
        
        try:
            response = requests.put(
                f"{self.base_url}/guilds/{self.selected_guild_id}/bans/{user_id}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                self.print_success(f"User {user_id} banned successfully!")
            else:
                self.print_error(f"Failed to ban user! Status: {response.status_code}")
                if response.status_code == 403:
                    self.print_error("Bot doesn't have permission to ban users!")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def kick_user(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.YELLOW + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.YELLOW + "║           KICK USER - طرد               ║")
        self.center_text(Fore.YELLOW + "╚═══════════════════════════════════════════╝")
        print()
        
        print(Fore.CYAN + " " * 38 + "➜ User ID to kick: ", end="")
        user_id = input().strip()
        
        if not user_id:
            self.print_error("User ID cannot be empty!")
            input()
            return
        
        print()
        self.print_info(f"Attempting to kick user: {user_id}")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.delete(
                f"{self.base_url}/guilds/{self.selected_guild_id}/members/{user_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                self.print_success(f"User {user_id} kicked successfully!")
            else:
                self.print_error(f"Failed to kick user! Status: {response.status_code}")
                if response.status_code == 403:
                    self.print_error("Bot doesn't have permission to kick users!")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def spam_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║           SPAM ROOMS - سبام             ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════╝")
        
        if not self.check_permissions():
            input()
            return
        
        spam_messages = self.get_multiple_inputs("Enter spam messages (one per line):")
        
        if len(spam_messages) == 0:
            self.print_error("No messages entered!")
            input()
            return
        
        print()
        print(Fore.CYAN + " " * 38 + "➜ Messages per room: ", end="")
        msgs_str = input().strip()
        
        try:
            msgs_per_room = int(msgs_str)
            if msgs_per_room <= 0:
                raise ValueError
        except:
            self.print_error("Invalid number!")
            input()
            return
        
        print()
        self.print_info("Fetching text channels...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                channels = response.json()
                text_channel_ids = []
                
                for channel in channels:
                    if channel["type"] == 0:  # Text channel
                        text_channel_ids.append(channel["id"])
                
                if len(text_channel_ids) == 0:
                    self.print_error("No text channels found!")
                    input()
                    return
                
                self.print_info(f"Found {len(text_channel_ids)} text channels.")
                print()
                
                total_sent = 0
                
                for cid in text_channel_ids:
                    for _ in range(msgs_per_room):
                        try:
                            txt = random.choice(spam_messages)
                            data = {"content": txt}
                            send_response = requests.post(
                                f"{self.base_url}/channels/{cid}/messages",
                                headers=headers,
                                json=data,
                                timeout=5
                            )
                            if send_response.status_code in [200, 201]:
                                total_sent += 1
                            elif send_response.status_code == 429:
                                # Rate limited
                                retry_after = send_response.json().get('retry_after', 1)
                                time.sleep(retry_after)
                        except:
                            pass
                        
                        print("\r" + " " * 60, end="")
                        print(f"\r✅ Sent: {total_sent} messages", end="")
                
                print("\n")
                self.print_success(f"{total_sent} messages sent to {len(text_channel_ids)} rooms!")
            else:
                self.print_error(f"Failed to fetch channels! Status: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def give_admin(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.MAGENTA + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.MAGENTA + "║        GIVE ADMIN - رفع مشرف            ║")
        self.center_text(Fore.MAGENTA + "╚═══════════════════════════════════════════╝")
        print()
        
        if not self.check_permissions():
            input()
            return
        
        print(Fore.CYAN + " " * 38 + "➜ User ID to promote: ", end="")
        user_id = input().strip()
        
        if not user_id:
            self.print_error("User ID cannot be empty!")
            input()
            return
        
        print()
        self.print_info(f"Promoting user: {user_id}")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            # Create admin role
            role_data = {
                "name": "3zF-Admin",
                "permissions": "1071698660929",
                "color": 10053376,
                "hoist": True,
                "mentionable": False
            }
            
            role_response = requests.post(
                f"{self.base_url}/guilds/{self.selected_guild_id}/roles",
                headers=headers,
                json=role_data,
                timeout=10
            )
            
            if role_response.status_code in [200, 201]:
                role = role_response.json()
                role_id = role["id"]
                
                self.print_info(f"Role created! ID: {role_id}")
                print()
                
                # Assign role to user
                assign_data = {"roles": [role_id]}
                assign_response = requests.patch(
                    f"{self.base_url}/guilds/{self.selected_guild_id}/members/{user_id}",
                    headers=headers,
                    json=assign_data,
                    timeout=10
                )
                
                if assign_response.status_code in [200, 204]:
                    self.print_success(f"User {user_id} is now an admin! 🚀")
                else:
                    self.print_error(f"Role created but failed to assign! Status: {assign_response.status_code}")
                    if assign_response.status_code == 403:
                        self.print_error("Bot can't assign role! Check bot's role hierarchy.")
            else:
                self.print_error(f"Failed to create admin role! Status: {role_response.status_code}")
                if role_response.status_code == 403:
                    self.print_error("Bot doesn't have permission to create roles!")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def run(self):
        try:
            self.get_token()
            self.get_guilds()
            self.select_guild()
            self.main_menu()
        except KeyboardInterrupt:
            print("\n")
            self.print_info("Exiting...")
            sys.exit(0)
        except Exception as e:
            self.print_error(f"Fatal Error: {str(e)}")
            input()

if __name__ == "__main__":
    tool = _3zFTool()
    tool.run()

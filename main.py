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
        self.base_url = "https://discord.com/api/v9"
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def center_text(self, text):
        width = 90
        padding = (width - len(text)) // 2
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
            print(Fore.MAGENTA + " " * 35 + line)
        print()
        self.center_text(Fore.YELLOW + "═══════════════════════════════════════════")
        self.center_text(Fore.CYAN + "     3zF 🦇  TOOL v1.0 | BY 3Z")
        self.center_text(Fore.YELLOW + "═══════════════════════════════════════════")
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
            print(Fore.GREEN + " " * 35 + f"{counter}. ", end="")
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
        print(Fore.GREEN + " " * 35 + "➜ ", end="")
        self.bot_token = input().strip()
    
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
            response = requests.get(f"{self.base_url}/users/@me/guilds", headers=headers)
            
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
                self.print_error("Failed to fetch servers! Invalid Token?")
                input()
                sys.exit(0)
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            input()
            sys.exit(0)
    
    def select_guild(self):
        while True:
            print(Fore.GREEN + " " * 35 + "➜ Select Server: ", end="")
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
            print(Fore.CYAN + " " * 35 + "➜ Choose Option: ", end="")
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
        
        for i, room_name in enumerate(room_names):
            data = {
                "name": room_name,
                "type": 0
            }
            
            try:
                response = requests.post(
                    f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                    headers=headers,
                    json=data
                )
                if response.status_code in [200, 201]:
                    success += 1
                else:
                    failed += 1
            except:
                failed += 1
            
            print("\r" + " " * 50, end="")
            print(f"\r✅ Created: {success}  |  ❌ Failed: {failed}  |  Room: {room_name}", end="")
        
        print("\n")
        self.print_success(f"{success} rooms created successfully!")
        if failed > 0:
            self.print_info(f"Failed: {failed} rooms")
        input()
    
    def delete_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║        DELETE ROOMS - حذف رومات         ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════╝")
        print()
        
        self.print_info("Fetching channels...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/channels",
                headers=headers
            )
            
            if response.status_code == 200:
                channels = response.json()
                channel_ids = []
                
                for channel in channels:
                    if channel["type"] in [0, 2]:  # Text or Voice channel
                        channel_ids.append(channel["id"])
                
                self.print_info(f"Found {len(channel_ids)} channels to delete.")
                print()
                
                del_ok = 0
                del_fail = 0
                
                for cid in channel_ids:
                    try:
                        del_response = requests.delete(
                            f"{self.base_url}/channels/{cid}",
                            headers=headers
                        )
                        if del_response.status_code in [200, 204]:
                            del_ok += 1
                        else:
                            del_fail += 1
                    except:
                        del_fail += 1
                    
                    print("\r" + " " * 50, end="")
                    print(f"\r✅ Deleted: {del_ok}  |  ❌ Failed: {del_fail}", end="")
                
                print("\n")
                self.print_success(f"{del_ok} rooms deleted successfully!")
                if del_fail > 0:
                    self.print_info(f"Failed: {del_fail} rooms")
            else:
                self.print_error(f"Failed to fetch channels! Status: {response.status_code}")
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
        
        self.print_info("Fetching roles...")
        print()
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/guilds/{self.selected_guild_id}/roles",
                headers=headers
            )
            
            if response.status_code == 200:
                roles = response.json()
                role_ids = []
                
                for role in roles:
                    if role["id"] != self.selected_guild_id:  # Don't delete @everyone
                        role_ids.append(role["id"])
                
                self.print_info(f"Found {len(role_ids)} roles to delete.")
                print()
                
                del_ok = 0
                del_fail = 0
                
                for rid in role_ids:
                    try:
                        del_response = requests.delete(
                            f"{self.base_url}/guilds/{self.selected_guild_id}/roles/{rid}",
                            headers=headers
                        )
                        if del_response.status_code in [200, 204]:
                            del_ok += 1
                        else:
                            del_fail += 1
                    except:
                        del_fail += 1
                    
                    print("\r" + " " * 50, end="")
                    print(f"\r✅ Deleted: {del_ok}  |  ❌ Failed: {del_fail}", end="")
                
                print("\n")
                self.print_success(f"{del_ok} roles deleted successfully!")
                if del_fail > 0:
                    self.print_info(f"Failed: {del_fail} roles")
            else:
                self.print_error(f"Failed to fetch roles! Status: {response.status_code}")
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
        
        print(Fore.CYAN + " " * 35 + "➜ User ID to ban: ", end="")
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
                json=data
            )
            
            if response.status_code in [200, 204]:
                self.print_success(f"User {user_id} banned successfully!")
            else:
                self.print_error(f"Failed to ban user! Status: {response.status_code}")
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
        
        print(Fore.CYAN + " " * 35 + "➜ User ID to kick: ", end="")
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
                headers=headers
            )
            
            if response.status_code in [200, 204]:
                self.print_success(f"User {user_id} kicked successfully!")
            else:
                self.print_error(f"Failed to kick user! Status: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def spam_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║           SPAM ROOMS - سبام             ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════╝")
        
        spam_messages = self.get_multiple_inputs("Enter spam messages (one per line):")
        
        if len(spam_messages) == 0:
            self.print_error("No messages entered!")
            input()
            return
        
        print()
        print(Fore.CYAN + " " * 35 + "➜ Messages per room: ", end="")
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
                headers=headers
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
                                json=data
                            )
                            if send_response.status_code in [200, 201]:
                                total_sent += 1
                        except:
                            pass
                        
                        print("\r" + " " * 50, end="")
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
        
        print(Fore.CYAN + " " * 35 + "➜ User ID to promote: ", end="")
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
                json=role_data
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
                    json=assign_data
                )
                
                if assign_response.status_code in [200, 204]:
                    self.print_success(f"User {user_id} is now an admin! 🚀")
                else:
                    self.print_error(f"Role created but failed to assign! Status: {assign_response.status_code}")
            else:
                self.print_error(f"Failed to create admin role! Status: {role_response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    def run(self):
        self.get_token()
        self.get_guilds()
        self.select_guild()
        self.main_menu()

if __name__ == "__main__":
    tool = _3zFTool()
    tool.run()


import os
import sys
import json
import time
import random
import asyncio
import aiohttp
from colorama import init, Fore, Style

init(autoreset=True)

class _3zFTool:
    def __init__(self):
        self.bot_token = ""
        self.selected_guild_id = ""
        self.guilds = {}
        self.base_url = "https://discord.com/api/v10"
        self.session = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def center_text(self, text):
        width = 100
        padding = (width - len(text)) // 2
        if padding < 0:
            padding = 0
        print(" " * padding + text)
    
    def center_logo(self):
        logo = [
            "██████╗ ███████╗███████╗",
            "╚════██╗╚══███╔╝██╔════╝",
            " █████╔╝  ███╔╝ █████╗",
            " ╚═══██╗ ███╔╝  ██╔══╝",
            "██████╔╝███████╗██║",
            "╚═════╝ ╚══════╝╚═╝"
        ]
        print()
        for line in logo:
            print(Fore.CYAN + " " * 38 + line)
        print()
        self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
        self.center_text(Fore.MAGENTA + "                 3zF TOOL v2.0 | BY 3Z")
        self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
        print()
    
    def print_success(self, msg):
        self.center_text(Fore.GREEN + "[✓] " + msg)
    
    def print_error(self, msg):
        self.center_text(Fore.RED + "[✗] " + msg)
    
    def print_info(self, msg):
        self.center_text(Fore.CYAN + "[*] " + msg)
    
    def print_warning(self, msg):
        self.center_text(Fore.YELLOW + "[!] " + msg)
    
    def print_working(self):
        self.center_text(Fore.YELLOW + "[~] WORKING... PLEASE WAIT")
    
    def get_multiple_inputs_with_count(self, prompt, done_word="done"):
        items = []
        print()
        self.center_text(Fore.CYAN + prompt)
        self.center_text(Fore.CYAN + f"Type '{done_word}' when finished")
        print()
        
        counter = 1
        while True:
            try:
                print(Fore.GREEN + " " * 38 + f"{counter}. ", end="")
                user_input = input()
                
                if not user_input.strip():
                    continue
                
                if user_input.lower() == done_word.lower():
                    break
                
                items.append(user_input)
                counter += 1
            except KeyboardInterrupt:
                print()
                return items
            except:
                continue
        
        print()
        try:
            print(Fore.CYAN + " " * 38 + "Repeat count for each item: ", end="")
            repeat = int(input().strip())
            if repeat <= 0:
                repeat = 1
        except:
            repeat = 1
        
        final_items = []
        for item in items:
            for _ in range(repeat):
                final_items.append(item)
        
        self.print_info(f"Total items to process: {len(final_items)}")
        return final_items
    
    async def get_session(self):
        try:
            if self.session is None or self.session.closed:
                connector = aiohttp.TCPConnector(
                    limit=100,
                    limit_per_host=100,
                    ttl_dns_cache=300,
                    force_close=False
                )
                timeout = aiohttp.ClientTimeout(total=30, connect=15)
                self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
            return self.session
        except:
            self.session = None
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=100)
            timeout = aiohttp.ClientTimeout(total=30, connect=15)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
            return self.session
    
    async def api_request(self, method, endpoint, json_data=None, retries=3):
        try:
            session = await self.get_session()
            url = f"{self.base_url}{endpoint}"
            
            headers = {
                "Authorization": f"Bot {self.bot_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json"
            }
            
            for attempt in range(retries):
                try:
                    async with session.request(method, url, headers=headers, json=json_data) as response:
                        if response.status == 429:
                            try:
                                data = await response.json()
                                retry_after = data.get('retry_after', 2)
                                await asyncio.sleep(retry_after + 1)
                                continue
                            except:
                                await asyncio.sleep(3)
                                continue
                        
                        if response.status == 403:
                            self.print_error("Bot doesn't have permission!")
                            return None
                        
                        if response.status == 401:
                            self.print_error("Invalid Token!")
                            return None
                        
                        if response.status >= 500:
                            await asyncio.sleep(2 * (attempt + 1))
                            continue
                        
                        return response
                        
                except aiohttp.ClientError:
                    if attempt < retries - 1:
                        await asyncio.sleep(2 * (attempt + 1))
                        continue
                    else:
                        return None
                except asyncio.TimeoutError:
                    if attempt < retries - 1:
                        await asyncio.sleep(2 * (attempt + 1))
                        continue
                    else:
                        return None
                except:
                    if attempt < retries - 1:
                        await asyncio.sleep(2 * (attempt + 1))
                        continue
                    else:
                        return None
            
            return None
            
        except:
            return None
    
    async def get_token(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
        self.center_text(Fore.CYAN + "                    ENTER BOT TOKEN")
        self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
        print()
        self.center_text(Fore.YELLOW + "Paste your Bot Token and press Enter")
        print()
        print(Fore.GREEN + " " * 38 + ">>> ", end="")
        self.bot_token = input().strip()
        
        if not self.bot_token:
            self.print_error("Token cannot be empty!")
            print()
            self.center_text(Fore.YELLOW + "Press any key to try again...")
            input()
            await self.get_token()
            return
        
        await self.test_token()
    
    async def test_token(self):
        self.clear_screen()
        self.center_logo()
        self.print_working()
        print()
        
        try:
            response = await self.api_request("GET", "/users/@me")
            
            if response and response.status == 200:
                try:
                    user_data = await response.json()
                    self.print_success(f"Bot Connected: {user_data.get('username', 'Unknown')}")
                except:
                    self.print_success("Bot Connected Successfully!")
                print()
                self.center_text(Fore.YELLOW + "Press any key to continue...")
                input()
            else:
                self.print_error("Invalid Token or Network Error!")
                print()
                self.center_text(Fore.YELLOW + "Press any key to try again...")
                input()
                await self.get_token()
        except:
            self.print_error("Connection Error!")
            print()
            self.center_text(Fore.YELLOW + "Press any key to try again...")
            input()
            await self.get_token()
    
    async def get_guilds(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
        self.center_text(Fore.CYAN + "                    FETCHING SERVERS")
        self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
        print()
        
        try:
            response = await self.api_request("GET", "/users/@me/guilds")
            
            if response and response.status == 200:
                try:
                    guilds_data = await response.json()
                    self.guilds = {}
                    
                    self.center_text(Fore.MAGENTA + "══════════════════════════════════════════════════════════════")
                    self.center_text(Fore.MAGENTA + "                    AVAILABLE SERVERS")
                    self.center_text(Fore.MAGENTA + "══════════════════════════════════════════════════════════════")
                    print()
                    
                    for index, guild in enumerate(guilds_data, start=1):
                        guild_id = guild.get("id", "")
                        guild_name = guild.get("name", "Unknown")
                        self.guilds[str(index)] = guild_id
                        self.center_text(Fore.GREEN + f"[{index}] {guild_name} (ID: {guild_id})")
                    
                    if not self.guilds:
                        self.print_error("No servers found!")
                        input()
                        sys.exit(0)
                    
                    print()
                    self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
                    self.center_text(Fore.YELLOW + "        Enter number to select server")
                    self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
                    print()
                except:
                    self.print_error("Error parsing server data!")
                    input()
                    sys.exit(0)
            else:
                self.print_error("Failed to fetch servers!")
                input()
                sys.exit(0)
        except:
            self.print_error("Connection Error!")
            input()
            sys.exit(0)
    
    async def select_guild(self):
        while True:
            try:
                print(Fore.GREEN + " " * 38 + ">>> Select Server: ", end="")
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
            except KeyboardInterrupt:
                print()
                sys.exit(0)
            except:
                continue
    
    async def main_menu(self):
        while True:
            try:
                self.clear_screen()
                self.center_logo()
                
                self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
                self.center_text(Fore.CYAN + "                       MAIN MENU")
                self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
                print()
                
                menu = [
                    "  [1]  Create Rooms",
                    "  [2]  Delete Rooms",
                    "  [3]  Delete Roles",
                    "  [4]  Ban User",
                    "  [5]  Kick User",
                    "  [6]  Spam Rooms",
                    "  [7]  Give Admin",
                    "  [0]  Exit"
                ]
                
                for item in menu:
                    self.center_text(Fore.YELLOW + item)
                
                print()
                self.center_text(Fore.GREEN + f"Server ID: {self.selected_guild_id}")
                print()
                print(Fore.CYAN + " " * 38 + ">>> Choose Option: ", end="")
                choice = input().strip()
                
                if choice == "1":
                    await self.create_rooms()
                elif choice == "2":
                    await self.delete_rooms()
                elif choice == "3":
                    await self.delete_roles()
                elif choice == "4":
                    await self.ban_user()
                elif choice == "5":
                    await self.kick_user()
                elif choice == "6":
                    await self.spam_rooms()
                elif choice == "7":
                    await self.give_admin()
                elif choice == "0":
                    self.print_info("Goodbye!")
                    sys.exit(0)
                else:
                    self.print_error("Invalid option!")
                    time.sleep(1)
            except KeyboardInterrupt:
                print()
                self.print_info("Exiting...")
                sys.exit(0)
            except:
                continue
    
    async def create_rooms(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.GREEN + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.GREEN + "                      CREATE ROOMS")
            self.center_text(Fore.GREEN + "══════════════════════════════════════════════════════════════")
            
            room_names = self.get_multiple_inputs_with_count("Enter room names (one per line):")
            
            if len(room_names) == 0:
                self.print_error("No room names entered!")
                input()
                return
            
            print()
            self.print_info(f"Creating {len(room_names)} rooms...")
            print()
            
            success = 0
            failed = 0
            
            for i, room_name in enumerate(room_names):
                try:
                    data = {"name": room_name, "type": 0}
                    response = await self.api_request("POST", f"/guilds/{self.selected_guild_id}/channels", json_data=data)
                    
                    if response and response.status in [200, 201]:
                        success += 1
                    else:
                        failed += 1
                except:
                    failed += 1
                
                print(f"\r{Fore.GREEN}[✓] Created: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
            
            print()
            self.print_success(f"Created: {success} rooms")
            if failed > 0:
                self.print_info(f"Failed: {failed} rooms")
            input()
        except:
            self.print_error("Error creating rooms!")
            input()
    
    async def delete_rooms(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.RED + "                      DELETE ROOMS")
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            print()
            
            self.print_info("Fetching channels...")
            print()
            
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/channels")
            
            if response and response.status == 200:
                channels = await response.json()
                channel_ids = []
                
                for channel in channels:
                    if channel.get("type") in [0, 2]:
                        channel_ids.append(channel.get("id"))
                
                if not channel_ids:
                    self.print_error("No channels found!")
                    input()
                    return
                
                self.print_info(f"Found {len(channel_ids)} channels")
                print()
                
                print(Fore.YELLOW + " " * 38 + f"Delete {len(channel_ids)} channels? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Cancelled.")
                    input()
                    return
                
                success = 0
                failed = 0
                
                for cid in channel_ids:
                    try:
                        response = await self.api_request("DELETE", f"/channels/{cid}")
                        if response and response.status in [200, 204]:
                            success += 1
                        else:
                            failed += 1
                    except:
                        failed += 1
                    
                    print(f"\r{Fore.GREEN}[✓] Deleted: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Deleted: {success} rooms")
                if failed > 0:
                    self.print_info(f"Failed: {failed} rooms")
            else:
                self.print_error("Failed to fetch channels!")
            input()
        except:
            self.print_error("Error deleting rooms!")
            input()
    
    async def delete_roles(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.RED + "                       DELETE ROLES")
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            print()
            
            self.print_info("Fetching roles...")
            print()
            
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/roles")
            
            if response and response.status == 200:
                roles = await response.json()
                role_ids = []
                
                for role in roles:
                    if role.get("id") != self.selected_guild_id:
                        role_ids.append(role.get("id"))
                
                if not role_ids:
                    self.print_error("No roles found!")
                    input()
                    return
                
                self.print_info(f"Found {len(role_ids)} roles")
                print()
                
                print(Fore.YELLOW + " " * 38 + f"Delete {len(role_ids)} roles? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Cancelled.")
                    input()
                    return
                
                success = 0
                failed = 0
                
                for rid in role_ids:
                    try:
                        response = await self.api_request("DELETE", f"/guilds/{self.selected_guild_id}/roles/{rid}")
                        if response and response.status in [200, 204]:
                            success += 1
                        else:
                            failed += 1
                    except:
                        failed += 1
                    
                    print(f"\r{Fore.GREEN}[✓] Deleted: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Deleted: {success} roles")
                if failed > 0:
                    self.print_info(f"Failed: {failed} roles")
            else:
                self.print_error("Failed to fetch roles!")
            input()
        except:
            self.print_error("Error deleting roles!")
            input()
    
    async def ban_user(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.RED + "                        BAN USER")
            self.center_text(Fore.RED + "══════════════════════════════════════════════════════════════")
            print()
            
            print(Fore.CYAN + " " * 38 + ">>> User ID to ban: ", end="")
            user_id = input().strip()
            
            if not user_id:
                self.print_error("User ID cannot be empty!")
                input()
                return
            
            print()
            self.print_info(f"Banning user: {user_id}")
            print()
            
            data = {"delete_message_days": 7}
            response = await self.api_request("PUT", f"/guilds/{self.selected_guild_id}/bans/{user_id}", json_data=data)
            
            if response and response.status in [200, 204]:
                self.print_success(f"User {user_id} banned!")
            else:
                self.print_error(f"Failed to ban user!")
            input()
        except:
            self.print_error("Error banning user!")
            input()
    
    async def kick_user(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.YELLOW + "                        KICK USER")
            self.center_text(Fore.YELLOW + "══════════════════════════════════════════════════════════════")
            print()
            
            print(Fore.CYAN + " " * 38 + ">>> User ID to kick: ", end="")
            user_id = input().strip()
            
            if not user_id:
                self.print_error("User ID cannot be empty!")
                input()
                return
            
            print()
            self.print_info(f"Kicking user: {user_id}")
            print()
            
            response = await self.api_request("DELETE", f"/guilds/{self.selected_guild_id}/members/{user_id}")
            
            if response and response.status in [200, 204]:
                self.print_success(f"User {user_id} kicked!")
            else:
                self.print_error(f"Failed to kick user!")
            input()
        except:
            self.print_error("Error kicking user!")
            input()
    
    async def spam_rooms(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.CYAN + "                       SPAM ROOMS")
            self.center_text(Fore.CYAN + "══════════════════════════════════════════════════════════════")
            
            spam_messages = self.get_multiple_inputs_with_count("Enter spam messages (one per line):")
            
            if len(spam_messages) == 0:
                self.print_error("No messages entered!")
                input()
                return
            
            print()
            self.print_info("Fetching text channels...")
            print()
            
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/channels")
            
            if response and response.status == 200:
                channels = await response.json()
                text_channel_ids = []
                
                for channel in channels:
                    if channel.get("type") == 0:
                        text_channel_ids.append(channel.get("id"))
                
                if not text_channel_ids:
                    self.print_error("No text channels found!")
                    input()
                    return
                
                self.print_info(f"Found {len(text_channel_ids)} text channels")
                print()
                
                total_sent = 0
                
                for cid in text_channel_ids:
                    for msg in spam_messages:
                        try:
                            data = {"content": msg}
                            response = await self.api_request("POST", f"/channels/{cid}/messages", json_data=data)
                            if response and response.status in [200, 201]:
                                total_sent += 1
                        except:
                            pass
                        
                        print(f"\r{Fore.GREEN}[✓] Sent: {total_sent} messages{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Sent: {total_sent} messages to {len(text_channel_ids)} rooms!")
            else:
                self.print_error("Failed to fetch channels!")
            input()
        except:
            self.print_error("Error spamming rooms!")
            input()
    
    async def give_admin(self):
        try:
            self.clear_screen()
            self.center_logo()
            self.center_text(Fore.MAGENTA + "══════════════════════════════════════════════════════════════")
            self.center_text(Fore.MAGENTA + "                       GIVE ADMIN")
            self.center_text(Fore.MAGENTA + "══════════════════════════════════════════════════════════════")
            print()
            
            print(Fore.CYAN + " " * 38 + ">>> User ID to promote: ", end="")
            user_id = input().strip()
            
            if not user_id:
                self.print_error("User ID cannot be empty!")
                input()
                return
            
            print()
            self.print_info(f"Promoting user: {user_id}")
            print()
            
            # Create role
            role_data = {
                "name": "3zF-Admin",
                "permissions": "1071698660929",
                "color": 10053376,
                "hoist": True,
                "mentionable": False
            }
            
            response = await self.api_request("POST", f"/guilds/{self.selected_guild_id}/roles", json_data=role_data)
            
            if response and response.status in [200, 201]:
                role = await response.json()
                role_id = role.get("id")
                
                self.print_success(f"Role created! ID: {role_id}")
                print()
                
                # Assign role
                assign_data = {"roles": [role_id]}
                assign_response = await self.api_request("PATCH", f"/guilds/{self.selected_guild_id}/members/{user_id}", json_data=assign_data)
                
                if assign_response and assign_response.status in [200, 204]:
                    self.print_success(f"User {user_id} is now admin!")
                else:
                    self.print_error("Role created but failed to assign!")
            else:
                self.print_error("Failed to create role!")
            input()
        except:
            self.print_error("Error giving admin!")
            input()
    
    async def run(self):
        try:
            await self.get_token()
            await self.get_guilds()
            await self.select_guild()
            await self.main_menu()
        except KeyboardInterrupt:
            print()
            self.print_info("Exiting...")
            sys.exit(0)
        except Exception as e:
            self.print_error(f"Fatal Error: {str(e)}")
            input()
        finally:
            if self.session:
                await self.session.close()

def main():
    tool = _3zFTool()
    try:
        asyncio.run(tool.run())
    except KeyboardInterrupt:
        print()
        print(Fore.CYAN + "[*] Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[-] Error: {str(e)}")
        input()

if __name__ == "__main__":
    main()

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
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def center_text(self, text):
        import re
        clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        width = 110
        padding = (width - len(clean_text)) // 2
        if padding < 0:
            padding = 0
        print(" " * padding + text)
    
    def center_logo(self):
        logo = [
            "██╗  ██╗   █████╗   ██████╗   ██████╗  ██████╗ ██╗  ██╗ ███████╗ ██████╗",
            "██║  ██║  ██╔══██╗  ╚════██╗ ██╔════╝ ██╔════╝ ██║ ██╔╝ ██╔════╝ ██╔══██╗",
            "███████║  ███████║   █████╔╝ ██║      ██║      █████╔╝  █████╗   ██████╔╝",
            "██╔══██║  ██╔══██║   ╚═══██╗ ██║      ██║      ██╔═██╗  ██╔══╝   ██╔══██╗",
            "██║  ██║  ██║  ██║  ██████╔╝ ╚██████╗ ╚██████╗ ██║  ██╗ ███████╗ ██║  ██║",
            "╚═╝  ╚═╝  ╚═╝  ╚═╝  ╚═════╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝  ╚═╝"
        ]
        print()
        for line in logo:
            print(Fore.CYAN + " " * 35 + line)
        print()
        self.center_text(Fore.YELLOW + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.YELLOW + "║                                                                               ║")
        self.center_text(Fore.YELLOW + "║" + Fore.MAGENTA + "                    3zF TOOL v2.0 | BY 3Z" + Fore.YELLOW + "                     ║")
        self.center_text(Fore.YELLOW + "║                                                                               ║")
        self.center_text(Fore.YELLOW + "╚═══════════════════════════════════════════════════════════════════════════════╝")
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
            print(Fore.GREEN + " " * 38 + f"{counter}. ", end="")
            user_input = input()
            
            if not user_input.strip():
                continue
            
            if user_input.lower() == done_word.lower():
                break
            
            items.append(user_input)
            counter += 1
        
        print()
        print(Fore.CYAN + " " * 38 + "Repeat count for each item: ", end="")
        try:
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
        if self.session is None:
            connector = aiohttp.TCPConnector(limit=200, limit_per_host=200, ttl_dns_cache=300)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self.session
    
    async def api_request(self, method, endpoint, headers=None, json_data=None, retries=3):
        session = await self.get_session()
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {
                "Authorization": f"Bot {self.bot_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        
        for attempt in range(retries):
            try:
                async with session.request(method, url, headers=headers, json=json_data) as response:
                    if response.status == 429:
                        data = await response.json()
                        retry_after = data.get('retry_after', 1)
                        await asyncio.sleep(retry_after)
                        continue
                    if response.status == 403:
                        self.print_error("Bot doesn't have permission!")
                        return response
                    return response
            except Exception as e:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
    
    async def get_token(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║                           ENTER BOT TOKEN                                  ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        print()
        self.center_text(Fore.YELLOW + "Paste your Bot Token and press Enter")
        print()
        print(Fore.GREEN + " " * 38 + ">>> ", end="")
        self.bot_token = input().strip()
        await self.test_token()
    
    async def test_token(self):
        self.clear_screen()
        self.center_logo()
        self.print_working()
        print()
        
        try:
            response = await self.api_request("GET", "/users/@me")
            if response.status == 200:
                user_data = await response.json()
                self.print_success(f"Bot Connected: {user_data.get('username', 'Unknown')}")
                print()
                self.center_text(Fore.YELLOW + "Press any key to continue...")
                input()
            else:
                self.print_error(f"Invalid Token! Status: {response.status}")
                print()
                self.center_text(Fore.YELLOW + "Press any key to try again...")
                input()
                await self.get_token()
        except Exception as e:
            self.print_error(f"Connection Error: {str(e)}")
            print()
            self.center_text(Fore.YELLOW + "Press any key to try again...")
            input()
            await self.get_token()
    
    async def get_guilds(self):
        self.clear_screen()
        self.center_logo()
        print()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║                           FETCHING SERVERS                                ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        print()
        
        try:
            response = await self.api_request("GET", "/users/@me/guilds")
            
            if response.status == 200:
                guilds_data = await response.json()
                self.guilds = {}
                
                self.center_text(Fore.MAGENTA + "╔═══════════════════════════════════════════════════════════════════════════════╗")
                self.center_text(Fore.MAGENTA + "║                           AVAILABLE SERVERS                                ║")
                self.center_text(Fore.MAGENTA + "╚═══════════════════════════════════════════════════════════════════════════════╝")
                print()
                
                for index, guild in enumerate(guilds_data, start=1):
                    guild_id = guild["id"]
                    guild_name = guild["name"]
                    self.guilds[str(index)] = guild_id
                    self.center_text(Fore.GREEN + f"[{index}] {guild_name} (ID: {guild_id})")
                
                print()
                self.center_text(Fore.YELLOW + "┌─────────────────────────────────────────────────────────────────────────────────┐")
                self.center_text(Fore.YELLOW + "│                    Enter number to select server                             │")
                self.center_text(Fore.YELLOW + "└─────────────────────────────────────────────────────────────────────────────────┘")
                print()
            else:
                self.print_error(f"Failed to fetch servers! Status: {response.status}")
                input()
                sys.exit(0)
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
            input()
            sys.exit(0)
    
    async def select_guild(self):
        while True:
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
    
    async def main_menu(self):
        while True:
            self.clear_screen()
            self.center_logo()
            
            self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════════════════════════════════════════╗")
            self.center_text(Fore.CYAN + "║                               MAIN MENU                                    ║")
            self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════════════════════════════════════════╝")
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
    
    async def create_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.GREEN + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.GREEN + "║                             CREATE ROOMS                                   ║")
        self.center_text(Fore.GREEN + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        
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
        semaphore = asyncio.Semaphore(100)
        progress_lock = asyncio.Lock()
        
        async def create_room(room_name):
            nonlocal success, failed
            async with semaphore:
                data = {"name": room_name, "type": 0}
                try:
                    response = await self.api_request("POST", f"/guilds/{self.selected_guild_id}/channels", json_data=data)
                    async with progress_lock:
                        if response.status in [200, 201]:
                            success += 1
                        else:
                            failed += 1
                except:
                    async with progress_lock:
                        failed += 1
        
        tasks = [create_room(name) for name in room_names]
        
        # Show progress
        import asyncio as aio
        for i in range(0, len(tasks), 50):
            batch = tasks[i:i+50]
            await asyncio.gather(*batch)
            print(f"\r{Fore.GREEN}[✓] Created: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
        
        print()
        self.print_success(f"Created: {success} rooms")
        if failed > 0:
            self.print_info(f"Failed: {failed} rooms")
        input()
    
    async def delete_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║                             DELETE ROOMS                                   ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        print()
        
        self.print_info("Fetching channels...")
        print()
        
        try:
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/channels")
            
            if response.status == 200:
                channels = await response.json()
                channel_ids = []
                
                for channel in channels:
                    if channel["type"] in [0, 2]:
                        channel_ids.append(channel["id"])
                
                if not channel_ids:
                    self.print_error("No channels found!")
                    input()
                    return
                
                self.print_info(f"Found {len(channel_ids)} channels")
                print()
                
                self.print_warning(f"Delete {len(channel_ids)} channels? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Cancelled.")
                    input()
                    return
                
                success = 0
                failed = 0
                semaphore = asyncio.Semaphore(100)
                progress_lock = asyncio.Lock()
                
                async def delete_channel(cid):
                    nonlocal success, failed
                    async with semaphore:
                        try:
                            response = await self.api_request("DELETE", f"/channels/{cid}")
                            async with progress_lock:
                                if response.status in [200, 204]:
                                    success += 1
                                else:
                                    failed += 1
                        except:
                            async with progress_lock:
                                failed += 1
                
                tasks = [delete_channel(cid) for cid in channel_ids]
                
                import asyncio as aio
                for i in range(0, len(tasks), 50):
                    batch = tasks[i:i+50]
                    await asyncio.gather(*batch)
                    print(f"\r{Fore.GREEN}[✓] Deleted: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Deleted: {success} rooms")
                if failed > 0:
                    self.print_info(f"Failed: {failed} rooms")
            else:
                self.print_error(f"Failed! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    async def delete_roles(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║                              DELETE ROLES                                  ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        print()
        
        self.print_info("Fetching roles...")
        print()
        
        try:
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/roles")
            
            if response.status == 200:
                roles = await response.json()
                role_ids = []
                
                for role in roles:
                    if role["id"] != self.selected_guild_id:
                        role_ids.append(role["id"])
                
                if not role_ids:
                    self.print_error("No roles found!")
                    input()
                    return
                
                self.print_info(f"Found {len(role_ids)} roles")
                print()
                
                self.print_warning(f"Delete {len(role_ids)} roles? (yes/no): ", end="")
                confirm = input().strip().lower()
                
                if confirm != 'yes':
                    self.print_info("Cancelled.")
                    input()
                    return
                
                success = 0
                failed = 0
                semaphore = asyncio.Semaphore(100)
                progress_lock = asyncio.Lock()
                
                async def delete_role(rid):
                    nonlocal success, failed
                    async with semaphore:
                        try:
                            response = await self.api_request("DELETE", f"/guilds/{self.selected_guild_id}/roles/{rid}")
                            async with progress_lock:
                                if response.status in [200, 204]:
                                    success += 1
                                else:
                                    failed += 1
                        except:
                            async with progress_lock:
                                failed += 1
                
                tasks = [delete_role(rid) for rid in role_ids]
                
                import asyncio as aio
                for i in range(0, len(tasks), 50):
                    batch = tasks[i:i+50]
                    await asyncio.gather(*batch)
                    print(f"\r{Fore.GREEN}[✓] Deleted: {success}  |  {Fore.RED}[✗] Failed: {failed}{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Deleted: {success} roles")
                if failed > 0:
                    self.print_info(f"Failed: {failed} roles")
            else:
                self.print_error(f"Failed! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    async def ban_user(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.RED + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.RED + "║                               BAN USER                                    ║")
        self.center_text(Fore.RED + "╚═══════════════════════════════════════════════════════════════════════════════╝")
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
        
        try:
            data = {"delete_message_days": 7}
            response = await self.api_request("PUT", f"/guilds/{self.selected_guild_id}/bans/{user_id}", json_data=data)
            
            if response.status in [200, 204]:
                self.print_success(f"User {user_id} banned!")
            else:
                self.print_error(f"Failed! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    async def kick_user(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.YELLOW + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.YELLOW + "║                               KICK USER                                    ║")
        self.center_text(Fore.YELLOW + "╚═══════════════════════════════════════════════════════════════════════════════╝")
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
        
        try:
            response = await self.api_request("DELETE", f"/guilds/{self.selected_guild_id}/members/{user_id}")
            
            if response.status in [200, 204]:
                self.print_success(f"User {user_id} kicked!")
            else:
                self.print_error(f"Failed! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    async def spam_rooms(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.CYAN + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.CYAN + "║                              SPAM ROOMS                                   ║")
        self.center_text(Fore.CYAN + "╚═══════════════════════════════════════════════════════════════════════════════╝")
        
        spam_messages = self.get_multiple_inputs_with_count("Enter spam messages (one per line):")
        
        if len(spam_messages) == 0:
            self.print_error("No messages entered!")
            input()
            return
        
        print()
        self.print_info("Fetching text channels...")
        print()
        
        try:
            response = await self.api_request("GET", f"/guilds/{self.selected_guild_id}/channels")
            
            if response.status == 200:
                channels = await response.json()
                text_channel_ids = []
                
                for channel in channels:
                    if channel["type"] == 0:
                        text_channel_ids.append(channel["id"])
                
                if not text_channel_ids:
                    self.print_error("No text channels found!")
                    input()
                    return
                
                self.print_info(f"Found {len(text_channel_ids)} text channels")
                print()
                
                total_sent = 0
                semaphore = asyncio.Semaphore(200)
                progress_lock = asyncio.Lock()
                
                async def send_message(cid, msg):
                    nonlocal total_sent
                    async with semaphore:
                        try:
                            data = {"content": msg}
                            response = await self.api_request("POST", f"/channels/{cid}/messages", json_data=data)
                            async with progress_lock:
                                if response.status in [200, 201]:
                                    total_sent += 1
                        except:
                            pass
                
                tasks = []
                for cid in text_channel_ids:
                    for msg in spam_messages:
                        tasks.append(send_message(cid, msg))
                
                import asyncio as aio
                for i in range(0, len(tasks), 100):
                    batch = tasks[i:i+100]
                    await asyncio.gather(*batch)
                    print(f"\r{Fore.GREEN}[✓] Sent: {total_sent} messages{Style.RESET_ALL}", end="")
                
                print()
                self.print_success(f"Sent: {total_sent} messages to {len(text_channel_ids)} rooms!")
            else:
                self.print_error(f"Failed! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
        input()
    
    async def give_admin(self):
        self.clear_screen()
        self.center_logo()
        self.center_text(Fore.MAGENTA + "╔═══════════════════════════════════════════════════════════════════════════════╗")
        self.center_text(Fore.MAGENTA + "║                              GIVE ADMIN                                   ║")
        self.center_text(Fore.MAGENTA + "╚═══════════════════════════════════════════════════════════════════════════════╝")
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
        
        try:
            # Create role
            role_data = {
                "name": "3zF-Admin",
                "permissions": "1071698660929",
                "color": 10053376,
                "hoist": True,
                "mentionable": False
            }
            
            response = await self.api_request("POST", f"/guilds/{self.selected_guild_id}/roles", json_data=role_data)
            
            if response.status in [200, 201]:
                role = await response.json()
                role_id = role["id"]
                
                self.print_success(f"Role created! ID: {role_id}")
                print()
                
                # Assign role
                assign_data = {"roles": [role_id]}
                assign_response = await self.api_request("PATCH", f"/guilds/{self.selected_guild_id}/members/{user_id}", json_data=assign_data)
                
                if assign_response.status in [200, 204]:
                    self.print_success(f"User {user_id} is now admin!")
                else:
                    self.print_error(f"Role created but failed to assign! Status: {assign_response.status}")
            else:
                self.print_error(f"Failed to create role! Status: {response.status}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")
        
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

if __name__ == "__main__":
    tool = _3zFTool()
    asyncio.run(tool.run())

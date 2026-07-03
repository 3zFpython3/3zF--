
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

namespace _3zFTool
{
    class Program
    {
        static string botToken = "";
        static string selectedGuildId = "";
        static Dictionary<string, string> guilds = new Dictionary<string, string>();

        static async Task Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;
            Console.Title = "3zF 🦇 | BY 3Z";
            Console.WindowWidth = 90;
            Console.WindowHeight = 45;

            // Step 1: Enter Token
            Console.Clear();
            CenterLogo();
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║         ENTER BOT TOKEN                 ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Yellow;
            CenterText("┌─────────────────────────────────────────┐");
            CenterText("│  Paste your Bot Token and press Enter  │");
            CenterText("└─────────────────────────────────────────┘");
            Console.ResetColor();
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write(new string(' ', 35) + "➜ ");
            Console.ForegroundColor = ConsoleColor.White;
            botToken = Console.ReadLine();

            // Step 2: Get Servers
            await GetGuilds();

            // Step 3: Select Server
            await SelectGuild();

            // Step 4: Show Main Menu
            await MainMenu();
        }

        static async Task GetGuilds()
        {
            Console.Clear();
            CenterLogo();
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║        FETCHING SERVERS...              ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                try
                {
                    var res = await client.GetAsync("https://discord.com/api/v9/users/@me/guilds");
                    string body = await res.Content.ReadAsStringAsync();

                    if (res.IsSuccessStatusCode)
                    {
                        var json = JsonDocument.Parse(body);
                        var guildsArray = json.RootElement.EnumerateArray();

                        int index = 1;
                        guilds.Clear();

                        Console.ForegroundColor = ConsoleColor.Magenta;
                        CenterText("╔═══════════════════════════════════════════╗");
                        CenterText("║         AVAILABLE SERVERS               ║");
                        CenterText("╚═══════════════════════════════════════════╝");
                        Console.ResetColor();
                        Console.WriteLine();

                        foreach (var guild in guildsArray)
                        {
                            string id = guild.GetProperty("id").GetString();
                            string name = guild.GetProperty("name").GetString();
                            guilds[index.ToString()] = id;
                            
                            Console.ForegroundColor = ConsoleColor.Green;
                            CenterText($"[{index}] {name} (ID: {id})");
                            Console.ResetColor();
                            index++;
                        }

                        Console.WriteLine();
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        CenterText("┌─────────────────────────────────────────┐");
                        CenterText("│  Enter number to select server        │");
                        CenterText("└─────────────────────────────────────────┘");
                        Console.ResetColor();
                        Console.WriteLine();
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        CenterText("❌ Failed to fetch servers! Invalid Token?");
                        Console.ResetColor();
                        Console.ReadKey();
                        Environment.Exit(0);
                    }
                }
                catch
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    CenterText("❌ Error connecting to Discord API!");
                    Console.ResetColor();
                    Console.ReadKey();
                    Environment.Exit(0);
                }
            }
        }

        static async Task SelectGuild()
        {
            while (true)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write(new string(' ', 35) + "➜ Select Server: ");
                Console.ForegroundColor = ConsoleColor.White;
                string choice = Console.ReadLine();

                if (guilds.ContainsKey(choice))
                {
                    selectedGuildId = guilds[choice];
                    Console.Clear();
                    CenterLogo();
                    Console.ForegroundColor = ConsoleColor.Green;
                    CenterText($"✅ Server Selected Successfully!");
                    Console.ResetColor();
                    Console.WriteLine();
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    CenterText($"➜ Server ID: {selectedGuildId}");
                    Console.ResetColor();
                    Console.WriteLine();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    CenterText("Press any key to continue...");
                    Console.ResetColor();
                    Console.ReadKey();
                    return;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    CenterText("❌ Invalid choice! Try again.");
                    Console.ResetColor();
                    Console.WriteLine();
                }
            }
        }

        static async Task MainMenu()
        {
            while (true)
            {
                Console.Clear();
                CenterLogo();
                
                Console.ForegroundColor = ConsoleColor.Cyan;
                CenterText("╔═══════════════════════════════════════════╗");
                CenterText("║           🚀 MAIN MENU                  ║");
                CenterText("╚═══════════════════════════════════════════╝");
                Console.ResetColor();
                Console.WriteLine();

                string[] menu = new string[]
                {
                    "  [1]  Create Rooms    انشاء رومات",
                    "  [2]  Delete Rooms    حذف رومات",
                    "  [3]  Delete Roles    حذف رتب",
                    "  [4]  Ban User        باند",
                    "  [5]  Kick User       طرد",
                    "  [6]  Spam Rooms      سبام",
                    "  [7]  Give Admin      رفع مشرف",
                    "  [0]  Exit            خروج"
                };

                foreach (var item in menu)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    CenterText(item);
                    Console.ResetColor();
                }

                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Green;
                CenterText($"➜ Server ID: {selectedGuildId}");
                Console.ResetColor();
                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.Write(new string(' ', 35) + "➜ Choose Option: ");
                Console.ForegroundColor = ConsoleColor.White;
                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1": await CreateRooms(); break;
                    case "2": await DeleteRooms(); break;
                    case "3": await DeleteRoles(); break;
                    case "4": await BanUser(); break;
                    case "5": await KickUser(); break;
                    case "6": await SpamRooms(); break;
                    case "7": await GiveAdmin(); break;
                    case "0": return;
                    default:
                        Console.ForegroundColor = ConsoleColor.Red;
                        CenterText("❌ Invalid option!");
                        Console.ResetColor();
                        System.Threading.Thread.Sleep(1000);
                        break;
                }
            }
        }

        static void CenterText(string text)
        {
            int padding = (Console.WindowWidth - text.Length) / 2;
            if (padding < 0) padding = 0;
            Console.WriteLine(new string(' ', padding) + text);
        }

        static void CenterLogo()
        {
            string[] logo = new string[]
            {
                @"██████╗░██████╗░",
                @"╚════██╗╚════██╗",
                @"░░███╔═╝░░███╔═╝",
                @"██╔══╝░░██╔══╝░░",
                @"███████╗███████╗",
                @"╚══════╝╚══════╝"
            };

            Console.WriteLine("");
            foreach (string line in logo)
            {
                Console.ForegroundColor = ConsoleColor.Magenta;
                CenterText(line);
                Console.ResetColor();
            }
            Console.WriteLine("");
            Console.ForegroundColor = ConsoleColor.Yellow;
            CenterText("═══════════════════════════════════════════");
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("     3zF 🦇  TOOL v1.0 | BY 3Z");
            Console.ForegroundColor = ConsoleColor.Yellow;
            CenterText("═══════════════════════════════════════════");
            Console.ResetColor();
        }

        static void PrintSuccess(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            CenterText("✅ " + msg);
            Console.ResetColor();
        }

        static void PrintError(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            CenterText("❌ " + msg);
            Console.ResetColor();
        }

        static void PrintInfo(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("ℹ️ " + msg);
            Console.ResetColor();
        }

        static string RandomString(int length)
        {
            const string chars = "abcdefghijklmnopqrstuvwxyz0123456789";
            Random rnd = new Random();
            char[] result = new char[length];
            for (int i = 0; i < length; i++)
                result[i] = chars[rnd.Next(chars.Length)];
            return new string(result);
        }

        // ============ GET MULTIPLE INPUTS ============
        static List<string> GetMultipleInputs(string prompt, string doneWord = "done")
        {
            List<string> items = new List<string>();
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText($"📝 {prompt}");
            CenterText($"Type '{doneWord}' when finished");
            Console.ResetColor();
            Console.WriteLine();

            int counter = 1;
            while (true)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write(new string(' ', 35) + $"{counter}. ");
                Console.ForegroundColor = ConsoleColor.White;
                string input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                    continue;

                if (input.ToLower() == doneWord.ToLower())
                    break;

                items.Add(input);
                counter++;
            }

            return items;
        }

        // ============ 1- CREATE ROOMS (WITH CUSTOM NAMES) ============
        static async Task CreateRooms()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Green;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║        CREATE ROOMS - انشاء رومات       ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();

            var roomNames = GetMultipleInputs("Enter room names (one per line):");

            if (roomNames.Count == 0)
            {
                PrintError("No room names entered!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            PrintInfo($"Creating {roomNames.Count} rooms...");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                int success = 0, failed = 0;

                for (int i = 0; i < roomNames.Count; i++)
                {
                    string json = $"{{\"name\":\"{roomNames[i]}\",\"type\":0}}";
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    try
                    {
                        var res = await client.PostAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/channels", content);
                        if (res.IsSuccessStatusCode) success++;
                        else failed++;
                    }
                    catch { failed++; }

                    Console.Write($"\r{" ".PadLeft(50)}");
                    Console.Write($"\r✅ Created: {success}  |  ❌ Failed: {failed}  |  Room: {roomNames[i]}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{success} rooms created successfully!");
                if (failed > 0)
                    PrintInfo($"Failed: {failed} rooms");
            }
            Console.ReadKey();
        }

        // ============ 6- SPAM ROOMS (WITH CUSTOM MESSAGES) ============
        static async Task SpamRooms()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║           SPAM ROOMS - سبام             ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();

            var spamMessages = GetMultipleInputs("Enter spam messages (one per line):");

            if (spamMessages.Count == 0)
            {
                PrintError("No messages entered!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write(new string(' ', 35) + "➜ Messages per room: ");
            Console.ForegroundColor = ConsoleColor.White;
            string msgsStr = Console.ReadLine();

            if (!int.TryParse(msgsStr, out int msgsPerRoom) || msgsPerRoom <= 0)
            {
                PrintError("Invalid number!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            PrintInfo("Fetching text channels...");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/channels");
                string body = await res.Content.ReadAsStringAsync();

                var textChannelIds = new List<string>();
                int idx = 0;
                while ((idx = body.IndexOf("\"id\":\"", idx)) != -1)
                {
                    idx += 6;
                    int end = body.IndexOf("\"", idx);
                    if (end > idx)
                    {
                        string cid = body.Substring(idx, end - idx);
                        int typeIdx = body.LastIndexOf("\"type\":", idx);
                        if (typeIdx != -1 && typeIdx < end + 10)
                        {
                            string typeVal = body.Substring(typeIdx + 7, 1);
                            if (typeVal == "0")
                                textChannelIds.Add(cid);
                        }
                    }
                }

                PrintInfo($"Found {textChannelIds.Count} text channels.");
                Console.WriteLine();

                int totalSent = 0;
                Random rnd = new Random();

                foreach (string cid in textChannelIds)
                {
                    for (int m = 0; m < msgsPerRoom; m++)
                    {
                        try
                        {
                            string txt = spamMessages[rnd.Next(spamMessages.Count)];
                            string json = $"{{\"content\":\"{txt}\"}}";
                            var content = new StringContent(json, Encoding.UTF8, "application/json");
                            var send = await client.PostAsync($"https://discord.com/api/v9/channels/{cid}/messages", content);
                            if (send.IsSuccessStatusCode) totalSent++;
                        }
                        catch { }

                        Console.Write($"\r{" ".PadLeft(50)}");
                        Console.Write($"\r✅ Sent: {totalSent} messages");
                    }
                }

                Console.WriteLine("\n");
                PrintSuccess($"{totalSent} messages sent to {textChannelIds.Count} rooms!");
            }
            Console.ReadKey();
        }

        // ============ 2- DELETE ROOMS ============
        static async Task DeleteRooms()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Red;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║        DELETE ROOMS - حذف رومات         ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            PrintInfo("Fetching channels...");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/channels");
                string body = await res.Content.ReadAsStringAsync();

                var channelIds = new List<string>();
                int idx = 0;
                while ((idx = body.IndexOf("\"id\":\"", idx)) != -1)
                {
                    idx += 6;
                    int end = body.IndexOf("\"", idx);
                    if (end > idx)
                    {
                        string cid = body.Substring(idx, end - idx);
                        int typeIdx = body.LastIndexOf("\"type\":", idx);
                        if (typeIdx != -1 && typeIdx < end + 10)
                        {
                            string typeVal = body.Substring(typeIdx + 7, 1);
                            if (typeVal == "0" || typeVal == "2")
                                channelIds.Add(cid);
                        }
                    }
                }

                PrintInfo($"Found {channelIds.Count} channels to delete.");
                Console.WriteLine();

                int delOk = 0, delFail = 0;
                foreach (string cid in channelIds)
                {
                    try
                    {
                        var del = await client.DeleteAsync($"https://discord.com/api/v9/channels/{cid}");
                        if (del.IsSuccessStatusCode) delOk++;
                        else delFail++;
                    }
                    catch { delFail++; }

                    Console.Write($"\r{" ".PadLeft(50)}");
                    Console.Write($"\r✅ Deleted: {delOk}  |  ❌ Failed: {delFail}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{delOk} rooms deleted successfully!");
                Console.WriteLine();
                PrintInfo($"Failed: {delFail} rooms");
            }
            Console.ReadKey();
        }

        // ============ 3- DELETE ROLES ============
        static async Task DeleteRoles()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Red;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║         DELETE ROLES - حذف رتب          ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            PrintInfo("Fetching roles...");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/roles");
                string body = await res.Content.ReadAsStringAsync();

                var roleIds = new List<string>();
                int idx = 0;
                while ((idx = body.IndexOf("\"id\":\"", idx)) != -1)
                {
                    idx += 6;
                    int end = body.IndexOf("\"", idx);
                    if (end > idx)
                    {
                        string rid = body.Substring(idx, end - idx);
                        if (rid != selectedGuildId)
                            roleIds.Add(rid);
                    }
                }

                PrintInfo($"Found {roleIds.Count} roles to delete.");
                Console.WriteLine();

                int delOk = 0, delFail = 0;
                foreach (string rid in roleIds)
                {
                    try
                    {
                        var del = await client.DeleteAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/roles/{rid}");
                        if (del.IsSuccessStatusCode) delOk++;
                        else delFail++;
                    }
                    catch { delFail++; }

                    Console.Write($"\r{" ".PadLeft(50)}");
                    Console.Write($"\r✅ Deleted: {delOk}  |  ❌ Failed: {delFail}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{delOk} roles deleted successfully!");
                Console.WriteLine();
                PrintInfo($"Failed: {delFail} roles");
            }
            Console.ReadKey();
        }

        // ============ 4- BAN USER ============
        static async Task BanUser()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Red;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║           BAN USER - باند               ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write(new string(' ', 35) + "➜ User ID to ban: ");
            Console.ForegroundColor = ConsoleColor.White;
            string userId = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(userId))
            {
                PrintError("User ID cannot be empty!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            PrintInfo($"Attempting to ban user: {userId}");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                string json = "{\"delete_message_days\":7}";
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var res = await client.PutAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/bans/{userId}", content);

                if (res.IsSuccessStatusCode)
                {
                    PrintSuccess($"User {userId} banned successfully!");
                }
                else
                {
                    PrintError($"Failed to ban user! Status: {res.StatusCode}");
                }
            }
            Console.ReadKey();
        }

        // ============ 5- KICK USER ============
        static async Task KickUser()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║           KICK USER - طرد               ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write(new string(' ', 35) + "➜ User ID to kick: ");
            Console.ForegroundColor = ConsoleColor.White;
            string userId = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(userId))
            {
                PrintError("User ID cannot be empty!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            PrintInfo($"Attempting to kick user: {userId}");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.DeleteAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/members/{userId}");

                if (res.IsSuccessStatusCode)
                {
                    PrintSuccess($"User {userId} kicked successfully!");
                }
                else
                {
                    PrintError($"Failed to kick user! Status: {res.StatusCode}");
                }
            }
            Console.ReadKey();
        }

        // ============ 7- GIVE ADMIN ============
        static async Task GiveAdmin()
        {
            Console.Clear();
            CenterLogo();
            Console.ForegroundColor = ConsoleColor.Magenta;
            CenterText("╔═══════════════════════════════════════════╗");
            CenterText("║        GIVE ADMIN - رفع مشرف            ║");
            CenterText("╚═══════════════════════════════════════════╝");
            Console.ResetColor();
            Console.WriteLine();

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write(new string(' ', 35) + "➜ User ID to promote: ");
            Console.ForegroundColor = ConsoleColor.White;
            string userId = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(userId))
            {
                PrintError("User ID cannot be empty!");
                Console.ReadKey();
                return;
            }

            Console.WriteLine();
            PrintInfo($"Promoting user: {userId}");
            Console.WriteLine();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {botToken}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                string roleJson = $"{{\"name\":\"3zF-Admin\",\"permissions\":\"1071698660929\",\"color\":10053376,\"hoist\":true,\"mentionable\":false}}";
                var content = new StringContent(roleJson, Encoding.UTF8, "application/json");

                var roleRes = await client.PostAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/roles", content);
                string roleBody = await roleRes.Content.ReadAsStringAsync();

                if (roleRes.IsSuccessStatusCode)
                {
                    int idStart = roleBody.IndexOf("\"id\":\"") + 6;
                    int idEnd = roleBody.IndexOf("\"", idStart);
                    string roleId = roleBody.Substring(idStart, idEnd - idStart);

                    PrintInfo($"Role created! ID: {roleId}");
                    Console.WriteLine();

                    string assignJson = $"{{\"roles\":[\"{roleId}\"]}}";
                    var assignContent = new StringContent(assignJson, Encoding.UTF8, "application/json");
                    var assignRes = await client.PatchAsync($"https://discord.com/api/v9/guilds/{selectedGuildId}/members/{userId}", assignContent);

                    if (assignRes.IsSuccessStatusCode)
                    {
                        PrintSuccess($"User {userId} is now an admin! 🚀");
                    }
                    else
                    {
                        PrintError($"Role created but failed to assign! Status: {assignRes.StatusCode}");
                    }
                }
                else
                {
                    PrintError($"Failed to create admin role! Status: {roleRes.StatusCode}");
                }
            }
            Console.ReadKey();
        }
    }
}

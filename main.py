using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace _3zFTool
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;
            Console.Title = "3zF 🦇 | BY 3Z";
            Console.WindowWidth = 80;
            Console.WindowHeight = 40;

            while (true)
            {
                Console.Clear();
                CenterLogo();
                CenterMenu();
                
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
                        CenterText(" [!] INVALID OPTION!");
                        Console.ResetColor();
                        System.Threading.Thread.Sleep(1000);
                        break;
                }
            }
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
                CenterTextColored(line, ConsoleColor.Magenta);
            }
            Console.WriteLine("");

            CenterTextColored("═══════════════════════════════════", ConsoleColor.Yellow);
            CenterTextColored("     3zF 🦇  TOOL v1.0 | BY 3Z", ConsoleColor.Cyan);
            CenterTextColored("═══════════════════════════════════", ConsoleColor.Yellow);
            Console.WriteLine("");
        }

        static void CenterMenu()
        {
            string[] menu = new string[]
            {
                "╔═══════════════════════════════════╗",
                "║                                   ║",
                "║       🚀 MAIN MENU                ║",
                "║                                   ║",
                "║  [1]  Create Rooms  انشاء رومات  ║",
                "║  [2]  Delete Rooms  حذف رومات      ║",
                "║  [3]  Delete Roles  حذف رتب        ║",
                "║  [4]  Ban User      باند           ║",
                "║  [5]  Kick User     طرد            ║",
                "║  [6]  Spam Rooms    سبام           ║",
                "║  [7]  Give Admin    برو (رفع مشرف) ║",
                "║  [0]  Exit          خروج           ║",
                "║                                   ║",
                "╚═══════════════════════════════════╝"
            };

            ConsoleColor[] colors = new ConsoleColor[]
            {
                ConsoleColor.Magenta,
                ConsoleColor.Magenta,
                ConsoleColor.Yellow,
                ConsoleColor.Magenta,
                ConsoleColor.Green,
                ConsoleColor.Red,
                ConsoleColor.Red,
                ConsoleColor.Red,
                ConsoleColor.DarkYellow,
                ConsoleColor.DarkYellow,
                ConsoleColor.Cyan,
                ConsoleColor.Cyan,
                ConsoleColor.Magenta,
                ConsoleColor.Magenta
            };

            for (int i = 0; i < menu.Length; i++)
            {
                Console.ForegroundColor = colors[i];
                int padding = (Console.WindowWidth - menu[i].Length) / 2;
                if (padding < 0) padding = 0;
                Console.WriteLine(new string(' ', padding) + menu[i]);
            }

            Console.ResetColor();
            Console.WriteLine("");
            
            string prompt = "  >>> Select Number: ";
            Console.ForegroundColor = ConsoleColor.Green;
            int pad = (Console.WindowWidth - prompt.Length) / 2;
            if (pad < 0) pad = 0;
            Console.Write(new string(' ', pad));
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write(prompt);
            Console.ResetColor();
        }

        static void CenterText(string text)
        {
            int padding = (Console.WindowWidth - text.Length) / 2;
            if (padding < 0) padding = 0;
            Console.WriteLine(new string(' ', padding) + text);
        }

        static void CenterTextColored(string text, ConsoleColor color)
        {
            Console.ForegroundColor = color;
            int padding = (Console.WindowWidth - text.Length) / 2;
            if (padding < 0) padding = 0;
            Console.WriteLine(new string(' ', padding) + text);
            Console.ResetColor();
        }

        static async Task<string> GetToken()
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            string txt = "  [?] Bot Token: ";
            int pad = (Console.WindowWidth - txt.Length) / 2;
            if (pad < 0) pad = 0;
            Console.Write(new string(' ', pad));
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write(txt);
            Console.ResetColor();
            return Console.ReadLine();
        }

        static async Task<string> GetGuildID()
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            string txt = "  [?] Server ID (Guild ID): ";
            int pad = (Console.WindowWidth - txt.Length) / 2;
            if (pad < 0) pad = 0;
            Console.Write(new string(' ', pad));
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write(txt);
            Console.ResetColor();
            return Console.ReadLine();
        }

        static async Task<string> GetInput(string prompt)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            int pad = (Console.WindowWidth - prompt.Length) / 2;
            if (pad < 0) pad = 0;
            Console.Write(new string(' ', pad));
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write(prompt);
            Console.ResetColor();
            return Console.ReadLine();
        }

        static void PrintSuccess(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            CenterText("[✓] " + msg);
            Console.ResetColor();
        }

        static void PrintError(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            CenterText("[✗] " + msg);
            Console.ResetColor();
        }

        static void PrintInfo(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            CenterText("[*] " + msg);
            Console.ResetColor();
        }

        static void PrintWorking()
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            CenterText("[*] WORKING... PLEASE WAIT");
            Console.ResetColor();
        }

        // ============ 1- CREATE ROOMS ============
        static async Task CreateRooms()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Green);
            CenterTextColored("║     CREATE ROOMS - انشاء رومات║", ConsoleColor.Green);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Green);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();
            string countStr = await GetInput("  [?] How many rooms to create: ");
            int count = int.Parse(countStr);

            PrintWorking();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                int success = 0, failed = 0;

                for (int i = 0; i < count; i++)
                {
                    string roomName = $"3zF-{RandomString(5)}";
                    string json = $"{{\"name\":\"{roomName}\",\"type\":2}}";
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    try
                    {
                        var res = await client.PostAsync($"https://discord.com/api/v9/guilds/{guildId}/channels", content);
                        if (res.IsSuccessStatusCode) success++;
                        else failed++;
                    }
                    catch { failed++; }

                    Console.Write($"\r  [+] Created: {success}  |  Failed: {failed}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{success} Rooms Created Successfully!");
            }
            Console.ReadKey();
        }

        // ============ 2- DELETE ROOMS ============
        static async Task DeleteRooms()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Red);
            CenterTextColored("║     DELETE ROOMS - حذف رومات   ║", ConsoleColor.Red);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Red);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();

            PrintInfo("Fetching channels...");

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{guildId}/channels");
                string body = await res.Content.ReadAsStringAsync();

                var channelIds = new List<string>();
                int idx = 0;
                while ((idx = body.IndexOf("\"id\":\"", idx)) != -1)
                {
                    idx += 6;
                    int end = body.IndexOf("\"", idx);
                    channelIds.Add(body.Substring(idx, end - idx));
                }

                PrintInfo($"Found {channelIds.Count} channels. Deleting...");

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

                    Console.Write($"\r  [+] Deleted: {delOk}  |  Failed: {delFail}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{delOk} Rooms Deleted Successfully!");
            }
            Console.ReadKey();
        }

        // ============ 3- DELETE ROLES ============
        static async Task DeleteRoles()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Red);
            CenterTextColored("║     DELETE ROLES - حذف رتب    ║", ConsoleColor.Red);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Red);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();

            PrintInfo("Fetching roles...");

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{guildId}/roles");
                string body = await res.Content.ReadAsStringAsync();

                var roleIds = new List<string>();
                int idx = 0;
                while ((idx = body.IndexOf("\"id\":\"", idx)) != -1)
                {
                    idx += 6;
                    int end = body.IndexOf("\"", idx);
                    string rid = body.Substring(idx, end - idx);
                    if (rid != guildId && !roleIds.Contains(rid))
                        roleIds.Add(rid);
                }

                PrintInfo($"Found {roleIds.Count} roles. Deleting...");

                int delOk = 0, delFail = 0;
                foreach (string rid in roleIds)
                {
                    try
                    {
                        var del = await client.DeleteAsync($"https://discord.com/api/v9/guilds/{guildId}/roles/{rid}");
                        if (del.IsSuccessStatusCode) delOk++;
                        else delFail++;
                    }
                    catch { delFail++; }

                    Console.Write($"\r  [+] Deleted: {delOk}  |  Failed: {delFail}");
                }

                Console.WriteLine("\n");
                PrintSuccess($"{delOk} Roles Deleted Successfully!");
            }
            Console.ReadKey();
        }

        // ============ 4- BAN USER ============
        static async Task BanUser()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Red);
            CenterTextColored("║        BAN USER - باند        ║", ConsoleColor.Red);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Red);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();
            string userId = await GetInput("  [?] User ID: ");

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                string json = "{\"delete_message_days\":7}";
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var res = await client.PutAsync($"https://discord.com/api/v9/guilds/{guildId}/bans/{userId}", content);

                if (res.IsSuccessStatusCode)
                    PrintSuccess($"User {userId} Banned Successfully!");
                else
                    PrintError($"Failed to ban user! ({res.StatusCode})");
            }
            Console.ReadKey();
        }

        // ============ 5- KICK USER ============
        static async Task KickUser()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.DarkYellow);
            CenterTextColored("║       KICK USER - طرد         ║", ConsoleColor.DarkYellow);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.DarkYellow);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();
            string userId = await GetInput("  [?] User ID: ");

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.DeleteAsync($"https://discord.com/api/v9/guilds/{guildId}/members/{userId}");

                if (res.IsSuccessStatusCode)
                    PrintSuccess($"User {userId} Kicked Successfully!");
                else
                    PrintError($"Failed to kick user! ({res.StatusCode})");
            }
            Console.ReadKey();
        }

        // ============ 6- SPAM ALL ROOMS ============
        static async Task SpamRooms()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Cyan);
            CenterTextColored("║     SPAM ROOMS - سبام         ║", ConsoleColor.Cyan);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Cyan);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();
            string msgsStr = await GetInput("  [?] Messages per room: ");
            int msgsPerRoom = int.Parse(msgsStr);

            PrintInfo("Fetching channels...");

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                var res = await client.GetAsync($"https://discord.com/api/v9/guilds/{guildId}/channels");
                string body = await res.Content.ReadAsStringAsync();

                var textChannelIds = new List<string>();
                string searchId = "\"id\":\"";
                string searchType = "\"type\":";
                int pos = 0;

                while ((pos = body.IndexOf(searchId, pos)) != -1)
                {
                    pos += 6;
                    int end = body.IndexOf("\"", pos);
                    string cid = body.Substring(pos, end - pos);

                    int typePos = body.LastIndexOf(searchType, pos);
                    if (typePos != -1)
                    {
                        int typeStart = typePos + searchType.Length;
                        string typeVal = body.Substring(typeStart, 1);
                        if (typeVal == "0") textChannelIds.Add(cid);
                    }
                }

                PrintInfo($"Found {textChannelIds.Count} text channels. Spamming...");

                string[] spamTexts = new string[]
                {
                    "3zF 🦇",
                    "BY 3Z",
                    "3zF 🦇 | BY 3Z",
                    "3zF On Top",
                    "3zF Forever",
                    "3zF Team",
                    "3zF 🦇🦇🦇",
                    "3zF Tool",
                    "3zF 🦇 3zF 🦇",
                    "3zF Number 1"
                };

                int totalSent = 0;
                Random rnd = new Random();

                foreach (string cid in textChannelIds)
                {
                    for (int m = 0; m < msgsPerRoom; m++)
                    {
                        try
                        {
                            string txt = spamTexts[rnd.Next(spamTexts.Length)];
                            string json = $"{{\"content\":\"{txt}\"}}";
                            var content = new StringContent(json, Encoding.UTF8, "application/json");
                            var send = await client.PostAsync($"https://discord.com/api/v9/channels/{cid}/messages", content);
                            if (send.IsSuccessStatusCode) totalSent++;
                        }
                        catch { }

                        Console.Write($"\r  [+] Sent: {totalSent} messages");
                    }
                }

                Console.WriteLine("\n");
                PrintSuccess($"{totalSent} Messages Sent to {textChannelIds.Count} Rooms!");
            }
            Console.ReadKey();
        }

        // ============ 7- GIVE ADMIN (PRO) ============
        static async Task GiveAdmin()
        {
            Console.Clear();
            CenterLogo();
            CenterTextColored("╔═══════════════════════════════╗", ConsoleColor.Magenta);
            CenterTextColored("║   GIVE ADMIN PRO - رفع مشرف  ║", ConsoleColor.Magenta);
            CenterTextColored("╚═══════════════════════════════╝", ConsoleColor.Magenta);
            Console.WriteLine("");

            string token = await GetToken();
            string guildId = await GetGuildID();
            string userId = await GetInput("  [?] User ID: ");

            PrintWorking();

            using (HttpClient client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Authorization", $"Bot {token}");
                client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");

                // All permissions = 1071698660929 (includes admin)
                string roleJson = $"{{\"name\":\"3zF\",\"permissions\":1071698660929,\"color\":10053376}}";
                var content = new StringContent(roleJson, Encoding.UTF8, "application/json");

                var roleRes = await client.PostAsync($"https://discord.com/api/v9/guilds/{guildId}/roles", content);
                string roleBody = await roleRes.Content.ReadAsStringAsync();

                if (roleRes.IsSuccessStatusCode)
                {
                    int idStart = roleBody.IndexOf("\"id\":\"") + 6;
                    int idEnd = roleBody.IndexOf("\"", idStart);
                    string roleId = roleBody.Substring(idStart, idEnd - idStart);

                    string assignJson = $"{{\"roles\":[\"{roleId}\"]}}";
                    var assignContent = new StringContent(assignJson, Encoding.UTF8, "application/json");
                    var assignRes = await client.PatchAsync($"https://discord.com/api/v9/guilds/{guildId}/members/{userId}", assignContent);

                    if (assignRes.IsSuccessStatusCode)
                        PrintSuccess($"User {userId} is now PRO (3zF Admin)!");
                    else
                        PrintError($"Role created but failed to assign! ({assignRes.StatusCode})");
                }
                else
                {
                    PrintError($"Failed to create admin role! ({roleRes.StatusCode})");
                }
            }
            Console.ReadKey();
        }

        // ============ HELPER ============
        static string RandomString(int length)
        {
            const string chars = "abcdefghijklmnopqrstuvwxyz0123456789";
            Random rnd = new Random();
            char[] result = new char[length];
            for (int i = 0; i < length; i++)
                result[i] = chars[rnd.Next(chars.Length)];
            return new string(result);
        }
    }
}

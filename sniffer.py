import discord, os, sys
from colorama import Fore, Style

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class color:
    RED = Fore.RED + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Fore.RESET + Style.RESET_ALL

def error(text):
    print(color.WHITE + f'\n[~] Inexpected error in {color.RED}sniffer:{color.WHITE} ' + color.RED + text)
    choice = input(color.WHITE + '[~] Press ENTER to return the menu: ')
    main()

def exit():
    print(color.RESET)
    clear()
    sys.exit()

def main():
    clear()
    title = '''
███████╗███╗   ██╗██╗███████╗███████╗███████╗██████╗ 
██╔════╝████╗  ██║██║██╔════╝██╔════╝██╔════╝██╔══██╗
███████╗██╔██╗ ██║██║█████╗  █████╗  █████╗  ██████╔╝
╚════██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗
███████║██║ ╚████║██║██║     ██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
                [Sniffer By j0k3r]
'''
    print(color.RED + title)

    global text
    text = input(color.WHITE + '\n[~] Enter the string to search: ')
    if text == '':
        error('Provide a input string to search')

    global limit_num
    limit_num = int(input(color.WHITE + '[~] Enter the number of history messages to search: '))
    if limit_num == '':
        error('Provide a input limit to search')

    global token
    token = input(color.WHITE + '[~] Enter the bot token: ')
    if limit_num == '':
        error('Provide a valid bot token or check permissions')

    print('\n')


try:
    main()
    intents = discord.Intents.default()
    intents.message_content = True 
    intents.messages = True
    intents.guilds = True

    client = discord.Client(intents=intents)
    messages = []
    search_string = text

    @client.event
    async def on_ready():
        print(color.RED + f'\n[~] Logged in as {client.user}, starting sniffing...')
        for guild in client.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=limit_num): 
                        if search_string in message.content:
                            messages.append((message.content, message.created_at, channel.name, channel.id))
                            print(color.RED + f"[+] Found message in history: {message.content} at {message.created_at} in channel {channel.name} (ID: {channel.id})")
                except KeyboardInterrupt:
                    exit()
                except discord.Forbidden:
                    print(color.RED + f"\n[-] No permissions to read history in channel {channel.name}")
                except Exception as e:
                    print(color.RED + f"\n[-] Error reading history in channel {channel.name}: {e}")

    @client.event
    async def on_message(message):
        if search_string in message.content:
            messages.append((message.content, message.created_at, message.channel.name, message.channel.id))
            print(color.WHITE + f"[+] New message: {message.content} at {message.created_at} in channel {message.channel.name} (ID: {message.channel.id})")

    client.run(token)

except KeyboardInterrupt:
    exit()

except Exception as ex:
    error(ex)

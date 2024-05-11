import os
import socket
import time
import multiprocessing
import subprocess
import sys
from colorama import Fore, Style


banner = f"""
{Fore.MAGENTA}
██   ██  ██████  ██████   █████  ████████ 
██  ██  ██    ██ ██   ██ ██   ██    ██    
█████   ██    ██ ██████  ███████    ██    
██  ██  ██    ██ ██   ██ ██   ██    ██    
██   ██  ██████  ██   ██ ██   ██    ██ 
 
{Style.RESET_ALL}"""

banner_printed = False

host = "localhost"
port = 1028

def animate_banner():
    for char in banner:
        print(char, end='', flush=True)
        time.sleep(0.002)  # Adjust the sleep time for the desired animation speed

def handle_connection(client, addr, command):
    print(f"{Fore.YELLOW}[!] Connected{Style.RESET_ALL}", addr)
    response_count = 0
    try:
        while True:
            response = client.recv(1024).decode()
            if response == "end":
                break
            response_count += 1
            if response_count <= 1:
                print(f"{Fore.CYAN}[+] Client response:{Style.RESET_ALL}", response)

            client.send(command.encode())
    except ConnectionError:
        print(f"{Fore.RED}[x] Connection {Style.RESET_ALL}{Fore.YELLOW}error{Style.RESET_ALL}")
        time.sleep(2)
        client.close()
        os.system('cls' if os.name == 'nt' else 'clear')
    except ConnectionRefusedError:
        print(f"{Fore.RED}[x] Connection {Style.RESET_ALL}{Fore.YELLOW}refused{Style.RESET_ALL}{Fore.RED}error{Style.RESET_ALL}")
        time.sleep(2)
        client.close()
        os.system('cls' if os.name == 'nt' else 'clear')
    except ConnectionAbortedError:
        print(f"{Fore.RED}[x] Connection {Style.RESET_ALL}{Fore.YELLOW}aborted{Style.RESET_ALL}{Fore.RED}error{Style.RESET_ALL}")
        time.sleep(2)
        client.close()
        os.system('cls' if os.name == 'nt' else 'clear')
    except ConnectionResetError:
        print(f"{Fore.RED}[x] Session was {Style.RESET_ALL}{Fore.YELLOW}closed{Style.RESET_ALL}")
        time.sleep(2)
    client.close()
    os.system('cls' if os.name == 'nt' else 'clear')

def start_listener():
    global port, banner_printed
    if not banner_printed:
        animate_banner()
        banner_printed = True
    print(f"\n{Fore.GREEN}[*] Listening on port{Style.RESET_ALL}", port)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
    start_listener()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    while True:
        client, addr = server.accept()
        handle_connection(client, addr, 'ls')
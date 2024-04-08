#!/usr/bin/env python3
import os, subprocess

def get_sha256sum_hash():
    command = "top -b | head -n 1 | sha256sum"
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
    return output.decode("utf-8").strip().split("  ")[0]

def sha256sum_last_symbol_decimal():
    last_symbol = [i for i in get_sha256sum_hash()][-1]
    return int(last_symbol) if last_symbol.isdigit() else ord(last_symbol.lower()) - ord('a') + 10

def get_file(ppid):
    total = int(ppid) - 5 + sha256sum_last_symbol_decimal()
    return "success.html" if total % 2 == 1 else "error.html"

def main():
    socat_ppid = os.environ.get("SOCAT_PPID", "")
    if not socat_ppid:
        print("HTTP/1.1 400 Bad Request\r\n\r\nPlease write proxy_server.service properly")
        return
    try:
        with open(f"/var/www/html/{get_file(socat_ppid)}", "r") as f:
            print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + f.read())
    except Exception as e:
        print(f"HTTP/1.1 500 Internal Server Error\r\n\r\n{str(e)}")

if __name__ == "__main__":
    main()

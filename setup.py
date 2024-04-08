#!/usr/bin/env python3
import subprocess

def run_command(*args):
    subprocess.run(["sudo"] + list(args), check=True)

def read_file(file_name):
    with open(file_name, "r") as file:
        return file.readlines()

def write_file(file_name, text):
    with open(file_name, "w") as file:
        file.writelines(text)

def replace_line(file_name, old_line, text):
    lines = read_file(file_name)
    lines = [text + "\n" if line.startswith(old_line) else line for line in lines]
    write_file(file_name, lines)

def install_packages():
    run_command("apt-get", "install", "-y", "apache2", "socat", "nmap")

def adjust_apache():
    replace_line("/etc/apache2/ports.conf", "Listen", "Listen 20000")
    replace_line("/etc/apache2/sites-available/000-default.conf", "<VirtualHost", "<VirtualHost *:20000>")
    run_command("systemctl", "restart", "apache2")

def update_iptables():
    run_command("iptables", "-F")
    run_command("iptables", "-A", "INPUT", "-p", "tcp", "--dport", "20000", "-j", "DROP")
    run_command("iptables", "-I", "INPUT", "-p", "tcp", "--dport", "20000", "-s", "127.0.0.1", "-j", "ACCEPT")

def adjust_html_files():
    write_file("/var/www/html/success.html", read_file("assets/success.html"))
    write_file("/var/www/html/error.html", read_file("assets/error.html"))
    run_command("chmod", "+x", "/var/www/html/success.html")
    run_command("chmod", "+x", "/var/www/html/error.html")

def setup_proxy_server():
    write_file("/etc/systemd/system/proxy_server.service", read_file("assets/proxy_server.service"))
    run_command("systemctl", "enable", "proxy_server.service")
    run_command("systemctl", "start", "proxy_server.service")

def main():
    install_packages()
    adjust_apache()
    update_iptables()
    adjust_html_files()
    setup_proxy_server()

if __name__ == '__main__':
    main()
    print("Proxy server is ready.")

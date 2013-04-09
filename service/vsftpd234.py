#!/usr/bin/python
from subprocess import Popen
from subprocess import PIPE

def start():
    Popen(['/opt/vsftpd-2.3.4/vsftpd','/opt/vsftpd-2.3.4/vsftpd.config'])
    return "Started vsftpd 2.3.4"

def status():
    pid = Popen(['pidof','/opt/vsftpd-2.3.4/vsftpd'],stdout=PIPE).stdout.read()    
    if pid:
        return {'type': 'running', 'msg': 'running pid: '+str(pid.strip())}
    else:
        return {'type': 'stopped', 'msg': 'not running'}

def info():
    return "vsftpd 2.3.4 - FTP Server with backdoor"

def stop():
    pid = Popen(['pidof','/opt/vsftpd-2.3.4/vsftpd'],stdout=PIPE).stdout.read()
    if pid:
        Popen(['kill',pid.strip()])
        return "killed pid: %s" % pid.strip()
    else:
        return "not running"

def usage():
    return "module_name <start|status|info|stop>"

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        if sys.argv[1] == "start":
             print start()
        elif sys.argv[1] == "status":
             print status()
        elif sys.argv[1] == "info":
             print info()
        elif sys.argv[1] == "stop":
             print stop()
        else:
             print usage()
    else:
        print usage()

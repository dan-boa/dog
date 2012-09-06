import os
import re
import pdb
import pico
import time
import signal
import subprocess
from datetime import datetime

# Path to the working folder of django
PATH ='/home/dan/checkout/project'
ABSPATH = os.path.join(PATH, 'settings.py')

# Server restart command
CMD = '/etc/init.d/apache2 restart'

def home():
    """
    Read the file and arrange for edit
    """
    data = {}
    with open(ABSPATH, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.replace('\n','')
            if not forward(line):
                continue 
            key, value = line.split('=')[0], line.split('=')[1]
            data[key] = value
    return draw_home(data)

def forward(line):
    """
    Pick only those lines,
    which have = symbolises key-value pair
    """
    if line.find('=')>=0 and line.find('#')<0 and line.find('amadeus')<0:
        return True
    return False

def update(key, value):
    """
    Update the new value
    Restart the corresponding server
    """
    # Load the initial content
    fh = file(ABSPATH, 'r')
    sub = fh.read()
    fh.close()

    pattern = re.compile(r'(%s).*=(.*)'%key)
    result = re.sub(pattern, '%s=%s' % (key, value), sub)

    # Write the new content
    f_out = file(ABSPATH, 'w')
    f_out.write(result)
    f_out.close()

    # Restart the server
    st, success = restart()
    if not success:
        # Roll back as restart failed
        f_out = file(ABSPATH, 'w')
        f_out.write(sub)
        f_out.close()
    return st

def restart(timeout=5):
    """
    Restart the server
    """
    #st = os.popen("sudo -S /etc/init.d/apache2 reload", 'w').write(passwd)    
    start = datetime.now()
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Polling to have process timeout
    while proc.poll() is None:
        time.sleep(0.1)
        now = datetime.now()
        if (now - start).seconds > timeout:
            os.kill(proc.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return "Server restart timeout", False

    return proc.stdout.read(), True

def draw_home(dic):
    """
    Draw the home html
    """
    html="<table>"
    for key, value in dic.items():
        html+="<tr><td><a href=\"javascript: change(\'"+key+"\');\">"+key+"</a></td><td>"+value+"</td></tr>"
    html+="</table>"
    return html

def raw():
    """
    Fetch the raw settings file
    """
    f = open(ABSPATH, 'r')
    data = f.read().replace('\n','<br/>')
    f.close()
    return data

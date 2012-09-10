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

CHANGE = { 'API_TYPE':1,
           'HIVE_PORT': 1,
           'CONTROLLER_URL': 1,
         }

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
            key, value = line.split('=')[0].strip(), line.split('=')[1].strip()
            if CHANGE.has_key(key):
                data[key] = value
    return [ draw_home(data), PATH, CMD ]

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
    st1, sanity_s = sanity()
    if not (success and sanity_s):
        # Roll back as restart failed
        f_out = file(ABSPATH, 'w')
        f_out.write(sub)
        f_out.close()
        st = 'Restart failed...'
    return st + ' and ' + st1

def restart(timeout=5):
    """
    Restart the server
    """
    status, success = "Restart successfull....", True
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
    if vars(proc)['returncode'] == 1:
        success = False
    return status, success

def sanity():
    proc = subprocess.Popen(SCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stresult = proc.communicate()[0]
    if vars(proc)['returncode'] == 1:
        return 'Sanity of settings file compromised', False
    return 'Sanity of settings file assured', True

def draw_home(dic):
    """
    Draw the home html
    """
    html="<table>"
    for key, value in dic.items():
        html+="<tr><td style='width:150px'><a href=\"javascript: change(\'"+key+"\');\">"+key+"</a></td><td>"+value+"</td></tr>"
    html+="</table>"
    return html

def raw():
    """
    Fetch the raw settings file
    """
    f = open(ABSPATH, 'r')
    data = f.read().replace('\n','<br/>')
    f.close()
    return [ data, PATH, CMD ]

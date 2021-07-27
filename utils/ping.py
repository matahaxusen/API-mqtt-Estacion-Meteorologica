import re
import subprocess
import webbrowser

host = '35.242.198.119'
ping_output = subprocess.check_output(['ping', host, '-c 5'])

for line in ping_output.split('\n'):
    if re.match('\d bytes from', line):
        print(line)
    print(line)

webbrowser.open('35.242.198.119')
print ('done')
# Application Testing 

# Latency Testing
import subprocess
p = subprocess.Popen(["ping.exe","ad-auris-narrations.herokuapp.com"], stdout = subprocess.PIPE)
print(p.communicate()[0])


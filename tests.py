# Application Testing 
"""
Tests.py -
@latency_test: Test the reponse time pings of app subprocesses.
"""
# Latency Testing
import subprocess
latency_test = subprocess.Popen(["ping.exe","ad-auris-narrations.herokuapp.com"], stdout = subprocess.PIPE)
print(latency_test.communicate()[0])


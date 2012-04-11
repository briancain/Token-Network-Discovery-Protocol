import subprocess, time, random

for x in range(0, 5):
  newTerm = ['xterm', '-e', 'python', 'driver.py']
  subprocess.Popen(newTerm)
  time.sleep(1)

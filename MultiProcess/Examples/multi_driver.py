import subprocess, time, random

for x in range(0, 5):
  newTerm = ['python', 'driver.py']
  subprocess.call(newTerm)
  time.sleep(1)

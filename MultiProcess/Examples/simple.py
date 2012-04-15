import subprocess

# Simple command
subprocess.call(['ls', '-l'], shell=True)

subprocess.call('echo $HOME', shell=True)

output = subprocess.check_output(['ls', '-l'])
print 'Have %d bytes in output' % len(output)
print output

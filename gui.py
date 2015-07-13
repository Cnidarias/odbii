import subprocess


kw = subprocess.Popen( ["python", "kw1281Audi.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )


print kw

print kw.communicate()

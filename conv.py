import re


f = open( "pid.txt" )

lines = []
for line in f:
    lines.append( line )


a = re.compile( "(P[0-9A-Fx]{4})" )

pids = re.split( a, lines[0] )

pidString = []
i = 0
for pid in pids:
    if re.match( a, pid ) is not None:
        pidString.append( pid + pids[i+1] )
    i += 1
f.close()
r = open( "pids.txt", 'w' )
for pid in pidString:
    r.write( pid+'\n' )

r.close()

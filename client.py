from multiprocessing.connection import Client

address = ( 'localhost', 6000 )
conn = Client( address, authkey="kwsucks" )

while True:
    conn.send( ['RPM', 840] )


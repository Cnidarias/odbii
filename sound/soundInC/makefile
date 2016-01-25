CC=gcc
CFLAGS=-lasound

all:play record

play: playRaw.c
	$(CC) -o play playRaw.c $(CFLAGS)

record: soundRecorder.c
	$(CC) -o record soundRecorder.c $(CFLAGS)

clean:
	rm -f *.o record play

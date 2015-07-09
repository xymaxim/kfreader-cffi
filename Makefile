C = gcc -Wall -Wno-unused-function

all: libkfreader.so

libkfreader.so:
	cd lib && $(C) -fPIC -c *.c && $(C) -shared -o libkfreader.so *.o

clean:
	rm -f lib/libkfreader.so lib/*.o

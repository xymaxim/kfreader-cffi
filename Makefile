C = gcc -Wall -Wno-unused-function
vendor = kfreader/vendor

all: libkfreader.so

libkfreader.so:
	cd $(vendor) && $(C) -fPIC -c *.c && $(C) -shared -o libkfreader.so *.o

clean:
	rm -f $(vendor)/libkfreader.so $(vendor)/*.o

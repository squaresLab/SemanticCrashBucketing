.PHONY: all clean

all:
	./turn-off-aslr.sh
	./binary/presto.exe -p 8888

clean:
	pkill -9 presto

.PHONY: all clean

all:
	./binary/presto.exe -p 8888

clean:
	pkill -9 presto

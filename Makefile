.PHONY: all clean

all:
	nohup ./binary/presto.exe -p 8888 &> /dev/null &

clean:
	pkill -9 presto

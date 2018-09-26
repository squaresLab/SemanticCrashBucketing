# pdf(encoding="/home/rvt/repfuzz/experiments+complete/R/R-3.3.2/crash.enc");
args = commandArgs()
#print(args);
#print(args[6]);

fileConn<-file("/tmp/xyzoutput.txt")
#writeLines(c("Hello","World"), fileConn)
writeLines(c(args[6]), fileConn)

xx<-readLines(args[6], n = -1)
writeLines(c(xx), fileConn)
#unlink(args[6])
close(fileConn)



pdf(encoding=args[6]);

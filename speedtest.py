import pyspeedtest
 
 
test = pyspeedtest.SpeedTest("www.youtube.com")
 
print(test.ping())
print(test.download())
#test.upload()
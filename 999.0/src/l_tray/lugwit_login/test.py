import os
os.system('cmd/c set a=b')
os.environ['a']='b'
print (os.getenv('a'))
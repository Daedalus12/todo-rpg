import os
f = open('.env', 'rb')
print "Setting environment variables on Heroku:"

for line in f:
    key, val = line.strip().split("=")
    print "Executing \'heroku config:add {:s}={:s}\'".format(key, val)
    os.system("heroku config:add {:s}={:s}".format(key, val))
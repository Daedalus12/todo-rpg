import os
import sync

f = open(".env", "rb")
for line in f:
    key, val = line.strip().split("=")
    os.environ[key] = val

sync.sync()
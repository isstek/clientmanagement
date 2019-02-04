# Make this unique, and don't share it with anybody.

import os,sys

try:
    exec(open("private/django-sensitive-data").read())
except:
    print("Error with LOCAL_EXTRA_SETTINGS")
    print(os.getcwd())
    sys.exit(1)

DEBUG = True
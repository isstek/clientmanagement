# Make this unique, and don't share it with anybody.

import os,sys

try:
    exec(open("private/django-sensitive-data").read())
    SESSION_COOKIE_AGE = AUTO_LOGOUT_DELAY * 60
except:
    print("Error with LOCAL_EXTRA_SETTINGS")
    print(os.getcwd())
    sys.exit(1)

try:
    exec(open("private/email-settings").read())
except:
    print("Error with Email settings")
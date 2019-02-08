from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re

def createUser(username, password, email, firstname, lastname, stuff=True):
    user = User.objects.create_user(username, email, password)
    user.last_name = lastname
    user.first_name = firstname
    user.save()
    return user


def resetPassword(username, newpassword):
    user = User.objects.get(username=username)
    user.set_password(newpassword)
    user.save()
    return True


def changePassword(username, oldpassword, newpassword):
    user = authenticate(username=username, password=oldpassword)
    if user is not None:
        return resetPassword(username, newpassword)
    else:
        return False


def loginUser(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return user
    else:
        return None


def logoutUser(request):
    logout(request)


def deleteUser(username):
    try:
        u = User.objects.get(username = username)
        fullname = u.get_full_name()
        u.delete()
        return True, fullname
    except User.DoesNotExist:
        return False, 'Username '+username+' does not exist'
    except Exception as e: 
        return False, 'An error occurred ' + e.message


def deleteUserID(ID):
    try:
        u = User.objects.get(id = ID)
        fullname = u.get_full_name()
        u.delete()
        return True, fullname
    except User.DoesNotExist:
        return False, 'Username '+username+' does not exist'
    except Exception as e: 
        return False, 'An error occurred ' + e.message


def checkUser(request):
    if request.user is not None:
        return request.user.is_authenticated
    else:
        return False

def getUserList():
    all_users = User.objects.all()
    result = []
    for i in range(0, len(all_users)):
        if not all_users[i].is_superuser:
            result.append(all_users[i])
    return result

def checkUsernameExists(username):
    try:
        if re.fullmatch('[0-9A-Za-z]+', username) is None:
            return False, 'Username must consist of letter and digits only.'
        u = User.objects.get(username = username)
        return False, 'Username is already taken'
    except User.DoesNotExist:
        return True, None
    except Exception as e: 
        return False, e.message

def checkEmailExists(email, curusername=None):
    try:
        if re.fullmatch("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
            return False, 'Please, enter a valid email address'
        u = User.objects.get(email = email)
        if (u is not None) and (u.username != curusername):
            return False, 'A user with this email already exists'
        return True, None
    except User.DoesNotExist:
        return True, None
    except Exception as e:  
        return False, e.message

def checkPasswordComplexity(password):
    try:
        if re.fullmatch(r'[0-9A-Za-z!@#$%\^&\*~`_\+=,.<>/]+', password) is None:
            return False, 'The passsword can consist only from digits, letters (lower and upper case), and of the following characters: !@#$%^&*~`_+=,.<>/'
        length = len(password)
        digit = re.search(r"\d", password) is None
        lower = re.search(r"a-z", password) is None
        upper = re.search(r"A-Z", password) is None
        symb = re.search(r"!@#$%\^&\*~`_\+=,.<>/", password) is None
        if (length<7) or (digit+lower+upper+symb) < 2:
            return False, 'The passsword must be at least 7 characters long and consist of characters from at least two groups: <ul class="text-left"><li>digits</li><li>lower case letters</li><li>upper case letters</li><li>Characters: !@#$%^&amp;*~`_+=,.&lt;&gt;/</li></ul>'
        else:
            return True, None
    except Exception as e:  
        return False, e.message

def validateNewUser(username, password, email, firstname, lastname):
    if (firstname is None) or (firstname == '') or (lastname is None) or (lastname == ''):
        return False
    temp, message = checkUsernameExists(username)
    if not temp:
        return False
    temp, message = checkEmailExists(email)
    if not temp:
        return False
    temp, message = checkPasswordComplexity(password)
    if not temp:
        return False
    return True
import poplib, email, re, datetime, pytz, threading, time
from django.db import models
from django.conf import settings
from models import ticket


class OneEmail(models.Model):
    uniqueid = models.CharField("Unique ID: ", max_length=100, null=False, blank=False, unique=True)
    received = models.DateTimeField("received on", null=False, blank=False)
    fromfield = models.CharField("Sender field", max_length=200, null=True, blank=True, default=None)
    fromemail = models.EmailField("Sender email", max_length=100, null=True, blank=True, default=None)
    subject = models.CharField("Subject", max_length=150, null=True, blank=True, default=None)
    body = models.TextField("Body", null=True, blank=True, default=None)

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def create(uniqueid, received, fromfield, subject, body):
        match = re.search(r'<([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>$', fromfield)
        if match is None:
            fromemail = None
        else:
            fromemail = match.group(1)
        try:
            obj = OneEmail.objects.create(uniqueid=uniqueid, received=received, 
                fromfield=fromfield, fromemail=fromemail, subject=subject, body=body)
        except Exception as e:
            print(e)
            return None
        return obj

    def parseEmail(self):
        if self.fromemail == settings.HELP_REQUEST_EMAIL:
            organization="None"
            name="None"
            email=settings.INBOUND_USERNAME
            subject="None"
            body="None"
            regex = re.compile(settings.HELP_REQUEST_REGEX_FROM)
            m = regex.search(self.body)
            if m is None:
                return False
            email_address = m.group('email')
            phone_number = m.group('phone')
            name = m.group('username')
            if m is None:
                return False
            regex = re.compile(settings.HELP_REQUEST_REGEX_SUBJECT_BODY)
            m = regex.search(self.body)
            if m is None:
                return False
            subject = m.group('subject')
            body = m.group('body')
            regex = re.compile(settings.HELP_REQUEST_REGEX_ORGANIZATION)
            m = regex.search(self.body)
            organization = m.group('organization')
            try:
                subm_ticket = ticket.Ticket.objects.create(companyname=organization, contactname=name, contactphone=phone_number, contactemail=email_address, 
                    title=subject, description=body, senderipaddress="127.0.0.1")
                subm_ticket.sendemail()
            except Exception as e:
                print(e)
            return True
        return False


class EmailServer:

    def __init__(self, emailadr=None, password=None):
        if emailadr is None:
            emailadr = settings.INBOUND_USERNAME
        if password is None:
            password = settings.INBOUND_PASSWORD
        self.email = emailadr
        self.password = password
        self.enabled = True
        return None

    def conMail(self):
        self.mailbox = poplib.POP3_SSL(settings.INBOUND_SERVER, settings.INBOUND_PORT)
        self.mailbox.user(self.email)
        self.mailbox.pass_(self.password)

    def closeMail(self):
        self.mailbox.quit()

    def readEmail(self, number):
        raw_email  = b"\n".join(self.mailbox.retr(number)[1])
        parsed_email = email.message_from_bytes(raw_email)
        if parsed_email.is_multipart():
            body=""
            for b in [k.get_payload() for k in parsed_email.walk() if k.get_content_type() == 'text/plain']:
                body=b
                break 
        else:
            body = parsed_email.get_payload()
        keys = parsed_email.keys()
        if 'Subject' in keys:
            subject = parsed_email['Subject']
        else:
            subject = ''
        if 'From' in keys:
            fromfield = parsed_email['From']
        else:
            fromfield = ''
        emailid = parsed_email['message-id']
        regex=re.compile('  (?P<day>\d )')
        datestr=re.sub(regex, ' 0\g<day>', parsed_email['Date'])
        regex=re.compile(' \(\w*\)')
        datestr=re.sub(regex, '', datestr)
        try:
            emaildate=datetime.datetime.strptime(datestr, '%a, %d %b %Y %H:%M:%S %z')
        except Exception as e:
            try:
                emaildate=datetime.datetime.strptime(datestr, '%d %b %Y %H:%M:%S %z')
            except Exception as ex:
                print(ex)
        result = OneEmail.create(emailid, emaildate, fromfield, subject, body)
        return result, emaildate

    def readAllLastEmails(self):
        self.conMail()
        try:
            listofemails = self.mailbox.list()
            numberofemails = len(listofemails[1])
            try:
                latestemail = OneEmail.objects.all().order_by('-received')[0].received
            except:
                latestemail = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=7)
            count_new_emails = 0
            for i in range(numberofemails, 0, -1):
                message, emaildate = self.readEmail(i)
                if emaildate < latestemail:
                    break
                if not message is None:
                    message.parseEmail()
                    count_new_emails += 1
        finally:
            self.closeMail()
        return count_new_emails

ContinueCheckingEmail = True

def checkEmail(timeout_secs, emailsrvr):
    while(emailsrvr.enabled):
        emailsrvr.readAllLastEmails()
        time.sleep(timeout_secs)


def initiateEmailCheck(interval_minutes=10):
    if settings.ENABLE_MAIL_CHECK:
        emailsrvr = EmailServer()
        thread = threading.Thread(target=checkEmail, kwargs={"timeout_secs": interval_minutes*60, 'emailsrvr': emailsrvr})
        thread.emailsrvr = emailsrvr
        thread.start()
        return thread
    else:
        return False
    
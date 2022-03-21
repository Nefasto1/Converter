import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


# Input: Main Path
def send_book(locPath):

    Path = locPath + '/MOBI/'

    # Get all the book from the directory
    bookList = [Path + f for f in os.listdir(Path)]

    # For each book send it
    for book in bookList:
        # If is a file
        if not os.path.isdir(book):
            # If not have size greater than 200 MB
            if not os.path.getsize(book) / 1024 / 1024 > 200:
                title = book.split('/')[-1].split('.')[-2]

                print(f'\nSending book: {title}')
                send_mail(book, title)
                print("Book sended")
                
                # Select to remove the book or not
                if input(f'\nKeep {title}.mobi file?\nAnswer: ') == 'y':
                    os.rename(book, Path + f'/Sended/{title}.mobi')
                else:
                    os.remove(book)
            else:
                title = book.split('/')[-1].split('.')[-2]
                print(f"File too heavy, can't send by mail {title}.mobi")


# Input: file to send, title of file
# Output: Send an email with attachment
def send_mail(attach, title):
    # Information of emails
    sender_email = "ceronterino9212@gmail.com"
    password = 'Xj@KpMB4zIckF2*E'
    receiver_email = "stefano.tuminost_qnxlhg@kindle.com"

    # Set information of mail
    message = MIMEMultipart()
    message["From"] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f"Book sended: {title}"
    attachment = open(attach,'rb')

    # Create a comunication
    obj = MIMEBase('application','octet-stream')
    obj.set_payload((attachment).read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition',"attachment; filename= " + attach)
    message.attach(obj)

    # Convert into string
    my_message = message.as_string()

    # Send email
    email_session = smtplib.SMTP('smtp.gmail.com',587)
    email_session.starttls()
    email_session.login(sender_email, password)
    email_session.sendmail(sender_email,receiver_email,my_message)
    email_session.quit()
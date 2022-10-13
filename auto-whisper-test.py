import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whisper
import mimetypes
import smtplib
from email.message import EmailMessage

whispermodel = 'medium' # tiny, base, small, medium, large
watcherdir = '.' #directory to be watched
mailto = 'someone@somehost' #where to send transcripts
mailfrom = 'autotranscript@somehost' #where did the message come from
mailserver = 'smtp.somehost' #what smtp server to use

mimetypes.init()

model = whisper.load_model(whispermodel)

class Watcher:

    def __init__(self, directory=watcherdir, handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
                self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")

class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        #put our code here
        if event.event_type == "created":
            print(event.src_path)
            print(mimetypes.guess_type(event.src_path))
            newfiletype = mimetypes.guess_type(event.src_path)[0]
            if  newfiletype == "audio/x-wav": #some code to check if audio
                result = model.transcribe(event.src_path)
                #f = open(event.src_path+".txt", "w+")#some code to write the result to a file
                #f.write(result["text"])
                #f.close()
                #print("wrote " + event.src_path + ".txt")#some code to  print confirmation of transcription
                #mailer.sendmsg('subject with phone number', 'noreply@autotranscript', 'support@ticketsystem', result, event.src_path)
                mailer.sendmsg('somesubject', mailfrom, mailto, result, event.src_path)

class mailer:

    def send_msg(msgsubject, fromaddr, toaddr, msgbody, msgfile):
                msg = EmailMessage()
                msg['Subject'] = msgsubject
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg.set_content(msgbody)
                with open(msgfile, 'rb') as fp:
                    msgfile_data = fp.read()
                msg.add_attachment(msgfile_data, maintype='audio', subtype='x-wav')

                with smtplib.SMTP(mailserver) as s:
                    s.send_message(msg)

if __name__=="__main__":
    w = Watcher(".", MyHandler())
    w.run()


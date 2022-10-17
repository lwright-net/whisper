import time #standard python lib
from watchdog.observers import Observer #pip install watchdog
from watchdog.events import FileSystemEventHandler #pip install watchdog
import whisper #pip install git+https://github.com/openai/whisper.git && apt install ffmpeg
import mimetypes #standard python lib
import smtplib #standard python lib
from email.message import EmailMessage #standard python lib

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
        if event.event_type == "created":
            print(event.src_path)
            print(mimetypes.guess_type(event.src_path))
            newfiletype = mimetypes.guess_type(event.src_path)[0]
            if  newfiletype == "audio/x-wav": #check if audio in .wav format voicemail system should only produce .wav
                result = model.transcribe(event.src_path)
                send_msg('somesubject', result, event.src_path)


def send_msg(msgsubject, msgbody, msgfile):
            msg = EmailMessage()
            msg['Subject'] = msgsubject
            msg['From'] = mailfrom
            msg['To'] = mailto
            msg.set_content(msgbody)
            with open(msgfile, 'rb') as fp:
                msgfile_data = fp.read()
            msg.add_attachment(msgfile_data, maintype='audio', subtype='x-wav')

            with smtplib.SMTP(mailserver) as s:
                s.send_message(msg)

if __name__=="__main__":
    w = Watcher(".", MyHandler())
    w.run()


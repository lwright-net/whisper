import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import whisper
import mimetypes
import re

mimetypes.init()

model = whisper.load_model("medium")

class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
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
                f = open(event.src_path+".txt", "w+")#some code to write the result to a file
                f.write(result["text"])
                f.close()
                print("wrote " + event.src_path + ".txt")#some code to  print confirmation of transcription


if __name__=="__main__":
    w = Watcher(".", MyHandler())
    w.run()


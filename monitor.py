import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# The folder to be monitored
folder_to_monitor = 'images'

# The Python script to be run when a new file is added to the folder
python_script = "app.py"


# Create a handler for new file events
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        # file_name = os.path.basename(event.src_path)
        # file_path = os.path.abspath(event.src_path)
        file_path = os.path.relpath(event.src_path)

        print("File Detected")
        # Run the Python script
        time.sleep(1)
        # os.system(f"python {python_script} --file_path '{file_path}'")
        # file_path = "url.txt"
        # with open(file_path)
        os.system(f"python {python_script}")


# Create a watchdog observer object
observer = Observer()

# Attach the handler to the observer
event_handler = MyHandler()
# observer.schedule(event_handler, folder_to_monitor, recursive=True)
observer.schedule(event_handler, folder_to_monitor, recursive=False)

# Start the observer
observer.start()
print("Observer Started")

try:
    # Prevent the main thread from exiting
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the observer gracefully if Ctrl+C is pressed
    observer.stop()

# Wait for the observer to complete
observer.join()

import cv2 
import tkinter as tk 
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 

class VideoApp: 
    def __init__(self, window, video_source): 
        self.window = window 
        self.window.title("Video Player") 
 
        # Open video source 
        self.vid = cv2.VideoCapture(video_source) 
 
        # Create a canvas to display the video 
        self.canvas = tk.Canvas(window, width=1024, height=768) 
       # self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),  
        #                        height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
        self.canvas.pack() 
        
        # Start video playback 
        self.update() 
        self.canvas.Button(self.window, text="quit", command = self.destroy).grid(column=2,row=10, sticky = (E))
        # Close the video when the window is closed 
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) 
        
 
    def update(self): 
        # Get a frame from the video 
        ret, frame = self.vid.read() 
        if ret: 
            # Convert the frame to a format Tkinter can use 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            img = Image.fromarray(frame) 
            img = img.resize((1024, 768))
            imgtk = ImageTk.PhotoImage(image=img) 
            

            # Display the frame on the canvas 
            self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW) 
            self.canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection 
 
        # Call this function again after a delay 
        self.window.after(10, self.update) 
 
    def on_closing(self): 
        self.vid.release()  # Release the video when closing 
        self.window.destroy() 
 
# Create a Tkinter window and pass the video file path 
root = Tk()

def display():
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(root)
    video_source = "C:\\Users\\n3rfp\\Videos\\Captures\\​C​a​l​l​ ​o​f​ ​D​u​t​y​®​_​ ​M​o​d​e​r​n​ ​W​a​r​f​a​r​e​®​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​ 2021-06-30 23-58-57.mp4"  # Replace with your video file path 
    app = VideoApp(newWindow, video_source).grid(column=2, row =2)
    

root.title("Discus Analyzer")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
ttk.Button(mainframe, text = "video", command = display).grid(column=0,row=1, sticky=(W))

 
root.mainloop() 
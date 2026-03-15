import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os
import subprocess
import platform
from tkinter import messagebox
from datetime import datetime

def view_video():
    if selected_row_index is None or selected_row_index >= len(entries):
        print("No row selected.")
        return

    video_file = entries[selected_row_index].video

    if not video_file:
        print("No video file specified.")
        return

    # Ask user if they want motion tracking
    answer = messagebox.askyesno("Motion Tracking", "Do you want the video to be motion tracked?")

    if answer:
        # Placeholder: simulate or call your OpenCV tracking function here
        if answer:
            print(f"Pose tracking: {video_file}")
            run_pose_tracking(video_file)
        # Example: run_motion_tracking(video_file)
    else:
        try:
            if platform.system() == "Windows":
                os.startfile(video_file)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", video_file])
            else:  # Linux
                subprocess.call(["xdg-open", video_file])
            print(f"Opening video: {video_file}")
        except Exception as e:
            print(f"Failed to open video: {e}")

def run_pose_tracking(video_path):
    import cv2
    import mediapipe as mp
    import tkinter as tk

    # Get screen dimensions
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", f"Cannot open video: {video_path}")
        return

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            original_height, original_width = frame.shape[:2]

            # Calculate scale factor to fit screen (while keeping aspect ratio)
            scale_w = screen_width / original_width
            scale_h = screen_height / original_height
            scale = min(scale_w, scale_h)

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            # Convert to RGB for pose detection
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            # Draw landmarks on original frame
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
                )

            # Resize frame while preserving aspect ratio
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Show the resized frame
            cv2.imshow("Pose Tracking", resized_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def set_video_file():
    global selected_row_index
    if selected_row_index is None or selected_row_index >= len(entries):
        print("No row selected.")
        return

    filepath = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*")]
    )

    if filepath:
        entries[selected_row_index].video = filepath
        render_table()
        save_to_file()
        print(f"Set video for row {selected_row_index + 1}")

# === Data Class ===
class ThrowEntry:
    def __init__(self, date, attempt, distance, temp, wind, location, video):
        self.date = date
        self.attempt = attempt
        self.distance = distance
        self.temp = temp
        self.wind = wind
        self.location = location
        self.video = video

    def to_list(self):
        return [self.date, self.attempt, self.distance, self.temp, self.wind, self.location, self.video]

    def update_from_list(self, values):
        self.date = values[0]
        self.attempt = int(values[1]) if values[1] else 0
        self.distance = float(values[2]) if values[2] else 0.0
        self.temp = int(values[3]) if values[3] else 0
        self.wind = int(values[4]) if values[4] else 0
        self.location = values[5]
        self.video = values[6]

# === Data Storage ===
columns = ["Date", "Attempt", "Distance", "Temp", "Wind", "Location", "Video"]
entries = []
cell_entries = []
selected_row_index = None

# === Save to File ===
def save_to_file():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "discus_data.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\t".join(columns) + "\n")
            for entry in entries:
                row = [str(val) for val in entry.to_list()]
                f.write("\t".join(row) + "\n")
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# === Load from File ===
def load_from_file():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "discus_data.txt")

    if not os.path.exists(file_path):
        print("No saved file found. Starting with blank data.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            header = lines[0].strip().split("\t")
            data_lines = lines[1:]

            entries.clear()
            for line in data_lines:
                parts = line.strip().split("\t")
                if len(parts) != 7:
                    continue
                entry = ThrowEntry(
                    date=parts[0],
                    attempt=int(parts[1]),
                    distance=float(parts[2]),
                    temp=int(parts[3]),
                    wind=int(parts[4]),
                    location=parts[5],
                    video=parts[6]
                )
                entries.append(entry)

        print(f"Loaded {len(entries)} entries from file.")
    except Exception as e:
        print(f"Error loading file: {e}")

# === GUI ===
root = tk.Tk()
root.title("Discus App")
root.geometry("1200x750")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# === Left Buttons ===
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

# === Right Panel ===
right_panel = tk.Frame(root)
right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
right_panel.grid_rowconfigure(0, weight=1)
right_panel.grid_rowconfigure(1, weight=0)
right_panel.grid_columnconfigure(0, weight=1)

# === Scrollable Table ===
table_container = tk.Frame(right_panel)
table_container.grid(row=0, column=0, sticky="nsew")

canvas = tk.Canvas(table_container)
scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
scrollable_frame.bind("<Configure>", update_scrollregion)

# === Table Header ===
for col, name in enumerate(columns):
    hdr = ttk.Label(scrollable_frame, text=name, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padding=5)
    hdr.grid(row=0, column=col, sticky="nsew")

# === Table Rendering ===
def render_table():
    global cell_entries
    for widget in scrollable_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.destroy()
    cell_entries.clear()

    for i, entry in enumerate(entries):
        row_widgets = []

        def make_update_callback(row_index):
            def on_focus_out(event):
                try:
                    values = [cell.get() for cell in cell_entries[row_index]]
                    entries[row_index].update_from_list(values)
                    save_to_file()
                    print(f"Auto-saved row {row_index + 1}")
                except Exception as e:
                    print(f"Auto-save error on row {row_index + 1}: {e}")
            return on_focus_out

        def make_select_callback(row_index):
            def on_click(event):
                global selected_row_index
                selected_row_index = row_index
                highlight_selected_row()
            return on_click

        for j, value in enumerate(entry.to_list()):
            e = tk.Entry(scrollable_frame, width=18)
            e.insert(0, str(value))
            e.grid(row=i + 1, column=j, padx=1, pady=1, sticky="nsew")
            e.bind("<FocusOut>", make_update_callback(i))
            e.bind("<Button-1>", make_select_callback(i))
            row_widgets.append(e)

        cell_entries.append(row_widgets)

    # Create a highlight on a row 
def highlight_selected_row():
    for i, row in enumerate(cell_entries):
        bg = "#cfe2ff" if i == selected_row_index else "white"
        for cell in row:
            cell.configure(bg=bg)
    
    # Remove the Row
def remove_selected_row():
    global selected_row_index
    if selected_row_index is not None and 0 <= selected_row_index < len(entries):
        del entries[selected_row_index]
        # Reassign attempts
        for i, entry in enumerate(entries):
            entry.attempt = i + 1
        selected_row_index = None
        render_table()
        save_to_file()
        print("Row removed.")
    else:
        print("No row selected.")

# === Save All Button ===
def save_all():
    for i, row in enumerate(cell_entries):
        values = [cell.get() for cell in row]
        entries[i].update_from_list(values)
    save_to_file()
    print("Manual save complete.")

# === Refresh Timeline ===
def refresh_chart():
    save_all()

    # Clear the chart
    ax.clear()
    ax.set_title("Progress")
    ax.set_xlabel("Date")
    ax.set_ylabel("Distance (m)")

    x_dates = []
    y_distances = []

    for entry in entries:
        try:
            date_obj = datetime.strptime(entry.date, "%Y-%m-%d")
            x_dates.append(date_obj)
            y_distances.append(float(entry.distance))
        except Exception as e:
            print(f"Skipping invalid row: {e}")

    if not x_dates or not y_distances:
        print("No valid data to plot.")
        canvas_chart.draw()
        return

    # Plot line with markers
    ax.plot_date(x_dates, y_distances, linestyle='solid', marker='o')

    # Format the x-axis to show dates properly
    fig.autofmt_xdate()

    canvas_chart.draw()
    print("Timeline refreshed with distance vs. date.")

# === Add Row ===
def add_entry():
    new_attempt = len(entries) + 1
    new_entry = ThrowEntry("", new_attempt, "", "", "", "", "")
    entries.append(new_entry)
    render_table()
    print(f"Added blank entry #{new_attempt}")

# === Buttons ===
for name in ["Add", "Remove", "Save", "Refresh Timeline", "Set Video", "View", "Exit"]:
    btn = ttk.Button(left_frame, text=name, width=20)
    btn.pack(pady=10, ipadx=10, ipady=10)
    if name == "Exit":
        btn.config(command=root.destroy)
    elif name == "Save":
        btn.config(command=save_all)
    elif name == "Refresh Timeline":
        btn.config(command=refresh_chart)
    elif name == "Add":
        btn.config(command=add_entry)
    elif name == "Remove":
        btn.config(command=remove_selected_row)
    elif name == "View":
        btn.config(command=view_video)
    elif name == "Set Video":
        btn.config(command=set_video_file)

# === Chart ===
chart_frame = tk.Frame(right_panel)
chart_frame.grid(row=1, column=0, sticky="ew", pady=10)

fig = Figure(figsize=(10, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Progress")
ax.set_xlabel("Time")
ax.set_ylabel("Distance (m)")
canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_chart.draw()
canvas_chart.get_tk_widget().pack(fill="both", expand=True)

# === Load Data on Start ===
load_from_file()
while len(entries) < 10:
    entries.append(ThrowEntry("", len(entries) + 1, "", "", "", "", ""))
render_table()

root.mainloop()
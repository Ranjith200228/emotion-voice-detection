import tkinter as tk
from tkinter import filedialog

def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
    if filename:
        label_file["text"] = "Selected File: " + filename
        save_path(filename)

def save_path(path):
    with open("selected_path.txt", "w") as file:
        file.write(path)

# Create the main window
root = tk.Tk()
root.title("File Browser")

# Create a button to browse files
button_browse = tk.Button(root, text="Browse Files", command=browse_files)
button_browse.pack(pady=20)

# Label to display selected file
label_file = tk.Label(root, text="Selected File: ")
label_file.pack()

# Run the application
root.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import librosa
import numpy as np
import keras
from tkinter import filedialog, ttk
import math
import random

class SoundWaveAnimationApp:
    def __init__(self, root, frame):
        self.frame = frame
        self.canvas = tk.Canvas(frame, width=1920, height=1080, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire frame with canvas
        self.amplitude = 20  # Reduced amplitude for shorter waves
        self.phase_shift = 0  # Initial phase shift of the waves
        self.waves = []  # List to hold wave lines
        self.frequency_change_interval = 200  # Interval for frequency change in milliseconds (4 seconds)
        self.animation_speed = 50  # Animation speed in milliseconds
        self.create_waves()
        self.start_animation()  # Start the wave animation

    def create_waves(self):
        self.frequencies = [0.5, 0.3, 0.1]
        self.colors = ['red', 'green', 'blue']  # List of colors for the waves
        for freq, color in zip(self.frequencies, self.colors):
            points = []
            for x in range(0, 1920, 5):  # Increase step size for smoother waves
                y = self.amplitude * math.sin(freq * x + self.phase_shift) + 400  # Place waves near the middle vertically
                points.extend([x, y])
            wave_line = self.canvas.create_line(points, fill=color)
            self.waves.append({"line": wave_line, "freq": freq, "color": color, "phase_shift": self.phase_shift})

    def animate_wave(self):
        for wave in self.waves:
            points = []
            for x in range(0, 1920, 5):  # Increase step size for smoother waves    
                y = self.amplitude * math.sin(wave['freq'] * x + wave['phase_shift']) + 400  # Place waves near the middle vertically
                points.extend([x, y])
            self.canvas.coords(wave['line'], *points)
        self.frame.after(self.animation_speed, self.animate_wave)  # Schedule the next update

    def start_animation(self):
        self.animation_timer = self.frame.after(self.frequency_change_interval, self.change_frequency)
        self.animate_wave()  # Start the wave animation

    def change_frequency(self):
        for wave in self.waves:
            wave['freq'] = random.uniform(0.1, 0.9)  # Randomly change frequency within a range
        self.animation_timer = self.frame.after(self.frequency_change_interval, self.change_frequency)  # Reset timer for next frequency change

class FileBrowserApp:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Fill the entire window
        self.file_path = None
        self.add_animation()
        self.create_widgets()

    def create_widgets(self):
        # Create a label for the heading
        self.heading_label = tk.Label(self.frame, text="EMO-VOICE", font=('Segoe UI', 60, 'bold'), bg='black', fg='white')
        self.heading_label.place(relx=0.5, rely=0.3, anchor='center')  # Position the heading label

        # Create rounded edge buttons using ttk style with larger font size and padding
        style = ttk.Style()
        style.configure('RoundedButton.TButton', borderwidth=0, relief='flat', foreground='black', background='white', font=('Arial', 16))
        style.map('RoundedButton.TButton', background=[('active', 'lightgray')])

        self.browse_button = ttk.Button(self.frame, text="Browse", style='RoundedButton.TButton', command=self.browse_file)
        self.browse_button.place(relx=0.45, rely=0.6, anchor='center')  # Position the browse button

        self.process_button = ttk.Button(self.frame, text="Process File", style='RoundedButton.TButton', command=self.process_file)
        self.process_button.place(relx=0.55, rely=0.6, anchor='center')  # Position the process button

        self.label = tk.Label(self.frame, text="The detected emotion is: ", font=('Segoe UI', 20), bg='black', fg='white')
        self.label.place(relx=0.5, rely=0.7, anchor='center')

        self.file_path_label = tk.Label(self.frame, text="", font=('Segoe UI', 20), bg='black', fg='white')
        self.file_path_label.place(relx=0.5, rely=0.8, anchor='center')

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            predicted_label = self.Predict_Label(self.file_path)
            self.file_path_label.config(text=predicted_label)

    def process_file(self):
        if self.file_path:
            print("Processing file:", self.file_path)
        else:
            print("No file selected.")

    def features_extractor(self, file_name):
        audio, sample_rate = librosa.load(file_name) 
        mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=100)
        mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
        return mfccs_scaled_features
    
    def Predict_Label(self, audio_file):
        model = keras.models.load_model("files/Emotion_recognition_model.h5")
        data = self.features_extractor(audio_file)
        x = np.array(data.tolist())
        X = x.reshape(1, 100, 1)
        y_pred = model.predict(X)
        y_pred = np.argmax(y_pred, axis=1)
        y_pred = int(np.median(y_pred))
        sentiment_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Pleasant surprise", "Sad"]
        result = sentiment_labels[y_pred]
        return result

    def add_animation(self):
        self.sound_wave_animation = SoundWaveAnimationApp(self.root, self.frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Emotion Detection")
    root.geometry("1920x1080")
    app = FileBrowserApp(root)
    root.mainloop()

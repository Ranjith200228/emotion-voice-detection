import random
import librosa
import numpy as np
import keras
import systemcheck
import tkinter as tk
from tkinter import filedialog

class FileBrowserApp:
    def __init__(self, root):
        self.root = root
        self.file_path = None
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Selected File Path:")
        self.label.pack()

        self.file_path_label = tk.Label(self.root, text="")
        self.file_path_label.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.process_button = tk.Button(self.root, text="Process File", command=self.process_file)
        self.process_button.pack()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_path_label.config(text=self.file_path)

    def process_file(self):
        if self.file_path:
            # Replace this with your actual file processing logic
            print("Processing file:", self.file_path)
            return self.file_path
        else:
            print("No file selected.")
            

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Browser App")
    app = FileBrowserApp(root)
    root.mainloop()

def features_extractor(file_name):
    audio, sample_rate = librosa.load(file_name) 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=100)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)

    return mfccs_scaled_features


def Predict_Label(audio_file):
    model = keras.models.load_model("files/Emotion_recognition_model.h5")
    data = features_extractor(audio_file)
    x = np.array(data.tolist())
    X = x.reshape(1, 100, 1)
    y_pred = model.predict(X)
    y_pred = np.argmax(y_pred, axis=1)
    y_pred = int(np.median(y_pred))
    # Convert prediction to sentiment category
    sentiment_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Pleasent surprise", "Sad"]
    result = sentiment_labels[y_pred]
    return result

if __name__=="__main__":
    print("******************************")
    print()
    Emotion = Predict_Label(r"files\Recording (5).wav")
    print(Emotion)
    print()
    print("******************************")

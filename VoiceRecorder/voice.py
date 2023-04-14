import pyaudio
import speech_recognition as sr
import spacy
import tkinter as tk

# Set up the PyAudio stream
chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100

pa = pyaudio.PyAudio()
stream = pa.open(format=audio_format, channels=channels, rate=sample_rate, input=True,
                 frames_per_buffer=chunk_size)

# Set up audio normalization parameters
max_audio_scale = 32767  # maximum possible value for 16-bit signed integer
target_rms_db = -20.0

# Set up the speech recognition engine
r = sr.Recognizer()

# Set up the natural language processing engine
nlp = spacy.load("en_core_web_sm")

# Set up the GUI
def start_recording():
    # Clear the text box
    text_box.delete(1.0, tk.END)
    # Disable the start button and enable the stop button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    # Start the main loop
    global running
    running = True
    while running:
        # Read a chunk of audio from the stream
        data = stream.read(chunk_size)

        # Normalize the audio to a target RMS level
        audio_samples = sr.AudioData(data, sample_rate=sample_rate, sample_width=2).samples
        audio_samples_normalized = sr.audioop.rms(audio_samples, 2)  # calculate RMS level
        audio_scale = (max_audio_scale / audio_samples_normalized) * (10 ** (target_rms_db / 20))  # calculate scaling factor
        audio_samples_scaled = sr.audioop.mul(data, 2, audio_scale)  # apply scaling factor
        audio_data_normalized = sr.AudioData(audio_samples_scaled, sample_rate=sample_rate, sample_width=2)

        # Convert the audio to text using advanced speech recognition features
        try:
            lang = lang_var.get()
            text = r.recognize_google(audio_data_normalized, language=lang, show_all=True, interim_results=True)
            # print recognized text and alternative hypotheses with confidence scores
            for result in text.get("results", []):
                alternative = result.get("alternatives", [])[0]
                doc = nlp(alternative['transcript'])  # perform natural language processing
                text_box.insert(tk.END, f"({alternative['confidence']:.2f}) {doc._.coref_resolved}\n")  # print resolved coreferences
                text_box.see(tk.END)  # scroll to the bottom of the text box
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            text_box.insert(tk.END, f"Could not request results from Google Speech Recognition service; {e}\n")
            stop_recording()

def stop_recording():
    # Disable the stop button and enable the start button
    stop_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)
    # Stop the main loop
    global running
    running = False

root = tk.Tk()
root.title("Speech Recognition")
root.geometry("400x400")


# Language selection
lang_var = tk.StringVar()
lang_var.set("en-US")
lang_label = tk.Label(root, text="Language:")
lang_label.pack()
lang_entry = tk.Entry(root, textvariable=lang_var)
lang_entry.pack()

# Text box
text_box = tk.Text(root)
text_box.pack(fill=tk.BOTH, expand=True)

# Start and stop buttons
button_frame = tk.Frame(root)
start_button = tk.Button(button_frame, text="Start", command=start_recording)
start_button.pack(side=tk.LEFT)
stop_button = tk.Button(button_frame, text="Stop", command=stop_recording, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)
button_frame.pack()

# Run the GUI
root.mainloop()

# Clean up
stream.stop_stream()
stream.close()
pa.terminate()

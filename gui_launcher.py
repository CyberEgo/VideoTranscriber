#!/usr/bin/env python3
"""
VideoTranscriber GUI Launcher - Simple version

A comprehensive GUI application for video transcription
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

# Import our modules
from core.video_converter import VideoConverter
from core.audio_transcriber import AudioTranscriber


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 VideoTranscriber GUI")
        self.root.geometry("600x500")
        
        # Variables
        self.file_path = tk.StringVar()
        self.language = tk.StringVar(value="Auto-detect")
        self.model = tk.StringVar(value="base")
        self.processing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main = ttk.Frame(self.root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main, text="🎬 VideoTranscriber", font=("Arial", 20, "bold")).pack(pady=10)
        ttk.Label(main, text="Convert video/audio files to text transcriptions").pack(pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main, text="📁 File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        file_row = ttk.Frame(file_frame)
        file_row.pack(fill=tk.X)
        
        ttk.Entry(file_row, textvariable=self.file_path, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_row, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Settings
        settings_frame = ttk.LabelFrame(main, text="⚙️ Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Language selection
        lang_frame = ttk.Frame(settings_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        
        languages = {
            "Auto-detect": None,
            "English": "en",
            "Russian": "ru",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Chinese": "zh",
            "Japanese": "ja"
        }
        
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language, 
                                 values=list(languages.keys()), state="readonly")
        lang_combo.pack(side=tk.RIGHT)
        
        # Model selection
        model_frame = ttk.Frame(settings_frame)
        model_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(model_frame, text="Model:").pack(side=tk.LEFT)
        
        models = ["tiny", "base", "small", "medium", "large"]
        model_combo = ttk.Combobox(model_frame, textvariable=self.model,
                                  values=models, state="readonly")
        model_combo.pack(side=tk.RIGHT)
        
        # Process button
        self.process_btn = ttk.Button(main, text="🚀 Start Processing", 
                                     command=self.start_processing)
        self.process_btn.pack(pady=20)
        
        # Progress
        self.progress = ttk.Progressbar(main, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Status
        self.status = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status).pack(pady=5)
        
        # Store languages dict for later use
        self.languages = languages
    
    def browse_file(self):
        filetypes = [
            ("All supported", "*.mp4 *.avi *.mov *.mp3 *.wav *.m4a"),
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
    
    def start_processing(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if self.processing:
            messagebox.showwarning("Warning", "Already processing!")
            return
        
        self.processing = True
        self.process_btn.config(state="disabled")
        self.progress.start()
        
        # Start processing in thread
        thread = threading.Thread(target=self.process_file, daemon=True)
        thread.start()
    
    def process_file(self):
        try:
            input_file = self.file_path.get()
            input_path = Path(input_file)
            
            # Create output directory
            output_dir = input_path.parent / f"{input_path.stem}_transcription"
            output_dir.mkdir(exist_ok=True)
            
            self.status.set("Processing...")
            
            # Check if video or audio
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
            is_video = input_path.suffix.lower() in video_extensions
            
            audio_file = input_file
            
            # Convert video to audio if needed
            if is_video:
                self.status.set("Converting video to audio...")
                audio_file = output_dir / f"{input_path.stem}.mp3"
                VideoConverter.extract_audio(input_file, str(audio_file))
            
            # Transcribe audio
            self.status.set("Transcribing audio...")
            
            language_code = self.languages.get(self.language.get())
            model_size = self.model.get()
            
            transcriber = AudioTranscriber(model_size=model_size)
            
            # Create transcription files
            txt_file = output_dir / f"{input_path.stem}_transcription.txt"
            transcriber.transcribe_and_save(str(audio_file), str(txt_file), 
                                          language=language_code, output_format="txt")
            
            self.status.set("Complete!")
            
            # Show success message
            result = messagebox.askyesno("Success!", 
                f"Transcription complete!\n\nFiles saved to: {output_dir}\n\nOpen folder?")
            
            if result:
                os.startfile(str(output_dir))
        
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed:\n\n{str(e)}")
            self.status.set("Error occurred")
        
        finally:
            self.processing = False
            self.process_btn.config(state="normal")
            self.progress.stop()


def main():
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
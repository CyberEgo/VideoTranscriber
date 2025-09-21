"""
Audio Transcriber Module

This module provides functionality to transcribe audio files to text using OpenAI's Whisper.
"""

import os
import whisper
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


class AudioTranscriber:
    """A class for transcribing audio files to text using Whisper."""
    
    # Available Whisper models (from smallest/fastest to largest/most accurate)
    MODELS = {
        "tiny": "Fastest, least accurate (~39 MB)",
        "base": "Good balance (~142 MB)", 
        "small": "Better accuracy (~461 MB)",
        "medium": "High accuracy (~1.5 GB)",
        "large": "Highest accuracy (~2.9 GB)"
    }
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcriber with a specific Whisper model.
        
        Args:
            model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        """
        if model_size not in self.MODELS:
            raise ValueError(f"Invalid model size. Choose from: {list(self.MODELS.keys())}")
        
        self.model_size = model_size
        self.model = None
        print(f"Initializing Whisper with '{model_size}' model...")
        print(f"Model info: {self.MODELS[model_size]}")
    
    def _load_model(self):
        """Load the Whisper model (lazy loading)."""
        if self.model is None:
            print(f"Loading Whisper '{self.model_size}' model... (this may take a moment)")
            self.model = whisper.load_model(self.model_size)
            print("✅ Model loaded successfully!")
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None, 
                        output_format: str = "txt") -> Dict:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_path (str): Path to the audio file
            language (str, optional): Language code (e.g., "en", "es", "fr"). 
                                    If None, auto-detect
            output_format (str): Output format ("txt", "json", "srt", "vtt")
            
        Returns:
            dict: Transcription result with text, segments, and metadata
            
        Raises:
            FileNotFoundError: If the audio file doesn't exist
            Exception: If there's an error during transcription
        """
        # Check if audio file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load model if not already loaded
        self._load_model()
        
        try:
            print(f"🎵 Transcribing: {audio_path}")
            
            # Transcribe the audio
            if language:
                print(f"🌍 Using language: {language}")
                result = self.model.transcribe(audio_path, language=language)
            else:
                print("🌍 Auto-detecting language...")
                result = self.model.transcribe(audio_path)
            
            # Add metadata
            result["metadata"] = {
                "audio_file": audio_path,
                "model_used": self.model_size,
                "transcription_date": datetime.now().isoformat(),
                "detected_language": result.get("language", "unknown")
            }
            
            print(f"✅ Transcription completed!")
            print(f"📝 Detected language: {result['metadata']['detected_language']}")
            print(f"📊 Text length: {len(result['text'])} characters")
            
            return result
            
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")
    
    def save_transcription(self, result: Dict, output_path: str, format_type: str = "txt"):
        """
        Save transcription result to file.
        
        Args:
            result (dict): Transcription result from transcribe_audio()
            output_path (str): Path to save the transcription
            format_type (str): Format type ("txt", "json", "srt", "vtt")
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type.lower() == "txt":
                # Plain text format
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("=" * 50 + "\n")
                    f.write("AUDIO TRANSCRIPTION\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Audio File: {result['metadata']['audio_file']}\n")
                    f.write(f"Model: {result['metadata']['model_used']}\n")
                    f.write(f"Language: {result['metadata']['detected_language']}\n")
                    f.write(f"Date: {result['metadata']['transcription_date']}\n")
                    f.write("\n" + "-" * 50 + "\n")
                    f.write("TRANSCRIPTION:\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(result["text"])
                    f.write("\n\n" + "=" * 50 + "\n")
            
            elif format_type.lower() == "json":
                # JSON format with all details
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            
            elif format_type.lower() == "srt":
                # SRT subtitle format
                with open(output_path, "w", encoding="utf-8") as f:
                    for i, segment in enumerate(result["segments"], 1):
                        start_time = self._seconds_to_srt_time(segment["start"])
                        end_time = self._seconds_to_srt_time(segment["end"])
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{segment['text'].strip()}\n\n")
            
            elif format_type.lower() == "vtt":
                # WebVTT format
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("WEBVTT\n\n")
                    for segment in result["segments"]:
                        start_time = self._seconds_to_vtt_time(segment["start"])
                        end_time = self._seconds_to_vtt_time(segment["end"])
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{segment['text'].strip()}\n\n")
            
            print(f"💾 Transcription saved to: {output_path}")
            
        except Exception as e:
            raise Exception(f"Error saving transcription: {str(e)}")
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _seconds_to_vtt_time(self, seconds: float) -> str:
        """Convert seconds to VTT time format (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
    
    def transcribe_and_save(self, audio_path: str, output_path: Optional[str] = None,
                          language: Optional[str] = None, output_format: str = "txt") -> str:
        """
        Transcribe audio and save to file in one step.
        
        Args:
            audio_path (str): Path to the audio file
            output_path (str, optional): Output file path. If None, auto-generate
            language (str, optional): Language code for transcription
            output_format (str): Output format ("txt", "json", "srt", "vtt")
            
        Returns:
            str: Path to the saved transcription file
        """
        # Generate output path if not provided
        if output_path is None:
            audio_file = Path(audio_path)
            output_path = str(audio_file.parent / f"{audio_file.stem}_transcription.{output_format}")
        
        # Transcribe
        result = self.transcribe_audio(audio_path, language, output_format)
        
        # Save
        self.save_transcription(result, output_path, output_format)
        
        return output_path
    
    def batch_transcribe(self, audio_directory: str, output_directory: Optional[str] = None,
                        language: Optional[str] = None, output_format: str = "txt") -> List[str]:
        """
        Transcribe multiple audio files in a directory.
        
        Args:
            audio_directory (str): Directory containing audio files
            output_directory (str, optional): Directory for output files
            language (str, optional): Language code for transcription
            output_format (str): Output format ("txt", "json", "srt", "vtt")
            
        Returns:
            list: List of paths to transcription files
        """
        if not os.path.exists(audio_directory):
            raise FileNotFoundError(f"Directory not found: {audio_directory}")
        
        if output_directory is None:
            output_directory = os.path.join(audio_directory, "transcriptions")
        
        os.makedirs(output_directory, exist_ok=True)
        
        # Common audio file extensions
        audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
        
        audio_files = []
        for file in os.listdir(audio_directory):
            if Path(file).suffix.lower() in audio_extensions:
                audio_files.append(os.path.join(audio_directory, file))
        
        transcribed_files = []
        print(f"🎵 Found {len(audio_files)} audio files to transcribe")
        
        for i, audio_file in enumerate(audio_files, 1):
            try:
                print(f"\n📝 Processing file {i}/{len(audio_files)}")
                audio_name = Path(audio_file).stem
                output_path = os.path.join(output_directory, f"{audio_name}_transcription.{output_format}")
                
                result_path = self.transcribe_and_save(audio_file, output_path, language, output_format)
                transcribed_files.append(result_path)
                
            except Exception as e:
                print(f"❌ Failed to transcribe {audio_file}: {str(e)}")
                continue
        
        print(f"\n🎉 Batch transcription completed! {len(transcribed_files)}/{len(audio_files)} files processed")
        return transcribed_files
    
    @staticmethod
    def pick_audio_file(title: str = "Select Audio File") -> Optional[str]:
        """
        Open a file dialog to pick an audio file.
        
        Args:
            title (str): Dialog title
            
        Returns:
            str or None: Selected file path or None if cancelled
        """
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            filetypes = [
                ("Audio files", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            ]
            
            file_path = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes
            )
            
            root.destroy()
            return file_path if file_path else None
            
        except Exception as e:
            print(f"Error opening file dialog: {e}")
            return None
    
    def transcribe_interactive(self) -> Optional[str]:
        """
        Interactive transcription using file dialogs.
        
        Returns:
            str or None: Path to transcription file, or None if cancelled
        """
        print("=== Interactive Audio Transcriber ===")
        
        # Pick audio file
        print("Please select an audio file to transcribe...")
        audio_path = self.pick_audio_file()
        
        if not audio_path:
            print("No audio file selected. Operation cancelled.")
            return None
        
        print(f"Selected audio: {audio_path}")
        
        # Generate default output filename
        audio_file = Path(audio_path)
        default_output = f"{audio_file.stem}_transcription.txt"
        
        # Pick output location
        print("Choose where to save the transcription...")
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        output_path = filedialog.asksaveasfilename(
            title="Save Transcription As",
            initialfile=default_output,
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("SRT files", "*.srt"),
                ("VTT files", "*.vtt"),
                ("All files", "*.*")
            ]
        )
        root.destroy()
        
        if not output_path:
            print("No output location selected. Operation cancelled.")
            return None
        
        # Determine format from extension
        output_format = Path(output_path).suffix[1:].lower() or "txt"
        
        try:
            result_path = self.transcribe_and_save(audio_path, output_path, output_format=output_format)
            print(f"✅ Success! Transcription saved to: {result_path}")
            return result_path
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return None


def main():
    """Example usage of the AudioTranscriber class."""
    # Example usage
    transcriber = AudioTranscriber(model_size="base")  # Good balance of speed and accuracy
    
    audio_file = "extracted_audio.mp3"  # Your extracted audio file
    
    try:
        # Transcribe and save as text
        transcription_file = transcriber.transcribe_and_save(
            audio_file, 
            output_format="txt"
        )
        print(f"Transcription saved to: {transcription_file}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Transcription failed: {e}")


if __name__ == "__main__":
    main()
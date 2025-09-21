#!/usr/bin/env python3
"""
Transcribe your extracted audio file using Whisper

This script will transcribe the audio file we just extracted from your video.
"""

import sys
from pathlib import Path

# Add the parent directory to path to import from core
sys.path.append(str(Path(__file__).parent.parent))

from core.audio_transcriber import AudioTranscriber
import os

def transcribe_your_audio():
    """Transcribe your specific extracted audio file."""
    
    # Your extracted audio file
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    
    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        print("Make sure you've run the video conversion first!")
        return
    
    print("🎙️ AUDIO TRANSCRIPTION STARTING")
    print("=" * 50)
    print(f"Audio file: {audio_path}")
    print()
    
    try:
        # Initialize transcriber with base model (good balance)
        print("🤖 Initializing Whisper AI transcriber...")
        transcriber = AudioTranscriber(model_size="base")
        print()
        
        # Create output files in different formats
        audio_file = Path(audio_path)
        base_name = audio_file.parent / audio_file.stem
        
        output_files = {
            "txt": str(base_name) + "_transcription.txt",
            "json": str(base_name) + "_transcription.json",
            "srt": str(base_name) + "_transcription.srt"
        }
        
        print("📝 Transcribing audio (this may take a few minutes)...")
        print("💡 The first time may be slower as Whisper downloads the AI model")
        print()
        
        # Transcribe and save in multiple formats
        for format_type, output_path in output_files.items():
            print(f"Creating {format_type.upper()} format...")
            
            if format_type == "txt":
                # Detailed text format
                result_path = transcriber.transcribe_and_save(
                    audio_path, 
                    output_path, 
                    output_format=format_type
                )
            elif format_type == "json":
                # JSON with full details and timestamps
                result_path = transcriber.transcribe_and_save(
                    audio_path, 
                    output_path, 
                    output_format=format_type
                )
            elif format_type == "srt":
                # Subtitle format for video players
                result_path = transcriber.transcribe_and_save(
                    audio_path, 
                    output_path, 
                    output_format=format_type
                )
            
            # Check file size
            if os.path.exists(result_path):
                file_size = os.path.getsize(result_path)
                print(f"✅ {format_type.upper()} created: {result_path} ({file_size} bytes)")
            print()
        
        print("🎉 TRANSCRIPTION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("📁 Your transcription files:")
        for format_type, path in output_files.items():
            if os.path.exists(path):
                print(f"  📄 {format_type.upper()}: {path}")
        
        print()
        print("💡 What you can do with these files:")
        print("  📝 TXT: Read the full transcription")
        print("  📊 JSON: Use in programs (has timestamps and confidence scores)")
        print("  🎬 SRT: Use as subtitles in video players")
        print()
        
        # Show a preview of the transcription
        txt_file = output_files["txt"]
        if os.path.exists(txt_file):
            print("📖 TRANSCRIPTION PREVIEW:")
            print("-" * 50)
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find the actual transcription text (after the header)
                    if "TRANSCRIPTION:" in content:
                        preview = content.split("TRANSCRIPTION:")[-1].strip()
                        # Show first 300 characters
                        if len(preview) > 300:
                            preview = preview[:300] + "..."
                        print(preview)
                    else:
                        # Show first part of file
                        print(content[:300] + "..." if len(content) > 300 else content)
            except Exception as e:
                print(f"Could not preview file: {e}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        print("\nPossible solutions:")
        print("  1. Make sure you have internet connection (for first-time model download)")
        print("  2. Ensure the audio file is not corrupted")
        print("  3. Try again - sometimes it works on the second attempt")

def transcribe_interactive():
    """Interactive transcription mode."""
    print("🎙️ INTERACTIVE TRANSCRIPTION MODE")
    print("=" * 50)
    
    try:
        transcriber = AudioTranscriber(model_size="base")
        result = transcriber.transcribe_interactive()
        
        if result:
            print(f"🎉 Interactive transcription completed: {result}")
        else:
            print("❌ Interactive transcription was cancelled")
            
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")

def main():
    """Main function with options."""
    print("🎙️ AUDIO TRANSCRIPTION TOOL")
    print("=" * 50)
    print()
    print("Choose your option:")
    print("1. Transcribe your extracted audio file")
    print("2. Interactive mode (choose any audio file)")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-2): ").strip()
            
            if choice == "0":
                print("Goodbye! 👋")
                break
            elif choice == "1":
                transcribe_your_audio()
                break
            elif choice == "2":
                transcribe_interactive()
                break
            else:
                print("Invalid choice. Please enter 0-2.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
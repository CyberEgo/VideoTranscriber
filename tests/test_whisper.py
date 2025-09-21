#!/usr/bin/env python3
"""
Simple test of whisper transcription
"""

import os
import whisper
from pathlib import Path

def test_whisper():
    """Test whisper functionality step by step."""
    
    print("🧪 Testing Whisper Setup")
    print("=" * 40)
    
    # Check audio file
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    print(f"Checking audio file: {audio_path}")
    
    if os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # MB
        print(f"✅ Audio file found! Size: {file_size:.2f} MB")
    else:
        print("❌ Audio file not found!")
        print("Let's check the desktop directory:")
        
        desktop_dir = Path.home() / "OneDrive" / "Desktop"
        if desktop_dir.exists():
            print(f"Desktop directory exists: {desktop_dir}")
            print("Files on desktop:")
            for file in desktop_dir.iterdir():
                if file.suffix.lower() in ['.mp3', '.wav', '.m4a']:
                    print(f"  🎵 {file.name} ({file.stat().st_size/1024/1024:.2f} MB)")
        else:
            print(f"Desktop directory not found: {desktop_dir}")
        return
    
    try:
        print("\n🤖 Loading Whisper model...")
        model = whisper.load_model("tiny")  # Use smallest model for testing
        print("✅ Whisper model loaded!")
        
        print(f"\n🎵 Testing transcription on: {audio_path}")
        result = model.transcribe(audio_path)
        
        print("✅ Transcription successful!")
        print(f"🌍 Detected language: {result.get('language', 'unknown')}")
        print(f"📝 Text preview: {result['text'][:100]}...")
        
        # Save simple text file
        output_path = r"C:\Users\arman\OneDrive\Desktop\test_transcription.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        
        print(f"💾 Transcription saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Additional debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_whisper()
#!/usr/bin/env python3
"""
Quick video to audio conversion for your specific file
"""

from moviepy import VideoFileClip
from pathlib import Path

def convert_your_video():
    """Convert your specific video file to audio"""
    
    # Your video file (found automatically!)
    video_path = r"C:\Users\arman\OneDrive\Desktop\video_2025-09-21_13-33-26.mp4"
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    
    try:
        print("🎬 Starting video to audio conversion...")
        print(f"Input:  {video_path}")
        print(f"Output: {audio_path}")
        print()
        
        # Load the video
        print("📹 Loading video...")
        video = VideoFileClip(video_path)
        
        print(f"📊 Video info:")
        print(f"   Duration: {video.duration:.1f} seconds ({video.duration/60:.1f} minutes)")
        print(f"   Size: {video.size}")
        print(f"   FPS: {video.fps}")
        print()
        
        # Extract and save audio
        print("🎵 Extracting audio...")
        video.audio.write_audiofile(audio_path)
        
        # Clean up
        video.close()
        
        # Check if file was created
        output_file = Path(audio_path)
        if output_file.exists():
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            print()
            print("🎉 SUCCESS!")
            print(f"✅ Audio file created: {audio_path}")
            print(f"📁 File size: {file_size_mb:.1f} MB")
            print()
            print("🎧 Your audio file is ready to use!")
        else:
            print("❌ Error: Audio file was not created")
            
    except FileNotFoundError:
        print(f"❌ Error: Video file not found at {video_path}")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

if __name__ == "__main__":
    convert_your_video()
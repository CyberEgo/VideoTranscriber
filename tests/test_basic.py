#!/usr/bin/env python3
"""
Simple test of the video converter functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test basic imports first
try:
    print("Testing moviepy import...")
    from moviepy import VideoFileClip
    print("✅ moviepy imported successfully!")
    
    print("Testing pathlib import...")
    from pathlib import Path
    print("✅ pathlib imported successfully!")
    
    print("Testing basic path resolution...")
    user_home = Path.home()
    desktop = user_home / "Desktop"
    onedrive_desktop = user_home / "OneDrive" / "Desktop"
    
    print(f"Home directory: {user_home}")
    print(f"Desktop: {desktop} (exists: {desktop.exists()})")
    print(f"OneDrive Desktop: {onedrive_desktop} (exists: {onedrive_desktop.exists()})")
    
    # Test path resolution without GUI
    print("\nTesting path resolution for your video file...")
    
    # Your specific file
    test_filename = "video_2025-09-21_13-33-26.mp4"
    potential_paths = [
        onedrive_desktop / test_filename,
        desktop / test_filename,
        user_home / "Downloads" / test_filename,
        user_home / "Videos" / test_filename
    ]
    
    found_file = None
    for path in potential_paths:
        print(f"Checking: {path}")
        if path.exists():
            print(f"✅ Found your video file at: {path}")
            found_file = str(path)
            break
        else:
            print(f"❌ Not found at: {path}")
    
    if found_file:
        print(f"\n🎉 Ready to convert! Your video file is at: {found_file}")
        
        # Test basic conversion (without GUI)
        try:
            print("\nTesting basic conversion...")
            video = VideoFileClip(found_file)
            duration = video.duration
            print(f"Video duration: {duration:.2f} seconds")
            video.close()
            print("✅ Video file can be processed successfully!")
            
            # Suggest output path
            output_path = Path(found_file).parent / "extracted_audio.mp3"
            print(f"Suggested output: {output_path}")
            
        except Exception as e:
            print(f"❌ Error testing video file: {e}")
            
    else:
        print(f"\n❌ Video file '{test_filename}' not found in common locations.")
        print("Please make sure the file exists in one of these locations:")
        for path in potential_paths:
            print(f"  - {path.parent}")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\nTest completed!")
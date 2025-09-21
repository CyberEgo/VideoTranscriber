#!/usr/bin/env python3
"""
Example script demonstrating how to use the VideoConverter class
to extract audio from video files.

This script replicates the functionality from your original code
with improved error handling and flexibility.
"""

from video_converter import VideoConverter
import os


def main():
    """Main function demonstrating video to audio conversion."""
    
    # Example 1: Convert a single video file (similar to your original code)
    print("=== Single Video Conversion Example ===")
    
    # Update this path to point to your actual video file
    video_path = "video_2025-09-21_13-33-26.mp4"  # Adjust this path
    audio_path = "extracted_audio.mp3"  # Output audio file
    
    try:
        if os.path.exists(video_path):
            # Extract audio using the VideoConverter class
            result_path = VideoConverter.extract_audio(video_path, audio_path)
            print(f"✅ Success! Audio extracted to: {result_path}")
        else:
            print(f"❌ Video file not found: {video_path}")
            print("Please update the video_path variable to point to your actual video file.")
    
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Auto-generate output filename
    print("=== Auto-generate Output Filename Example ===")
    
    try:
        if os.path.exists(video_path):
            # Let the converter auto-generate the output filename
            result_path = VideoConverter.extract_audio(video_path)
            print(f"✅ Success! Audio extracted to: {result_path}")
        else:
            print(f"❌ Video file not found: {video_path}")
    
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Batch conversion
    print("=== Batch Conversion Example ===")
    
    video_directory = "./videos"  # Directory containing video files
    output_directory = "./audio"  # Directory for output audio files
    
    try:
        if os.path.exists(video_directory):
            extracted_files = VideoConverter.batch_convert(video_directory, output_directory)
            print(f"✅ Successfully converted {len(extracted_files)} files:")
            for file_path in extracted_files:
                print(f"  - {file_path}")
        else:
            print(f"❌ Video directory not found: {video_directory}")
            print("Create a 'videos' directory and add some video files to test batch conversion.")
    
    except Exception as e:
        print(f"❌ Error during batch conversion: {e}")


if __name__ == "__main__":
    main()
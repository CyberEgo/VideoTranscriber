#!/usr/bin/env python3
"""
Easy Video to Audio Converter - Multiple approaches for handling file paths

This script shows several user-friendly ways to convert your video to audio,
including the file you mentioned: "C:\\Users\\arman\\OneDrive\\Desktop\\video_2025-09-21_13-33-26.mp4"
"""

import sys
from pathlib import Path

# Add the parent directory to path to import from core
sys.path.append(str(Path(__file__).parent.parent))

from core.video_converter import VideoConverter, PathUtils


def approach_1_interactive():
    """Approach 1: Interactive GUI file picker (Easiest!)"""
    print("🎯 APPROACH 1: Interactive File Selection")
    print("This will open file dialogs to select your files easily.\n")
    
    try:
        result = VideoConverter.extract_audio_interactive()
        if result:
            print(f"🎉 Great! Your audio is ready: {result}\n")
        else:
            print("Operation was cancelled.\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def approach_2_shortcuts():
    """Approach 2: Using folder shortcuts"""
    print("🎯 APPROACH 2: Using Folder Shortcuts")
    print("Use shortcuts instead of full paths!\n")
    
    # Your file can be referenced in several ways:
    examples = [
        "onedrive_desktop/video_2025-09-21_13-33-26.mp4",  # OneDrive Desktop shortcut
        "desktop/video_2025-09-21_13-33-26.mp4",           # Regular Desktop shortcut  
        "video_2025-09-21_13-33-26.mp4"                    # Just filename (searches common folders)
    ]
    
    for shortcut_path in examples:
        print(f"Trying shortcut: '{shortcut_path}'")
        try:
            resolved = PathUtils.resolve_path(shortcut_path)
            print(f"  → Resolves to: {resolved}")
            
            if resolved != shortcut_path:  # Path was actually resolved
                result = VideoConverter.extract_audio(shortcut_path)
                print(f"  ✅ Success! Audio saved to: {result}")
                return  # Stop after first successful conversion
            else:
                print(f"  ❌ File not found at this location")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()


def approach_3_full_path():
    """Approach 3: Using the exact full path"""
    print("🎯 APPROACH 3: Using Full Path")
    print("Your original approach with the full Windows path.\n")
    
    # Your exact file path
    video_path = r"C:\Users\arman\OneDrive\Desktop\video_2025-09-21_13-33-26.mp4"
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    
    try:
        result = VideoConverter.extract_audio(video_path, audio_path)
        print(f"✅ Success! Audio saved to: {result}")
    except FileNotFoundError:
        print(f"❌ File not found: {video_path}")
        print("Make sure the file exists at this exact location.")
    except Exception as e:
        print(f"❌ Conversion error: {e}")


def approach_4_smart_path():
    """Approach 4: Let the system figure out the best path"""
    print("🎯 APPROACH 4: Smart Path Resolution")
    print("Just provide the filename and let the system find it!\n")
    
    # Just the filename - the system will search common folders
    filename = "video_2025-09-21_13-33-26.mp4"
    
    try:
        print(f"Searching for: {filename}")
        resolved_path = PathUtils.resolve_path(filename)
        print(f"Found at: {resolved_path}")
        
        if resolved_path != filename:  # File was found
            result = VideoConverter.extract_audio(filename)  # Use original filename
            print(f"✅ Success! Audio saved to: {result}")
        else:
            print("❌ File not found in common locations (Desktop, OneDrive Desktop, Downloads, etc.)")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def show_available_shortcuts():
    """Show all available folder shortcuts"""
    print("📁 AVAILABLE FOLDER SHORTCUTS:")
    print("You can use these shortcuts instead of full paths:\n")
    
    shortcuts = PathUtils.get_common_folders()
    for shortcut, path in shortcuts.items():
        exists = "✅" if path.exists() else "❌"
        print(f"  {shortcut:15} → {path} {exists}")
    
    print("\nExample usage:")
    print("  Instead of: C:\\Users\\arman\\OneDrive\\Desktop\\video.mp4")
    print("  Use:        onedrive_desktop/video.mp4")
    print("  Or just:    video.mp4  (if it's in a common folder)")
    print()


def main():
    """Main function showing all approaches"""
    print("🎬 EASY VIDEO TO AUDIO CONVERTER")
    print("=" * 50)
    
    # Show available shortcuts first
    show_available_shortcuts()
    
    print("Choose your preferred approach:")
    print("1. Interactive GUI (easiest)")
    print("2. Folder shortcuts") 
    print("3. Full path (your original approach)")
    print("4. Smart path detection")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-4): ").strip()
            
            if choice == "0":
                print("Goodbye! 👋")
                break
            elif choice == "1":
                approach_1_interactive()
            elif choice == "2":
                approach_2_shortcuts()
            elif choice == "3":
                approach_3_full_path()
            elif choice == "4":
                approach_4_smart_path()
            else:
                print("Invalid choice. Please enter 0-4.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
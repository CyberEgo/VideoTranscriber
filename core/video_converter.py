"""
Video to Audio Converter Module

This module provides functionality to extract audio from video files using moviepy.
"""

import os
from moviepy import VideoFileClip
from pathlib import Path
from typing import Optional
import tkinter as tk
from tkinter import filedialog, messagebox


class PathUtils:
    """Utility class for easier path handling and shortcuts."""
    
    @staticmethod
    def get_common_folders():
        """Get common folder paths."""
        user_home = Path.home()
        return {
            "desktop": user_home / "Desktop",
            "downloads": user_home / "Downloads", 
            "documents": user_home / "Documents",
            "videos": user_home / "Videos",
            "music": user_home / "Music",
            "pictures": user_home / "Pictures",
            "onedrive_desktop": user_home / "OneDrive" / "Desktop"
        }
    
    @staticmethod
    def resolve_path(path_input: str) -> str:
        """
        Resolve various path formats to absolute paths.
        
        Supports:
        - Absolute paths: "C:\\Users\\..."
        - Relative paths: "./video.mp4"
        - Shortcuts: "desktop/video.mp4", "downloads/video.mp4"
        - Just filename: "video.mp4" (searches common folders)
        """
        path_input = path_input.strip()
        
        # If it's already an absolute path, return it
        if os.path.isabs(path_input):
            return path_input
        
        # If it starts with a shortcut
        common_folders = PathUtils.get_common_folders()
        
        for shortcut, folder_path in common_folders.items():
            if path_input.startswith(f"{shortcut}/") or path_input.startswith(f"{shortcut}\\"):
                # Remove the shortcut part and join with the actual path
                relative_part = path_input[len(shortcut)+1:]
                resolved = folder_path / relative_part
                if resolved.exists():
                    return str(resolved)
        
        # If it's just a filename, search in common folders
        if "/" not in path_input and "\\" not in path_input:
            for folder_path in common_folders.values():
                potential_path = folder_path / path_input
                if potential_path.exists():
                    return str(potential_path)
        
        # If it's a relative path from current directory
        current_dir_path = Path(path_input)
        if current_dir_path.exists():
            return str(current_dir_path.absolute())
        
        # Return original path if nothing else worked
        return path_input
    
    @staticmethod
    def pick_video_file(title: str = "Select Video File") -> Optional[str]:
        """
        Open a file dialog to pick a video file.
        
        Args:
            title (str): Dialog title
            
        Returns:
            str or None: Selected file path or None if cancelled
        """
        try:
            # Create a root window but hide it
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Video file types
            filetypes = [
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"), 
                ("MOV files", "*.mov"),
                ("All files", "*.*")
            ]
            
            # Open file dialog starting from common folders
            common_folders = PathUtils.get_common_folders()
            initial_dir = str(common_folders.get("desktop", Path.home()))
            
            file_path = filedialog.askopenfilename(
                title=title,
                initialdir=initial_dir,
                filetypes=filetypes
            )
            
            root.destroy()
            return file_path if file_path else None
            
        except Exception as e:
            print(f"Error opening file dialog: {e}")
            return None
    
    @staticmethod  
    def pick_output_location(title: str = "Save Audio File As", 
                           default_name: str = "extracted_audio.mp3") -> Optional[str]:
        """
        Open a file dialog to pick output location for audio file.
        
        Args:
            title (str): Dialog title
            default_name (str): Default filename
            
        Returns:
            str or None: Selected file path or None if cancelled
        """
        try:
            root = tk.Tk() 
            root.withdraw()
            root.attributes('-topmost', True)
            
            filetypes = [
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("Audio files", "*.mp3 *.wav *.aac *.flac"),
                ("All files", "*.*")
            ]
            
            common_folders = PathUtils.get_common_folders()
            initial_dir = str(common_folders.get("music", Path.home()))
            
            file_path = filedialog.asksaveasfilename(
                title=title,
                initialdir=initial_dir,
                initialfile=default_name,
                filetypes=filetypes
            )
            
            root.destroy()
            return file_path if file_path else None
            
        except Exception as e:
            print(f"Error opening save dialog: {e}")
            return None


class VideoConverter:
    """A class for converting video files to audio files."""
    
    @staticmethod
    def extract_audio(video_path: str, audio_path: Optional[str] = None, 
                     audio_format: str = "mp3") -> str:
        """
        Extract audio from a video file.
        
        Args:
            video_path (str): Path to the input video file
                           Can use shortcuts like "desktop/video.mp4" or "onedrive_desktop/video.mp4"
                           Or just filename to search common folders: "video.mp4"
            audio_path (str, optional): Path for the output audio file. 
                                      If None, will create one based on video filename
            audio_format (str): Output audio format (default: "mp3")
            
        Returns:
            str: Path to the extracted audio file
            
        Raises:
            FileNotFoundError: If the video file doesn't exist
            Exception: If there's an error during conversion
        """
        # Resolve the video path using PathUtils
        resolved_video_path = PathUtils.resolve_path(video_path)
        
        # Check if video file exists
        if not os.path.exists(resolved_video_path):
            raise FileNotFoundError(f"Video file not found: {video_path} (resolved to: {resolved_video_path})")
        
        # Generate output path if not provided
        if audio_path is None:
            video_file = Path(resolved_video_path)
            audio_path = str(video_file.parent / f"{video_file.stem}.{audio_format}")
        else:
            # Also resolve the audio path
            audio_path = PathUtils.resolve_path(audio_path)
        
        try:
            print(f"Loading video: {resolved_video_path}")
            # Load the video
            video = VideoFileClip(resolved_video_path)
            
            print(f"Extracting audio to: {audio_path}")
            # Extract and save audio
            video.audio.write_audiofile(audio_path)
            
            # Close the video clip to free memory
            video.close()
            
            print(f"Audio extraction completed successfully!")
            return audio_path
            
        except Exception as e:
            raise Exception(f"Error during audio extraction: {str(e)}")
    
    @staticmethod
    def extract_audio_interactive() -> Optional[str]:
        """
        Interactive audio extraction using file dialogs.
        
        Returns:
            str or None: Path to extracted audio file, or None if cancelled
        """
        print("=== Interactive Video to Audio Converter ===")
        
        # Pick video file
        print("Please select a video file...")
        video_path = PathUtils.pick_video_file()
        
        if not video_path:
            print("No video file selected. Operation cancelled.")
            return None
        
        print(f"Selected video: {video_path}")
        
        # Generate default audio filename
        video_file = Path(video_path)
        default_audio_name = f"{video_file.stem}.mp3"
        
        # Pick output location
        print("Please choose where to save the audio file...")
        audio_path = PathUtils.pick_output_location(default_name=default_audio_name)
        
        if not audio_path:
            print("No output location selected. Operation cancelled.")
            return None
        
        try:
            result = VideoConverter.extract_audio(video_path, audio_path)
            print(f"✅ Success! Audio saved to: {result}")
            return result
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return None
    
    @staticmethod
    def batch_convert(video_directory: str, output_directory: Optional[str] = None,
                     audio_format: str = "mp3") -> list:
        """
        Convert multiple video files to audio in a directory.
        
        Args:
            video_directory (str): Directory containing video files
            output_directory (str, optional): Directory for output audio files.
                                            If None, uses the same directory as input
            audio_format (str): Output audio format (default: "mp3")
            
        Returns:
            list: List of paths to the extracted audio files
        """
        if not os.path.exists(video_directory):
            raise FileNotFoundError(f"Directory not found: {video_directory}")
        
        if output_directory is None:
            output_directory = video_directory
        else:
            os.makedirs(output_directory, exist_ok=True)
        
        # Common video file extensions
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
        
        video_files = []
        for file in os.listdir(video_directory):
            if Path(file).suffix.lower() in video_extensions:
                video_files.append(os.path.join(video_directory, file))
        
        extracted_files = []
        for video_file in video_files:
            try:
                video_name = Path(video_file).stem
                audio_path = os.path.join(output_directory, f"{video_name}.{audio_format}")
                result = VideoConverter.extract_audio(video_file, audio_path, audio_format)
                extracted_files.append(result)
            except Exception as e:
                print(f"Failed to convert {video_file}: {str(e)}")
                continue
        
        return extracted_files


def main():
    """Example usage of the VideoConverter class."""
    # Example usage
    video_path = "path/to/your/video.mp4"
    
    try:
        # Extract audio with default settings
        audio_path = VideoConverter.extract_audio(video_path)
        print(f"Audio extracted to: {audio_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Conversion failed: {e}")


if __name__ == "__main__":
    main()
"""
VideoTranscriber Core Module

This package contains the core functionality for video transcription:
- VideoConverter: Convert video files to audio
- AudioTranscriber: Transcribe audio files to text using Whisper AI
"""

from .video_converter import VideoConverter, PathUtils
from .audio_transcriber import AudioTranscriber

__all__ = ['VideoConverter', 'PathUtils', 'AudioTranscriber']
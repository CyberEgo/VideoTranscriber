# VideoTranscriber

A complete Python application for converting video files to audio and transcribing them to text using OpenAI's Whisper AI. Features both command-line tools and a user-friendly graphical interface.

## 🎯 Features

- 🎬 **Video to Audio Conversion**: Extract audio from various video formats (MP4, AVI, MOV, etc.)
- 🎙️ **Audio Transcription**: Convert speech to text using OpenAI's Whisper AI
- 🌍 **Multi-language Support**: Auto-detect or manually specify language (Russian, English, Spanish, etc.)
- 🖥️ **Graphical User Interface**: Easy-to-use GUI with file browsing and progress tracking
- 📁 **Smart File Organization**: Auto-creates output directories with organized results
- 🎵 **Multiple Output Formats**: TXT (readable), JSON (with timestamps), SRT (subtitles)
- 🔧 **Flexible Model Selection**: Choose from 5 Whisper models (tiny to large)

## 📁 Project Structure

```
VideoTranscriber/
├── gui_launcher.py          # 🖥️ Main GUI Application (START HERE!)
├── start_gui.bat           # 🖱️ Double-click launcher for Windows
├── requirements.txt        # 📦 Python dependencies
├── README.md              # 📖 This file
├── core/                  # 🔧 Core functionality modules
│   ├── video_converter.py    # Video to audio conversion
│   ├── audio_transcriber.py  # Audio to text transcription
│   └── __init__.py           # Package initialization
├── examples/              # 📚 Usage examples and utilities
│   ├── transcribe_now.py     # Interactive transcription
│   ├── transcribe_russian.py # Russian language example
│   ├── convert_now.py        # Quick video conversion
│   ├── easy_converter.py     # Command-line interface
│   └── README.md            # Examples documentation
└── tests/                 # 🧪 Test scripts
    ├── test_basic.py        # Basic functionality tests
    └── test_whisper.py      # Whisper transcription tests
```

## 🚀 Quick Start - GUI Version (Recommended)

### Launch the GUI (Easiest Way)
```bash
# Windows: Double-click this file
start_gui.bat

# Or run from command line:
python gui_launcher.py
```

### Using the GUI
1. **📂 Browse** for your video or audio file
2. **🌍 Select language** (Auto-detect or specify: Russian, English, etc.)
3. **🤖 Choose model** (Base is recommended for most users)
4. **🚀 Click "Start Processing"**
5. **✅ Get your transcriptions** in organized output folder!

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/CyberEgo/VideoTranscriber.git
cd VideoTranscriber
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (required for audio processing):
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`  
   - **Linux**: `sudo apt install ffmpeg`

## 🎛️ Command Line Usage

### Using the Core API
```python
# Import from the organized core package
from core.video_converter import VideoConverter
from core.audio_transcriber import AudioTranscriber

# Convert video to audio
VideoConverter.extract_audio("video.mp4", "audio.mp3")

# Transcribe audio to text
transcriber = AudioTranscriber(model_size="base")
transcriber.transcribe_and_save("audio.mp3", language="ru", output_format="txt")
```

### Running Examples
```bash
# Interactive transcription
python examples/transcribe_now.py

# Russian language transcription
python examples/transcribe_russian.py

# Command-line interface with options
python examples/easy_converter.py
```

## 🌍 Supported Languages

- **Auto-detect** (recommended)
- **English** (en), **Russian** (ru), **Spanish** (es)
- **French** (fr), **German** (de), **Chinese** (zh)
- **Japanese** (ja), **Korean** (ko), **Arabic** (ar)
- **Hindi** (hi) and many more...

## 🤖 Whisper Model Options

| Model | Size | Speed | Accuracy | Best For |
|-------|------|--------|----------|----------|
| Tiny | ~39 MB | Fastest | Good | Quick tests, real-time |
| Base | ~142 MB | Fast | Better | **Recommended** for most users |
| Small | ~461 MB | Medium | High | High accuracy needed |
| Medium | ~1.5 GB | Slow | Very High | Professional transcription |
| Large | ~2.9 GB | Slowest | Best | Maximum accuracy |

## 📁 Output Structure

When processing a file, VideoTranscriber creates:
```
[filename]_transcription/
├── [filename].mp3                    # Extracted audio (if input was video)
├── [filename]_transcription.txt      # Clean, readable text
├── [filename]_transcription.json     # Full data with timestamps & confidence
└── [filename]_transcription.srt      # Subtitle format for video players
```

## 🔧 Troubleshooting

### Common Issues

**"No module named 'core'"**
- Make sure you're running from the VideoTranscriber root directory
- The `core/` directory should be present with `__init__.py`

**"FFmpeg not found"**
- Install FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html)
- Make sure it's in your system PATH

**GUI not starting**
- Run: `python gui_launcher.py` from the project root directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

## 📊 System Requirements

- **Python**: 3.8+ (3.12+ recommended)
- **RAM**: 4GB+ (8GB+ for larger models)
- **Storage**: 2GB+ free space (for models and output)
- **FFmpeg**: Required for audio processing
- **Internet**: Required for first-time model download

## 🎉 Success Stories

- ✅ **Russian video transcription** - Works perfectly!
- ✅ **Organized project structure** - Clean and maintainable
- ✅ **User-friendly GUI** - No command line expertise needed
- ✅ **Multiple output formats** - TXT, JSON, SRT all generated

## 📞 Getting Help

1. Check the **Troubleshooting** section above
2. Review the **examples/** directory for usage patterns
3. Open an issue on GitHub with:
   - Your operating system
   - Python version
   - Full error message
   - Steps to reproduce

---

**Made with ❤️ for easy video transcription!**
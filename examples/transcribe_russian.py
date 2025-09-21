#!/usr/bin/env python3
"""
Russian language transcription script
"""

import os
import whisper
from pathlib import Path

def transcribe_russian_audio():
    """Transcribe audio specifically in Russian language."""
    
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    
    print("🎙️ RUSSIAN LANGUAGE TRANSCRIPTION")
    print("=" * 50)
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    try:
        print("🤖 Loading Whisper model...")
        print("💡 Using 'base' model for better Russian language accuracy")
        
        # Use base model for better accuracy with Russian
        model = whisper.load_model("base")
        
        print("🎵 Transcribing audio in Russian...")
        print("🇷🇺 Language explicitly set to Russian (ru)")
        
        # Explicitly specify Russian language
        result = model.transcribe(audio_path, language="ru")
        
        print("✅ Russian transcription completed!")
        print(f"🌍 Language used: {result.get('language', 'ru')}")
        print(f"📊 Text length: {len(result['text'])} characters")
        
        # Save Russian transcription
        output_path = r"C:\Users\arman\OneDrive\Desktop\russian_transcription.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("РУССКАЯ ТРАНСКРИПЦИЯ / RUSSIAN TRANSCRIPTION\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Аудио файл / Audio file: {audio_path}\n")
            f.write(f"Модель / Model: base\n")
            f.write(f"Язык / Language: Русский (ru)\n")
            f.write(f"Длина текста / Text length: {len(result['text'])} символов\n\n")
            f.write("ТРАНСКРИПЦИЯ / TRANSCRIPTION:\n")
            f.write("-" * 60 + "\n\n")
            f.write(result['text'])
            f.write("\n\n" + "=" * 60 + "\n")
        
        print(f"💾 Russian transcription saved to: {output_path}")
        
        # Also create JSON with detailed segments
        import json
        json_output = r"C:\Users\arman\OneDrive\Desktop\russian_transcription_detailed.json"
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Detailed JSON saved to: {json_output}")
        print()
        
        print("📖 RUSSIAN TRANSCRIPTION PREVIEW:")
        print("-" * 60)
        preview = result['text'][:400] + "..." if len(result['text']) > 400 else result['text']
        print(preview)
        print("-" * 60)
        
        # Show confidence information if available
        if 'segments' in result and result['segments']:
            avg_confidence = sum(seg.get('avg_logprob', 0) for seg in result['segments']) / len(result['segments'])
            print(f"📈 Average confidence: {avg_confidence:.3f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def compare_languages():
    """Compare transcription results in different languages."""
    
    audio_path = r"C:\Users\arman\OneDrive\Desktop\extracted_audio.mp3"
    
    print("🔍 LANGUAGE COMPARISON")
    print("=" * 50)
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    languages = {
        "auto": "Auto-detect",
        "ru": "Russian (Русский)",
        "en": "English"
    }
    
    model = whisper.load_model("base")
    
    results = {}
    
    for lang_code, lang_name in languages.items():
        try:
            print(f"\n🌍 Transcribing as {lang_name}...")
            
            if lang_code == "auto":
                result = model.transcribe(audio_path)
                detected_lang = result.get('language', 'unknown')
                print(f"   Detected language: {detected_lang}")
            else:
                result = model.transcribe(audio_path, language=lang_code)
            
            results[lang_code] = result['text']
            
            # Show preview
            preview = result['text'][:150] + "..." if len(result['text']) > 150 else result['text']
            print(f"   Preview: {preview}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results[lang_code] = f"Error: {e}"
    
    # Save comparison
    comparison_file = r"C:\Users\arman\OneDrive\Desktop\language_comparison.txt"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write("LANGUAGE COMPARISON RESULTS\n")
        f.write("=" * 50 + "\n\n")
        
        for lang_code, lang_name in languages.items():
            f.write(f"{lang_name.upper()}:\n")
            f.write("-" * 30 + "\n")
            f.write(results.get(lang_code, "No result") + "\n\n")
    
    print(f"\n💾 Comparison saved to: {comparison_file}")

def main():
    """Main function with options."""
    print("🎙️ RUSSIAN LANGUAGE TRANSCRIPTION TOOL")
    print("=" * 50)
    print()
    print("Choose your option:")
    print("1. Transcribe specifically in Russian")
    print("2. Compare different language results")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-2): ").strip()
            
            if choice == "0":
                print("До свидания! / Goodbye! 👋")
                break
            elif choice == "1":
                transcribe_russian_audio()
                break
            elif choice == "2":
                compare_languages()
                break
            else:
                print("Invalid choice. Please enter 0-2.")
                
        except KeyboardInterrupt:
            print("\n\nДо свидания! / Goodbye! 👋")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
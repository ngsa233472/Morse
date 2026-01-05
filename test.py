#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
import time
import re
import sys
import argparse

# Standard Morse code dictionary
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    ' ': '/'
}

def text_to_morse(text):
    """Convert text to Morse code."""
    text = re.sub(r'[^A-Z0-9\s\?\.,]', '', text.upper())
    return ' '.join(MORSE_DICT.get(c, '') for c in text)

def play_tone(duration, freq=800):
    """Play a single tone using SoX play (blocking)."""
    subprocess.run(['play', '-n', 'synth', f'{duration:.3f}', 'sine', str(freq), 
                    'vol', '0.3', 'remix', '-'], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def play_morse(morse, wpm=100, freq=800):
    """Play Morse with proper ITU timing ratios."""
    dit_time = 1.2 / wpm  # Standard: PARIS method [web:42][web:51]
    
    print(f"Playing at {wpm} WPM (dit={dit_time*1000:.0f}ms)")
    
    for symbol_group in morse.split(' / '):  # Word groups
        for symbol in symbol_group.split():
            # Play each dot/dash
            for signal in symbol:
                duration = dit_time if signal == '.' else 3 * dit_time
                play_tone(duration, freq)
                time.sleep(dit_time)  # Intra-character gap (1 dit)
            
            time.sleep(3 * dit_time)  # Inter-character gap (3 dit total w/ prev)
        
        time.sleep(7 * dit_time)  # Inter-word gap (7 dit total)

def get_headline():
    """Fetch from working AP Top News RSS."""
    rss_url = 'https://apnews.com/rss'  # Official AP RSS [web:46][web:50]
    try:
        with urllib.request.urlopen(rss_url, timeout=10) as resp:
            tree = ET.parse(resp)
            root = tree.getroot()
        
        # Standard RSS namespace handling
        ns = {'rss': 'http://purl.org/rss/1.0/', 'atom': 'http://www.w3.org/2005/Atom'}
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None:
                return title.text[:40] or "NO TITLE"
        return "NO HEADLINES"
    except Exception as e:
        return f"RSS ERROR: {str(e)[:30]}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AP News to Morse Code Player")
    parser.add_argument('--wpm', type=int, default=100, help='Words per minute (5-30)', 
                       choices=range(5, 31))
    parser.add_argument('--freq', type=int, default=800, help='Tone frequency Hz (400-1200)')
    
    args = parser.parse_args()
    
    print("Fetching AP headline...")
    headline = get_headline()
    print(f"Headline: {headline}\n")
    
    morse = text_to_morse(headline)
    print(f"Morse: {morse}\n")
    
    print("Playing with proper timing...")
    play_morse(morse, args.wpm, args.freq)
    print("Finished!")


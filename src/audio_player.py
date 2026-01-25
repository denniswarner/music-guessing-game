"""
Audio Player Module

Handles downloading, trimming, and playing audio preview clips.
Supports both local playback (pydub/ffmpeg) and browser fallback.
"""

import os
import tempfile
import webbrowser
from typing import Optional

try:
    from pydub import AudioSegment
    from pydub.playback import play
    import requests
    AUDIO_SUPPORT = True
except ImportError:
    AUDIO_SUPPORT = False


class AudioPlayer:
    """
    Handles audio preview playback with automatic fallback.
    
    Attempts to play audio locally using pydub/ffmpeg, falling back
    to browser playback if dependencies are unavailable.
    """
    
    def __init__(self):
        """Initialize the audio player and check for local playback support."""
        self.has_local_support = AUDIO_SUPPORT
        
    def play_preview_clip(
        self, 
        preview_url: str, 
        duration_seconds: int = 10
    ) -> bool:
        """
        Play an audio preview clip for the specified duration.
        
        Args:
            preview_url (str): URL to the audio preview (MP3 format)
            duration_seconds (int): Length of clip to play in seconds (default: 10)
            
        Returns:
            bool: True if playback succeeded, False otherwise
            
        Note:
            If local playback fails, automatically falls back to browser.
        """
        if not self.has_local_support:
            return self._play_in_browser(preview_url)
        
        try:
            return self._play_locally(preview_url, duration_seconds)
        except Exception as e:
            print(f"⚠️  Couldn't play locally: {e}")
            print("🎧 Opening in browser instead...")
            return self._play_in_browser(preview_url)
    
    def _play_locally(self, preview_url: str, duration_seconds: int) -> bool:
        """
        Download and play audio clip locally using pydub.
        
        Args:
            preview_url (str): URL to download audio from
            duration_seconds (int): Duration to trim audio to
            
        Returns:
            bool: True if playback succeeded
            
        Raises:
            Exception: If download or playback fails
        """
        print("🎧 Downloading and playing 10-second clip...")
        
        # Reason: Import here to avoid NameError if module not available
        import requests
        from pydub import AudioSegment
        from pydub.playback import play
        
        # Download the preview
        response = requests.get(preview_url, timeout=10)
        response.raise_for_status()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.mp3'
        ) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Load and trim to specified duration
            audio = AudioSegment.from_mp3(temp_path)
            clip = audio[:duration_seconds * 1000]  # Convert to milliseconds
            
            # Play the clip
            play(clip)
            
            return True
        finally:
            # Clean up temporary file
            # Reason: Ensure cleanup even if playback fails
            try:
                os.unlink(temp_path)
            except OSError:
                pass  # File already deleted or not accessible
    
    def _play_in_browser(self, preview_url: str) -> bool:
        """
        Open audio preview in the default web browser.
        
        Args:
            preview_url (str): URL to open
            
        Returns:
            bool: True (assumes browser opens successfully)
        """
        if not self.has_local_support:
            print("🎧 Opening 30-second preview in browser")
            print("   (Install pydub and ffmpeg for 10-second clips)")
        
        webbrowser.open(preview_url)
        return True
    
    @staticmethod
    def check_dependencies() -> dict:
        """
        Check which audio playback dependencies are available.
        
        Returns:
            dict: Status of each dependency
                - 'pydub': bool
                - 'ffmpeg': bool (requires subprocess check)
                - 'requests': bool
        """
        dependencies = {
            'pydub': False,
            'requests': False,
            'ffmpeg': False
        }
        
        try:
            import pydub
            dependencies['pydub'] = True
        except ImportError:
            pass
        
        try:
            import requests
            dependencies['requests'] = True
        except ImportError:
            pass
        
        # Check for ffmpeg (pydub requires it)
        if dependencies['pydub']:
            try:
                import subprocess
                result = subprocess.run(
                    ['ffmpeg', '-version'],
                    capture_output=True,
                    timeout=2
                )
                dependencies['ffmpeg'] = result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
        
        return dependencies

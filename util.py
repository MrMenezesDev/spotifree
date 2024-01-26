from typing import List
import psutil
from pycaw.pycaw import AudioUtilities, AudioSession
import win32gui
import win32process


APP_NAME = "Spotify.exe"
AD_TEXT = 'Advertisement'
NOT_AD_TEXT = '-'

def get_audio_sessions() -> AudioSession:
    sessions: List[AudioSession] = AudioUtilities.GetAllSessions()
    for session in sessions:
        process = psutil.Process(session.ProcessId)
        if process.name() == APP_NAME:
            return session

def get_session_volume(session: AudioSession) -> float:
    return session.SimpleAudioVolume.GetMasterVolume()

def set_session_volume(session: AudioSession, volume: float):
    session.SimpleAudioVolume.SetMasterVolume(volume, None)

def encontrar_janela_por_pid(pid: int) -> int:
    res = None
    def callback(hwnd, _):
        nonlocal res
        if not win32gui.IsWindowVisible(hwnd):
            return True
        _, cpid = win32process.GetWindowThreadProcessId(hwnd)
        if cpid == pid:
            res = hwnd
            return False
        return True
    try:
        win32gui.EnumWindows(callback, None)
    except Exception as e:
        pass
    return res

def anuncio_tocando(hwnd: int) -> bool:
    text = win32gui.GetWindowText(hwnd)
    return text, AD_TEXT == text or NOT_AD_TEXT not in text


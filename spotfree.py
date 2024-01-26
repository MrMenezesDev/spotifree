import time
from util import get_audio_sessions, get_session_volume, set_session_volume, encontrar_janela_por_pid, anuncio_tocando


session = get_audio_sessions()
if not session:
    print('Spotify não encontrado')
    exit(1)
volume = get_session_volume(session)
if volume == 0:
    volume = 0.5
hwnd = encontrar_janela_por_pid(session.ProcessId)

anuncio_anterior = None
while True:
    time.sleep(1)
    anuncio_atual = anuncio_tocando(hwnd)
    if anuncio_atual != anuncio_anterior:
        if anuncio_atual:
            volume = get_session_volume(session)
            print('Anúncio tocando')
            set_session_volume(session, 0)
        else:
            print('Anúncio não tocando')
            set_session_volume(session, volume)
        anuncio_anterior = anuncio_atual


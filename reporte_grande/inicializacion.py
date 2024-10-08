import pygame
import yt_dlp as youtube_dl
import cv2
import numpy as np
import os
import random
import ctypes  # Para controlar la ventana en Windows
import time
import win32gui
import win32con

# Ocultar la ventana de la consola
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)

# Definir los nombres de los videos y URLs
videos = {
    'video1': 'https://youtu.be/YKKOKC6MnpM',
    'video2': 'https://youtu.be/tqC64Rj9dXA',
    'video3': 'https://youtu.be/xs_OxX5TEW8',
    'video4': 'https://youtu.be/qoL0LBk_4jo',
    'video5': 'https://youtu.be/xs_OxX5TEW8',
    'video6': 'https://youtu.be/7xj1uzuDj_Y',
    'video7': 'https://youtu.be/LiAMJz7RGyA',
    'video8': 'https://youtu.be/98ObRyyoGIU'
}

# Función para reproducir un video desde un punto aleatorio
def play_video(video_name, video_url):
    # Inicializar Pygame
    pygame.init()
    ancho = 350
    alto = 200

    # Crear la ventana
    screen = pygame.display.set_mode((ancho, alto), pygame.NOFRAME)
    pygame.display.set_caption("Iniciando...")

    # Hacer la ventana siempre en la parte superior (funciona en Windows)
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # Descargar el video con yt-dlp
    ydl_opts = {'format': 'bestvideo', 'outtmpl': f'{video_name}.mp4'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Abrir el video descargado con OpenCV
    video_capture = cv2.VideoCapture(f'{video_name}.mp4')

    # Chequear si se pudo abrir el video
    if not video_capture.isOpened():
        print("Error al abrir el video.")
        return

    # Obtener la duración total del video en segundos
    video_duration = video_capture.get(cv2.CAP_PROP_FRAME_COUNT) / video_capture.get(cv2.CAP_PROP_FPS)

    # Elegir un punto de inicio aleatorio entre 0 y la duración - 15 segundos
    if video_duration > 15:
        random_start_time = random.uniform(0, video_duration - 15)
        # Ir al frame correspondiente a este punto
        video_capture.set(cv2.CAP_PROP_POS_MSEC, random_start_time * 1000)
    else:
        print("El video es demasiado corto para iniciar en un punto aleatorio.")
        return

    # Obtener la cantidad de frames por segundo (FPS) del video
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Calcular el límite de frames para 15 segundos
    frame_limit = int(60 * fps)

    done = False
    clock = pygame.time.Clock()
    frame_count = 0

    start_time = time.time()  # Registrar el tiempo de inicio

    while not done and frame_count < frame_limit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Mantener la ventana en la parte superior
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

        # Leer frame del video
        ret, frame = video_capture.read()

        if not ret:
            print("Fin del video.")
            break

        # Convertir el frame de OpenCV (BGR) a un formato compatible con Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.transpose(frame, (1, 0, 2))  # Transponer el frame
        frame_surface = pygame.surfarray.make_surface(frame)

        # Ajustar el tamaño del video a la ventana de Pygame
        frame_surface = pygame.transform.scale(frame_surface, (ancho, alto))

        # Dibujar el frame en la ventana
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        # Actualizar el contador de frames
        frame_count += 1

        clock.tick(fps)  # Controlar la tasa de fotogramas

        # Verificar si hemos alcanzado los 15 segundos
        elapsed_time = time.time() - start_time
        if elapsed_time >= 15:
            print("Fin de los 15 segundos.")
            break

    # Finalizar
    video_capture.release()
    pygame.quit()

    # Eliminar el archivo de video descargado
    # os.remove(f'{video_name}.mp4')
    # print(f'{video_name} removido')

def iniciar_reporte():
    try:
        # Seleccionar aleatoriamente uno de los videos
        video_name, video_url = random.choice(list(videos.items()))

        # Reproducir el video seleccionado aleatoriamente
        play_video(video_name, video_url)

    except Exception as e:
        # Manejar el error y mostrar un mensaje
        print(f"Ocurrió un error: {e}")


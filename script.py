#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script universal para descargar videos de YouTube, Facebook e Instagram
Usa yt-dlp para todas las plataformas (más estable y confiable)
Requiere: pip install yt-dlp
"""

import os
import sys
import re
from pathlib import Path

def crear_carpeta_si_no_existe(ruta):
    """Crea la carpeta de destino si no existe"""
    try:
        Path(ruta).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
        return False

def detectar_plataforma(url):
    """Detecta si la URL es de YouTube, Facebook o Instagram"""
    if re.search(r'(youtube\.com|youtu\.be)', url.lower()):
        return 'youtube'
    elif re.search(r'(facebook\.com|fb\.watch|fb\.me)', url.lower()):
        return 'facebook'
    elif re.search(r'(instagram\.com|instagr\.am)', url.lower()):
        return 'instagram'
    else:
        return 'desconocida'

def limpiar_nombre_archivo(nombre):
    """Limpia caracteres no válidos del nombre del archivo"""
    caracteres_invalidos = '<>:"/\\|?*'
    for char in caracteres_invalidos:
        nombre = nombre.replace(char, '_')
    return nombre

# ===================== FUNCIONES PARA YOUTUBE =====================

def obtener_info_youtube(url):
    """Obtiene información del video de YouTube usando yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Manejar duración de forma robusta
            duracion = info.get('duration')
            duracion_str = "N/A"
            
            if duracion is not None:
                try:
                    duracion_int = int(float(duracion)) if duracion else 0
                    if duracion_int > 0:
                        minutos = duracion_int // 60
                        segundos = duracion_int % 60
                        duracion_str = f"{minutos}:{segundos:02d}"
                except (ValueError, TypeError):
                    duracion_str = "N/A"
            
            # Obtener información de YouTube
            titulo = info.get('title') or info.get('fulltitle') or 'Video de YouTube'
            
            # Formatear vistas
            vistas = info.get('view_count')
            vistas_str = f"{vistas:,}" if vistas else "N/A"
            
            # Formatear likes
            likes = info.get('like_count')
            likes_str = f"{likes:,}" if likes else "N/A"
            
            descripcion = info.get('description') or 'Sin descripción'
            if len(descripcion) > 100:
                descripcion = descripcion[:100] + '...'
            
            return {
                'titulo': titulo,
                'autor': info.get('uploader') or info.get('channel') or 'Canal de YouTube',
                'duracion': duracion_str,
                'vistas': vistas_str,
                'likes': likes_str,
                'descripcion': descripcion,
                'plataforma': 'YouTube'
            }
            
    except Exception as e:
        print(f"Error al obtener información de YouTube: {e}")
        return {
            'titulo': 'Video de YouTube',
            'autor': 'Canal de YouTube',
            'duracion': 'N/A',
            'vistas': 'N/A',
            'likes': 'N/A',
            'descripcion': 'Información no disponible',
            'plataforma': 'YouTube'
        }

def mostrar_opciones_tipo_descarga():
    """Muestra opciones de tipo de descarga para YouTube"""
    print("\n   🎯 Tipo de descarga:")
    opciones = {
        1: {
            'tipo': 'video',
            'descripcion': 'Video completo (con audio)'
        },
        2: {
            'tipo': 'audio_mp3',
            'descripcion': 'Solo audio en formato MP3'
        },
        3: {
            'tipo': 'audio_wav',
            'descripcion': 'Solo audio en formato WAV'
        }
    }
    
    for num, info in opciones.items():
        print(f"   {num}. {info['descripcion']}")
    
    return opciones

def mostrar_opciones_calidad_youtube():
    """Muestra opciones predefinidas de calidad para video de YouTube"""
    print("\n   📺 Opciones de calidad de video:")
    opciones = {
        1: {
            'formato': 'best[height<=1080]/best',
            'descripcion': '1080p (Full HD) - Mejor calidad'
        },
        2: {
            'formato': 'best[height<=720]/best',
            'descripcion': '720p (HD) - Buena calidad'
        },
        3: {
            'formato': 'best[height<=480]/best',
            'descripcion': '480p (SD) - Calidad media'
        },
        4: {
            'formato': 'best[height<=360]/best',
            'descripcion': '360p - Calidad básica'
        },
        5: {
            'formato': 'best',
            'descripcion': 'Mejor calidad disponible (automático)'
        },
        6: {
            'formato': 'worst',
            'descripcion': 'Menor calidad (descarga más rápida)'
        }
    }
    
    for num, info in opciones.items():
        print(f"   {num}. {info['descripcion']}")
    
    return opciones

def mostrar_opciones_calidad_audio():
    """Muestra opciones de calidad para audio"""
    print("\n   🎵 Opciones de calidad de audio:")
    opciones = {
        1: {
            'formato': 'bestaudio',
            'descripcion': 'Mejor calidad de audio disponible'
        },
        2: {
            'formato': 'bestaudio[abr<=320]',
            'descripcion': 'Hasta 320 kbps (excelente calidad)'
        },
        3: {
            'formato': 'bestaudio[abr<=192]',
            'descripcion': 'Hasta 192 kbps (buena calidad)'
        },
        4: {
            'formato': 'bestaudio[abr<=128]',
            'descripcion': 'Hasta 128 kbps (calidad estándar)'
        }
    }
    
    for num, info in opciones.items():
        print(f"   {num}. {info['descripcion']}")
    
    return opciones

def descargar_youtube(url, carpeta_destino, nuevo_nombre):
    """Descarga video o audio de YouTube usando yt-dlp con opciones de formato"""
    tipo_seleccionado = 'video'  # Valor por defecto
    
    try:
        import yt_dlp
        
        print(f"\n   🔗 Conectando con YouTube...")
        
        # Paso 1: Seleccionar tipo de descarga
        opciones_tipo = mostrar_opciones_tipo_descarga()
        
        print()
        while True:
            try:
                opcion_tipo = input(f"   Selecciona el tipo de descarga (1-{len(opciones_tipo)}): ").strip()
                opcion_tipo_num = int(opcion_tipo)
                
                if 1 <= opcion_tipo_num <= len(opciones_tipo):
                    tipo_seleccionado = opciones_tipo[opcion_tipo_num]['tipo']
                    descripcion_tipo = opciones_tipo[opcion_tipo_num]['descripcion']
                    break
                else:
                    print(f"   ❌ Opción inválida. Selecciona entre 1 y {len(opciones_tipo)}")
            except ValueError:
                print("   ❌ Por favor ingresa un número válido.")
        
        # Paso 2: Seleccionar calidad según el tipo
        if tipo_seleccionado == 'video':
            # Mostrar opciones de calidad de video
            opciones_calidad = mostrar_opciones_calidad_youtube()
            print()
            while True:
                try:
                    opcion_calidad = input(f"   Selecciona la calidad (1-{len(opciones_calidad)}): ").strip()
                    opcion_calidad_num = int(opcion_calidad)
                    
                    if 1 <= opcion_calidad_num <= len(opciones_calidad):
                        formato_seleccionado = opciones_calidad[opcion_calidad_num]['formato']
                        descripcion_calidad = opciones_calidad[opcion_calidad_num]['descripcion']
                        break
                    else:
                        print(f"   ❌ Opción inválida. Selecciona entre 1 y {len(opciones_calidad)}")
                except ValueError:
                    print("   ❌ Por favor ingresa un número válido.")
        
        else:  # audio_mp3 o audio_wav
            # Mostrar opciones de calidad de audio
            opciones_calidad = mostrar_opciones_calidad_audio()
            print()
            while True:
                try:
                    opcion_calidad = input(f"   Selecciona la calidad de audio (1-{len(opciones_calidad)}): ").strip()
                    opcion_calidad_num = int(opcion_calidad)
                    
                    if 1 <= opcion_calidad_num <= len(opciones_calidad):
                        formato_seleccionado = opciones_calidad[opcion_calidad_num]['formato']
                        descripcion_calidad = opciones_calidad[opcion_calidad_num]['descripcion']
                        break
                    else:
                        print(f"   ❌ Opción inválida. Selecciona entre 1 y {len(opciones_calidad)}")
                except ValueError:
                    print("   ❌ Por favor ingresa un número válido.")
        
        # Paso 3: Configurar opciones de yt-dlp según el tipo de descarga
        if tipo_seleccionado == 'video':
            # Configuración para video
            ydl_opts = {
                'outtmpl': os.path.join(carpeta_destino, f'{nuevo_nombre}.%(ext)s'),
                'format': formato_seleccionado,
                'noplaylist': True,
                'ignoreerrors': False,
                'no_warnings': False,
                'extract_flat': False,
                'embed_metadata': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            }
            
        elif tipo_seleccionado == 'audio_mp3':
            # Configuración para audio MP3
            ydl_opts = {
                'outtmpl': os.path.join(carpeta_destino, f'{nuevo_nombre}.%(ext)s'),
                'format': formato_seleccionado,
                'noplaylist': True,
                'ignoreerrors': False,
                'no_warnings': False,
                'extract_flat': False,
                'embed_metadata': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',  # Calidad máxima para MP3
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            }
            
        elif tipo_seleccionado == 'audio_wav':
            # Configuración para audio WAV
            ydl_opts = {
                'outtmpl': os.path.join(carpeta_destino, f'{nuevo_nombre}.%(ext)s'),
                'format': formato_seleccionado,
                'noplaylist': True,
                'ignoreerrors': False,
                'no_warnings': False,
                'extract_flat': False,
                'embed_metadata': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            }
        
        print(f"\n   📥 Iniciando descarga desde YouTube...")
        print(f"   🎯 Tipo: {descripcion_tipo}")
        print(f"   📊 Calidad: {descripcion_calidad}")
        
        # Mostrar nota sobre ffmpeg si se descarga audio
        if tipo_seleccionado in ['audio_mp3', 'audio_wav']:
            print("   ℹ️  Nota: Se requiere ffmpeg para conversión de audio")
        
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("-" * 50)
        
        # Mensaje de éxito específico según el tipo
        if tipo_seleccionado == 'video':
            print("✅ ¡Descarga de video de YouTube completada!")
        elif tipo_seleccionado == 'audio_mp3':
            print("✅ ¡Descarga de audio MP3 de YouTube completada!")
        elif tipo_seleccionado == 'audio_wav':
            print("✅ ¡Descarga de audio WAV de YouTube completada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la descarga de YouTube: {e}")
        
        error_msg = str(e).lower()
        if "ffmpeg" in error_msg and tipo_seleccionado in ['audio_mp3', 'audio_wav']:
            print("   💡 Error de ffmpeg: Se requiere ffmpeg para conversión de audio.")
            print("   📥 Instala ffmpeg desde: https://ffmpeg.org/")
            print("   💡 O intenta descargar solo el video.")
        elif "private" in error_msg or "unavailable" in error_msg:
            print("   💡 El video puede ser privado o no estar disponible.")
        elif "age" in error_msg or "restricted" in error_msg:
            print("   💡 El video puede tener restricciones de edad.")
            print("   📝 Intenta con otro video o verifica la configuración de tu cuenta.")
        elif "region" in error_msg or "blocked" in error_msg:
            print("   💡 El video puede estar bloqueado en tu región.")
        elif "copyright" in error_msg:
            print("   💡 El video puede tener restricciones de copyright.")
        elif "live" in error_msg:
            print("   💡 No se pueden descargar transmisiones en vivo.")
        elif "premium" in error_msg:
            print("   💡 El video puede requerir YouTube Premium.")
        elif "sign in" in error_msg or "login" in error_msg:
            print("   💡 El video puede requerir iniciar sesión.")
        else:
            print("   💡 Error desconocido. Verifica la URL y la conexión.")
            print("   📋 Soluciones:")
            print("      - Verifica que el video sea público")
            print("      - Copia la URL directamente desde YouTube")
            print("      - Intenta con otro video")
            print("      - Actualiza yt-dlp: pip install --upgrade yt-dlp")
        
        return False

# ===================== FUNCIONES PARA FACEBOOK =====================

def obtener_info_facebook(url):
    """Obtiene información del video de Facebook usando yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Manejar duración de forma robusta
            duracion = info.get('duration')
            duracion_str = "N/A"
            
            if duracion is not None:
                try:
                    duracion_int = int(float(duracion)) if duracion else 0
                    if duracion_int > 0:
                        minutos = duracion_int // 60
                        segundos = duracion_int % 60
                        duracion_str = f"{minutos}:{segundos:02d}"
                except (ValueError, TypeError):
                    duracion_str = "N/A"
            
            titulo = info.get('title') or info.get('fulltitle') or 'Video de Facebook'
            
            descripcion = info.get('description') or info.get('alt_title') or 'Sin descripción'
            if len(descripcion) > 100:
                descripcion = descripcion[:100] + '...'
            
            return {
                'titulo': titulo,
                'autor': info.get('uploader') or info.get('uploader_id') or 'Usuario de Facebook',
                'duracion': duracion_str,
                'descripcion': descripcion,
                'plataforma': 'Facebook'
            }
            
    except Exception as e:
        print(f"Error al obtener información de Facebook: {e}")
        return {
            'titulo': 'Video de Facebook',
            'autor': 'Usuario de Facebook',
            'duracion': 'N/A',
            'descripcion': 'Información no disponible',
            'plataforma': 'Facebook'
        }

def descargar_facebook(url, carpeta_destino, nuevo_nombre):
    """Descarga video de Facebook usando yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'outtmpl': os.path.join(carpeta_destino, f'{nuevo_nombre}.%(ext)s'),
            'format': 'best[height<=720]/best',
            'noplaylist': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'extract_flat': False,
        }
        
        print(f"\n   📥 Iniciando descarga desde Facebook...")
        print("   ℹ️  Nota: Solo funciona con videos públicos")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("-" * 50)
        print("✅ ¡Descarga de Facebook completada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la descarga de Facebook: {e}")
        
        error_msg = str(e).lower()
        if "private" in error_msg or "login" in error_msg:
            print("   💡 El video puede ser privado o requerir autenticación.")
        elif "not available" in error_msg or "removed" in error_msg:
            print("   💡 El video no está disponible o fue eliminado.")
        else:
            print("   💡 Verifica que el video sea público y la URL sea correcta.")
        
        return False

# ===================== FUNCIONES PARA INSTAGRAM =====================

def obtener_info_instagram(url):
    """Obtiene información del video de Instagram usando yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            duracion = info.get('duration')
            duracion_str = "N/A"
            
            if duracion is not None:
                try:
                    duracion_int = int(float(duracion)) if duracion else 0
                    if duracion_int > 0:
                        minutos = duracion_int // 60
                        segundos = duracion_int % 60
                        duracion_str = f"{minutos}:{segundos:02d}"
                except (ValueError, TypeError):
                    duracion_str = "N/A"
            
            titulo = info.get('title') or info.get('fulltitle') or 'Post de Instagram'
            autor = (info.get('uploader') or 
                    info.get('uploader_id') or 
                    info.get('channel') or 
                    'Usuario de Instagram')
            
            descripcion = info.get('description') or info.get('alt_title') or 'Sin descripción'
            if len(descripcion) > 100:
                descripcion = descripcion[:100] + '...'
            
            likes = info.get('like_count', 'N/A')
            views = info.get('view_count', 'N/A')
            
            return {
                'titulo': titulo,
                'autor': autor,
                'duracion': duracion_str,
                'descripcion': descripcion,
                'likes': likes if likes != 'N/A' else None,
                'views': views if views != 'N/A' else None,
                'plataforma': 'Instagram'
            }
            
    except Exception as e:
        print(f"Error al obtener información de Instagram: {e}")
        return {
            'titulo': 'Post de Instagram',
            'autor': 'Usuario de Instagram',
            'duracion': 'N/A',
            'descripcion': 'Información no disponible',
            'plataforma': 'Instagram'
        }

def descargar_instagram(url, carpeta_destino, nuevo_nombre):
    """Descarga video de Instagram usando yt-dlp"""
    try:
        import yt_dlp
        
        ydl_opts = {
            'outtmpl': os.path.join(carpeta_destino, f'{nuevo_nombre}.%(ext)s'),
            'format': 'best[height<=1080]/best',
            'noplaylist': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '115',
                'Connection': 'keep-alive',
            }
        }
        
        print(f"\n   📥 Iniciando descarga desde Instagram...")
        print("   ℹ️  Nota: Solo funciona con posts públicos")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("-" * 50)
        print("✅ ¡Descarga de Instagram completada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la descarga de Instagram: {e}")
        
        error_msg = str(e).lower()
        if "private" in error_msg or "login" in error_msg:
            print("   💡 La cuenta o el post puede ser privado.")
        elif "not available" in error_msg or "removed" in error_msg:
            print("   💡 El post no está disponible o fue eliminado.")
        elif "rate" in error_msg or "too many" in error_msg:
            print("   💡 Instagram está limitando las descargas. Espera un momento.")
        else:
            print("   💡 Verifica que el post sea público y la URL sea correcta.")
        
        return False

# ===================== FUNCIONES UNIVERSALES =====================

def descargar_video_universal(url, carpeta_destino, nuevo_nombre):
    """Función universal que detecta la plataforma y usa el método apropiado"""
    plataforma = detectar_plataforma(url)
    
    if plataforma == 'youtube':
        return descargar_youtube(url, carpeta_destino, nuevo_nombre)
    elif plataforma == 'facebook':
        return descargar_facebook(url, carpeta_destino, nuevo_nombre)
    elif plataforma == 'instagram':
        return descargar_instagram(url, carpeta_destino, nuevo_nombre)
    else:
        print(f"❌ Plataforma no soportada. Solo YouTube, Facebook e Instagram son compatibles.")
        return False

def obtener_info_universal(url):
    """Función universal para obtener información del video"""
    plataforma = detectar_plataforma(url)
    
    if plataforma == 'youtube':
        return obtener_info_youtube(url)
    elif plataforma == 'facebook':
        return obtener_info_facebook(url)
    elif plataforma == 'instagram':
        return obtener_info_instagram(url)
    else:
        return None

def verificar_dependencias():
    """Verifica que yt-dlp esté instalado"""
    try:
        import yt_dlp
        print("✅ yt-dlp: Instalado")
        
        # Verificar versión
        version = yt_dlp.version.__version__
        print(f"   📦 Versión: {version}")
        
    except ImportError:
        print("❌ yt-dlp: No instalado")
        print("\nInstálalo ejecutando:")
        print("pip install yt-dlp")
        return False
    
    # Verificar ffmpeg (requerido para conversión de audio)
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ffmpeg: Instalado")
        else:
            print("⚠️  ffmpeg: No encontrado")
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        print("⚠️  ffmpeg: No encontrado")
        print("   💡 IMPORTANTE: ffmpeg es requerido para descargar audio (MP3/WAV)")
        print("   📥 Descarga desde: https://ffmpeg.org/")
        print("   🎯 Sin ffmpeg solo podrás descargar videos completos")
    
    return True

def main():
    print("=" * 70)
    print("    DESCARGADOR UNIVERSAL DE VIDEOS")
    print("      YouTube + Facebook + Instagram")
    print("=" * 70)
    print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    print("\n✅ Todas las plataformas usan yt-dlp (máxima estabilidad)")
    print("💡 Para actualizar: pip install --upgrade yt-dlp")
    print()
    
    while True:
        try:
            # Solicitar URL del video
            print("1. URL del video:")
            url = input("   Ingresa la URL (YouTube, Facebook o Instagram): ").strip()
            
            if not url:
                print("   ❌ La URL no puede estar vacía.")
                continue
            
            # Detectar plataforma
            plataforma = detectar_plataforma(url)
            
            if plataforma == 'desconocida':
                print("   ❌ URL no reconocida. Solo se admiten URLs de YouTube, Facebook o Instagram.")
                continue
            
            print(f"   🎯 Plataforma detectada: {plataforma.upper()}")
            
            # Obtener información del video
            print(f"\n   📡 Obteniendo información del contenido...")
            info_video = obtener_info_universal(url)
            
            if info_video:
                print(f"   🏷️  Plataforma: {info_video['plataforma']}")
                print(f"   📹 Título: {info_video['titulo']}")
                print(f"   👤 Autor: {info_video['autor']}")
                print(f"   ⏱️  Duración: {info_video['duracion']}")
                
                # Mostrar información específica según la plataforma
                if 'vistas' in info_video and info_video['vistas'] and info_video['vistas'] != 'N/A':
                    print(f"   👁️  Vistas: {info_video['vistas']}")
                if 'likes' in info_video and info_video['likes'] and info_video['likes'] != 'N/A':
                    print(f"   ❤️  Likes: {info_video['likes']}")
                if 'views' in info_video and info_video['views'] and info_video['views'] != 'N/A':
                    print(f"   👁️  Visualizaciones: {info_video['views']:,}")
                    
                print(f"   📝 Descripción: {info_video['descripcion']}")
            else:
                print("   ⚠️  No se pudo obtener información del contenido, pero se intentará descargar.")
            
            print()
            
            # Solicitar carpeta de destino
            print("2. Carpeta de destino:")
            print("   (Presiona Enter para usar la carpeta de Descargas)")
            carpeta_destino = input("   Ingresa la ruta donde guardar el video: ").strip()
            
            if not carpeta_destino:
                # Usar carpeta de descargas del usuario por defecto
                try:
                    carpeta_destino = os.path.join(str(Path.home()), "Downloads")
                    print(f"   📁 Usando carpeta por defecto: {carpeta_destino}")
                except Exception:
                    # Fallback si no se puede acceder a la carpeta del usuario
                    carpeta_destino = f"./descargas_{plataforma}"
                    print(f"   📁 Usando carpeta local: {carpeta_destino}")
            
            # Crear carpeta si no existe
            if not crear_carpeta_si_no_existe(carpeta_destino):
                continue
            
            print()
            
            # Solicitar nuevo nombre
            print("3. Nombre del archivo:")
            nuevo_nombre = input("   Ingresa el nuevo nombre (sin extensión): ").strip()
            
            if not nuevo_nombre:
                nuevo_nombre = f"video_{plataforma}"
                print(f"   📝 Usando nombre por defecto: {nuevo_nombre}")
            
            # Limpiar caracteres no válidos del nombre
            nuevo_nombre = limpiar_nombre_archivo(nuevo_nombre)
            
            print()
            
            # Mostrar notas importantes según la plataforma
            if plataforma == 'instagram':
                print("   📋 Notas para Instagram:")
                print("      • Solo posts públicos")
                print("      • Puede tener limitaciones de descarga")
                print()
            elif plataforma == 'facebook':
                print("   📋 Notas para Facebook:")
                print("      • Solo videos públicos")
                print()
            elif plataforma == 'youtube':
                print("   📋 Notas para YouTube:")
                print("      • Puedes descargar video completo o solo audio")
                print("      • Audio disponible en MP3 o WAV")
                print("      • Se requiere ffmpeg para conversión de audio")
                print("      • Videos privados no funcionan")
                print()
            
            print("=" * 70)
            
            # Confirmar descarga
            respuesta = input(f"¿Proceder con la descarga desde {plataforma.upper()}? (s/n): ").strip().lower()
            
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                print()
                exito = descargar_video_universal(url, carpeta_destino, nuevo_nombre)
                
                if exito:
                    print(f"\n✅ El archivo se guardó en: {os.path.abspath(carpeta_destino)}")
                else:
                    print("\n❌ La descarga falló.")
            else:
                print("\n❌ Descarga cancelada.")
            
            print()
            print("=" * 70)
            
            # Preguntar si desea descargar otro video
            otra_descarga = input("¿Descargar otro video? (s/n): ").strip().lower()
            if otra_descarga not in ['s', 'si', 'sí', 'y', 'yes']:
                break
            
            print("\n" + "=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n❌ Operación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("Intentando nuevamente...")
            print()
    
    print("\n¡Gracias por usar el descargador universal!")
    print("=" * 70)

if __name__ == "__main__":
    main()
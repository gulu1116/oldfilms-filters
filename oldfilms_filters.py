# oldfilms_filters.py - Extract your filter functions into this module

import subprocess
import logging

logger = logging.getLogger(__name__)

def get_decade_filter_config():
    """Return filter configurations for each decade with customization options"""
    return {
        '1900s': {
            'name': '1900s - Early Cinema',
            'description': 'Hand-cranked cameras, sepia tone, heavy scratches',
            'fps': 12,
            'max_height': 240,  # Changed from resolution to max_height
            'filters': [
                'colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131',  # Sepia
                # 'noise=alls=50:allf=t',  # Heavy noise
                # 'eq=brightness=0.2:contrast=1.4:gamma=1.3',
                # 'vignette=angle=PI/2:x=0.5:y=0.5',
                'noise=alls=20:allf=t',  # Reduced noise to prevent issues
                'eq=brightness=0.1:contrast=1.3:gamma=1.2',  # Adjusted parameters
                'vignette=angle=3.14/2',
                'fps=12'

            ],
            'customizable': True,
            'options': {
                'sepia_intensity': {'min': 0.5, 'max': 1.5, 'default': 1.0, 'label': 'Sepia Intensity'},
                'scratches_level': {'min': 30, 'max': 70, 'default': 50, 'label': 'Film Scratches'},
                'vignette_strength': {'min': 0.3, 'max': 1.0, 'default': 0.7, 'label': 'Vignette Effect'},
                'flicker_enabled': {'enabled': True, 'label': 'Film Flicker Effect'},
                'frame_rate': {'min': 8, 'max': 18, 'default': 12, 'label': 'Playback Speed (fps)'}
            }
        },
        '1910s': {
            'name': '1910s - Silent Films',
            'description': 'Charlie Chaplin era, flickering, title cards',
            'fps': 16,
            'max_height': 360,
            'filters': [
                'colorchannelmixer=.3:.6:.1:0:.3:.6:.1:0:.3:.6:.1',  # Monochrome
                'noise=alls=40:allf=t',
                'eq=brightness=0.15:contrast=1.35:gamma=1.25',
                'fps=16'
            ],
            'customizable': True,
            'options': {
                'contrast_level': {'min': 1.0, 'max': 2.0, 'default': 1.35, 'label': 'Film Contrast'},
                'grain_intensity': {'min': 20, 'max': 60, 'default': 40, 'label': 'Film Grain'},
                'flicker_enabled': {'enabled': True, 'label': 'Silent Film Flicker'},
                'title_card_enabled': {'enabled': False, 'label': 'Add Title Card'},
                'title_card_text': {'default': 'SILENT FILM', 'label': 'Title Card Text'}
            }
        },
        '1920s': {
            'name': '1920s - Jazz Age Films',
            'description': 'Art deco style, high contrast black & white',
            'fps': 18,
            'max_height': 480,
            'filters': [
                'hue=s=0',  # Remove all color
                'noise=alls=35:allf=t',
                'eq=brightness=0.1:contrast=1.3:gamma=1.2',
                'vignette=angle=PI/3',
                'fps=18'
            ],
            'customizable': True,
            'options': {
                'contrast_boost': {'min': 1.1, 'max': 1.8, 'default': 1.3, 'label': 'Art Deco Contrast'},
                'grain_level': {'min': 15, 'max': 50, 'default': 35, 'label': 'Film Grain'},
                'vignette_style': {'options': ['classic', 'art_deco', 'none'], 'default': 'classic', 'label': 'Vignette Style'},
                'glamour_glow': {'enabled': False, 'label': 'Hollywood Glamour Glow'}
            }
        },
        '1930s': {
            'name': '1930s - Golden Age',
            'description': 'Early talkies, soft focus, dramatic lighting',
            'fps': 24,
            'max_height': 540,
            'filters': [
                'hue=s=0',
                'noise=alls=25:allf=t',
                'eq=brightness=0.05:contrast=1.25:gamma=1.15',
                'gblur=sigma=0.5',  # Slight blur for dream-like quality
                'fps=24'
            ],
            'customizable': True,
            'options': {
                'soft_focus': {'min': 0.2, 'max': 1.5, 'default': 0.5, 'label': 'Soft Focus Intensity'},
                'dramatic_lighting': {'min': 0.8, 'max': 1.5, 'default': 1.25, 'label': 'Dramatic Contrast'},
                'film_quality': {'min': 10, 'max': 40, 'default': 25, 'label': 'Film Grain'},
                'golden_tone': {'enabled': False, 'label': 'Subtle Golden Tint'}
            }
        },
        '1940s': {
            'name': '1940s - War Era',
            'description': 'Film noir style, high contrast, dramatic shadows',
            'fps': 24,
            'max_height': 540,
            'filters': [
                'hue=s=0',
                'noise=alls=20:allf=t',
                'eq=brightness=0.0:contrast=1.4:gamma=1.1',
                'fps=24'
            ],
            'customizable': True,
            'options': {
                'noir_contrast': {'min': 1.2, 'max': 2.0, 'default': 1.4, 'label': 'Film Noir Contrast'},
                'shadow_depth': {'min': -0.3, 'max': 0.1, 'default': 0.0, 'label': 'Shadow Intensity'},
                'film_grain': {'min': 10, 'max': 35, 'default': 20, 'label': 'Wartime Film Quality'},
                'cigarette_haze': {'enabled': False, 'label': 'Atmospheric Haze Effect'}
            }
        },
        '1950s': {
            'name': '1950s - Technicolor Era',
            'description': 'Early color films, saturated colors, film grain',
            'fps': 24,
            'max_height': 540,
            'filters': [
                'colorbalance=rs=0.1:gs=-0.05:bs=-0.1',  # Fixed: Better color grading
                'hue=s=1.3:h=5',  # Boosted saturation
                'noise=alls=18:allf=t',
                'eq=brightness=0.08:contrast=1.2',
                'fps=24'
            ],
            'customizable': True,
            'options': {
                'technicolor_saturation': {'min': 1.0, 'max': 2.0, 'default': 1.3, 'label': 'Technicolor Saturation'},
                'color_shift': {'min': -10, 'max': 15, 'default': 5, 'label': 'Color Temperature Shift'},
                'film_grain': {'min': 8, 'max': 30, 'default': 18, 'label': 'Color Film Grain'},
                'vibrant_reds': {'enabled': True, 'label': 'Enhanced Red Channel'},
                'golden_glow': {'enabled': False, 'label': 'Hollywood Golden Glow'}
            }
        },
        '1960s': {
            'name': '1960s - Kodachrome',
            'description': 'Vibrant colors, slight oversaturation, film texture',
            'fps': 24,
            'max_height': 720,
            'filters': [
                'colorbalance=rs=0.1:gs=0.05:bs=-0.05',  # Fixed: Gentle warm tone instead of curves
                'hue=s=1.2:h=-3',
                'noise=alls=15:allf=t',
                'eq=brightness=0.05:contrast=1.15',
                'fps=24'
            ],
            'customizable': True,
            'options': {
                'kodachrome_look': {'min': 1.0, 'max': 1.8, 'default': 1.2, 'label': 'Kodachrome Saturation'},
                'warm_tone': {'min': -8, 'max': 5, 'default': -3, 'label': 'Warm Color Cast'},
                'film_texture': {'min': 5, 'max': 25, 'default': 15, 'label': 'Film Texture'},
                'psychedelic_boost': {'enabled': False, 'label': 'Psychedelic Color Boost'},
                'fade_edges': {'enabled': False, 'label': 'Vintage Photo Fade'}
            }
        },
        '1970s': {
            'name': '1970s - Super 8 / 16mm',
            'description': 'Home movies, warm tones, heavy grain',
            'fps': 18,
            'max_height': 720,
            'filters': [
                'colorbalance=rs=0.05:gs=0.1:bs=-0.2',  # Fixed: Warm tone using colorbalance
                'hue=s=0.9:h=-8',
                'noise=alls=22:allf=t',
                'vignette=angle=PI/4',
                'eq=brightness=0.06:contrast=1.12',
                'fps=18'
            ],
            'customizable': True,
            'options': {
                'super8_grain': {'min': 10, 'max': 40, 'default': 22, 'label': 'Super 8 Grain'},
                'warm_vintage': {'min': -15, 'max': 0, 'default': -8, 'label': 'Warm Vintage Tone'},
                'home_movie_feel': {'min': 0.7, 'max': 1.2, 'default': 0.9, 'label': 'Home Movie Saturation'},
                'light_leaks': {'enabled': False, 'label': 'Light Leak Effects'},
                'handheld_shake': {'enabled': False, 'label': 'Handheld Camera Shake'}
            }
        },
        '1980s': {
            'name': '1980s - VHS Era',
            'description': 'VHS tapes, scanlines, color bleeding, timestamps',
            'fps': 25,
            'max_height': 480,
            'filters': [
                'colorbalance=rs=0.1:gs=0.1:bs=0.1',  # Fixed: Subtle color adjustment
                'noise=alls=12:allf=t',
                'hue=s=1.25:h=8',
                'eq=brightness=0.03:contrast=1.08',
                'fps=25'
            ],
            'customizable': True,
            'options': {
                'static_level': {'min': 5, 'max': 25, 'default': 12, 'label': 'VHS Static'},
                'color_bleeding': {'min': 1.0, 'max': 1.8, 'default': 1.25, 'label': 'Color Bleeding'},
                'timestamp_enabled': {'enabled': True, 'label': 'VHS Timestamp'},
                'timestamp_text': {'default': '12/25/85 14:30', 'label': 'Custom Timestamp'},
                'scanlines_enabled': {'enabled': True, 'label': 'VHS Scanlines'},
                'tracking_issues': {'enabled': False, 'label': 'Tracking Problems'}
            }
        },
        '1990s': {
            'name': '1990s - Camcorder',
            'description': 'Digital camcorders, auto-focus hunting, date stamps',
            'fps': 30,
            'max_height': 480,
            'filters': [
                'colorbalance=rs=0.05:gs=0.05:bs=0.05',  # Fixed: Subtle digital look
                'noise=alls=8:allf=t',
                'hue=s=1.1:h=2',
                'eq=brightness=0.02:contrast=1.05',
                'fps=30'
            ],
            'customizable': True,
            'options': {
                'digital_noise': {'min': 3, 'max': 15, 'default': 8, 'label': 'Digital Artifacts'},
                'camcorder_saturation': {'min': 0.9, 'max': 1.4, 'default': 1.1, 'label': 'Camcorder Color'},
                'timestamp_enabled': {'enabled': True, 'label': 'Digital Date Stamp'},
                'timestamp_text': {'default': '12/25/1995 14:30:45', 'label': 'Custom Date/Time'},
                'auto_focus_enabled': {'enabled': True, 'label': 'Auto-focus Hunting'},
                'zoom_artifacts': {'enabled': False, 'label': 'Digital Zoom Artifacts'}
            }
        }
    }

def build_filter_command(decade, custom_options=None):
    """Build FFmpeg filter command for specific decade with customizations"""
    config = get_decade_filter_config()[decade]
    filters = config['filters'].copy()
    
    
    # Add aspect-ratio preserving scaling
    if 'max_height' in config:
        max_height = config['max_height']
        filters.append(f"scale=-1:{max_height}")
    
    return ','.join(filters)

def process_video_with_ffmpeg(input_path, output_path, decade, custom_options=None):
    try:
        filter_string = build_filter_command(decade, custom_options)
        cmd = [
            'ffmpeg', '-i', input_path, '-vf', filter_string,
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '128k', '-y', output_path
        ]
        
        logger.info(f"Processing with {decade} filter")
        logger.info(f"Custom options: {custom_options}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stderr if result.returncode != 0 else "Success"
    except Exception as e:
        return False, str(e)

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
#
# # HTML template
# HTML_TEMPLATE = '''
# <!DOCTYPE html>
# <html lang="zh-CN">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>复古视频滤镜 - 时光影像</title>
#     <style>
#         * { margin: 0; padding: 0; box-sizing: border-box; }
#         body {
#             font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
#             background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
#             min-height: 100vh;
#             color: #f0f0f0;
#             line-height: 1.6;
#         }
#         .container {
#             max-width: 1200px;
#             margin: 0 auto;
#             padding: 20px;
#         }
#         .header {
#             text-align: center;
#             margin-bottom: 40px;
#             padding: 20px;
#             background: rgba(0, 0, 0, 0.3);
#             border-radius: 15px;
#             backdrop-filter: blur(10px);
#             border: 1px solid rgba(255, 255, 255, 0.1);
#         }
#         .header h1 {
#             font-size: 2.8em;
#             margin-bottom: 10px;
#             background: linear-gradient(45deg, #d4af37, #f5f5dc, #c0c0c0);
#             background-size: 300% 300%;
#             -webkit-background-clip: text;
#             background-clip: text;
#             -webkit-text-fill-color: transparent;
#             animation: gradient 6s ease infinite;
#             font-weight: 300;
#             letter-spacing: 1px;
#         }
#         .header p {
#             color: #cccccc;
#             margin-bottom: 5px;
#         }
#         .header p.subtitle {
#             font-size: 1.1em;
#             color: #d4af37;
#         }
#         @keyframes gradient {
#             0% { background-position: 0% 50%; }
#             50% { background-position: 100% 50%; }
#             100% { background-position: 0% 50%; }
#         }
#         .section {
#             background: rgba(30, 30, 46, 0.7);
#             border-radius: 15px;
#             padding: 30px;
#             margin-bottom: 30px;
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
#             transition: transform 0.3s ease, box-shadow 0.3s ease;
#         }
#         .section:hover {
#             transform: translateY(-5px);
#             box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
#         }
#         .section h2 {
#             color: #d4af37;
#             margin-bottom: 20px;
#             font-weight: 400;
#             font-size: 1.6em;
#             border-bottom: 1px solid rgba(212, 175, 55, 0.3);
#             padding-bottom: 10px;
#         }
#         .upload-area {
#             border: 2px dashed rgba(212, 175, 55, 0.5);
#             border-radius: 15px;
#             padding: 40px;
#             text-align: center;
#             cursor: pointer;
#             transition: all 0.3s ease;
#             background: rgba(40, 40, 60, 0.5);
#             position: relative;
#             overflow: hidden;
#         }
#         .upload-area:before {
#             content: '';
#             position: absolute;
#             top: -50%;
#             left: -50%;
#             width: 200%;
#             height: 200%;
#             background: linear-gradient(
#                 to bottom right,
#                 rgba(212, 175, 55, 0.1) 0%,
#                 transparent 50%,
#                 rgba(212, 175, 55, 0.1) 100%
#             );
#             transform: rotate(30deg);
#             transition: all 0.5s ease;
#         }
#         .upload-area:hover:before {
#             transform: rotate(45deg);
#         }
#         .upload-area:hover {
#             border-color: rgba(212, 175, 55, 0.8);
#             background: rgba(50, 50, 70, 0.6);
#         }
#         .upload-area p {
#             color: #f0f0f0;
#             font-size: 1.2em;
#             margin-bottom: 10px;
#         }
#         .upload-area p small {
#             color: #aaaaaa;
#             font-size: 0.9em;
#         }
#         .upload-icon {
#             font-size: 3em;
#             margin-bottom: 15px;
#             color: rgba(212, 175, 55, 0.7);
#         }
#         .decade-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#             gap: 15px;
#             margin-top: 20px;
#         }
#         .decade-option {
#             background: rgba(40, 40, 60, 0.7);
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             border-radius: 12px;
#             padding: 20px;
#             cursor: pointer;
#             transition: all 0.3s ease;
#             text-align: center;
#             position: relative;
#             overflow: hidden;
#         }
#         .decade-option:before {
#             content: '';
#             position: absolute;
#             top: 0;
#             left: -100%;
#             width: 100%;
#             height: 100%;
#             background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
#             transition: left 0.5s ease;
#         }
#         .decade-option:hover:before {
#             left: 100%;
#         }
#         .decade-option:hover {
#             background: rgba(50, 50, 70, 0.8);
#             border-color: rgba(212, 175, 55, 0.5);
#             transform: translateY(-3px);
#         }
#         .decade-option.selected {
#             border-color: #d4af37;
#             background: rgba(40, 35, 25, 0.7);
#             box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
#         }
#         .decade-option h3 {
#             margin-bottom: 8px;
#             font-size: 1.1em;
#             color: #f0f0f0;
#             font-weight: 500;
#         }
#         .decade-option p {
#             font-size: 0.85em;
#             color: #cccccc;
#         }
#         .customization-panel {
#             display: none;
#             background: rgba(30, 30, 46, 0.8);
#             border-radius: 15px;
#             padding: 25px;
#             margin-top: 25px;
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             max-height: 500px;
#             overflow-y: auto;
#             box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2);
#         }
#         .customization-panel.active { display: block; }
#         .custom-group {
#             margin-bottom: 20px;
#             padding-bottom: 15px;
#             border-bottom: 1px solid rgba(255, 255, 255, 0.05);
#         }
#         .custom-group:last-child {
#             border-bottom: none;
#         }
#         .custom-group label {
#             display: block;
#             margin-bottom: 8px;
#             font-weight: 500;
#             font-size: 0.95em;
#             color: #f0f0f0;
#         }
#         .custom-input {
#             width: 100%;
#             padding: 10px 15px;
#             border-radius: 8px;
#             border: 1px solid rgba(255, 255, 255, 0.2);
#             background: rgba(20, 20, 30, 0.7);
#             color: #f0f0f0;
#             font-size: 14px;
#             transition: all 0.3s ease;
#         }
#         .custom-input:focus {
#             outline: none;
#             border-color: #d4af37;
#             box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
#         }
#         .custom-input::placeholder { color: #888888; }
#         .slider-container {
#             display: flex;
#             align-items: center;
#             gap: 15px;
#             margin-top: 8px;
#         }
#         .slider-container span {
#             color: #cccccc;
#             font-size: 0.9em;
#         }
#         .slider {
#             flex: 1;
#             height: 6px;
#             border-radius: 3px;
#             background: rgba(255, 255, 255, 0.1);
#             outline: none;
#             -webkit-appearance: none;
#         }
#         .slider::-webkit-slider-thumb {
#             -webkit-appearance: none;
#             appearance: none;
#             width: 18px;
#             height: 18px;
#             border-radius: 50%;
#             background: #d4af37;
#             cursor: pointer;
#             box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
#         }
#         .slider::-moz-range-thumb {
#             width: 18px;
#             height: 18px;
#             border-radius: 50%;
#             background: #d4af37;
#             cursor: pointer;
#             border: none;
#             box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
#         }
#         .checkbox-container {
#             display: flex;
#             align-items: center;
#             gap: 10px;
#             margin-top: 8px;
#         }
#         .checkbox-container input[type="checkbox"] {
#             width: 18px;
#             height: 18px;
#             accent-color: #d4af37;
#         }
#         .checkbox-container label {
#             color: #f0f0f0;
#             margin-bottom: 0;
#         }
#         .select-container {
#             margin-top: 8px;
#         }
#         .custom-select {
#             width: 100%;
#             padding: 10px 15px;
#             border-radius: 8px;
#             border: 1px solid rgba(255, 255, 255, 0.2);
#             background: rgba(20, 20, 30, 0.7);
#             color: #f0f0f0;
#             font-size: 14px;
#             transition: all 0.3s ease;
#         }
#         .custom-select:focus {
#             outline: none;
#             border-color: #d4af37;
#             box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
#         }
#         .custom-select option {
#             background: #1a1a2e;
#             color: #f0f0f0;
#         }
#         .slider-value {
#             min-width: 45px;
#             text-align: center;
#             font-weight: bold;
#             background: rgba(212, 175, 55, 0.2);
#             padding: 4px 8px;
#             border-radius: 4px;
#             font-size: 0.9em;
#             color: #d4af37;
#         }
#         .process-btn {
#             background: linear-gradient(45deg, #1a1a2e, #d4af37);
#             border: none;
#             border-radius: 50px;
#             padding: 15px 40px;
#             font-size: 1.1em;
#             font-weight: bold;
#             color: #f0f0f0;
#             cursor: pointer;
#             width: 100%;
#             margin-top: 20px;
#             transition: all 0.3s ease;
#             position: relative;
#             overflow: hidden;
#             letter-spacing: 1px;
#         }
#         .process-btn:before {
#             content: '';
#             position: absolute;
#             top: 0;
#             left: -100%;
#             width: 100%;
#             height: 100%;
#             background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
#             transition: left 0.5s ease;
#         }
#         .process-btn:hover:before {
#             left: 100%;
#         }
#         .process-btn:hover {
#             transform: translateY(-3px);
#             box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);
#         }
#         .process-btn:disabled {
#             opacity: 0.6;
#             cursor: not-allowed;
#             transform: none;
#             background: #444444;
#         }
#         .process-btn:disabled:hover {
#             box-shadow: none;
#         }
#         .video-preview {
#             width: 100%;
#             max-width: 600px;
#             border-radius: 15px;
#             margin: 20px auto;
#             display: block;
#             background: #000000;
#             box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
#         }
#         .download-btn {
#             background: linear-gradient(45deg, #1a1a2e, #2e8b57);
#             border: none;
#             border-radius: 50px;
#             padding: 12px 30px;
#             color: #f0f0f0;
#             text-decoration: none;
#             display: inline-block;
#             margin-top: 15px;
#             transition: all 0.3s ease;
#             font-weight: 500;
#             letter-spacing: 1px;
#         }
#         .download-btn:hover {
#             transform: translateY(-3px);
#             box-shadow: 0 10px 20px rgba(46, 139, 87, 0.3);
#         }
#         .hidden { display: none; }
#         .progress-bar {
#             width: 100%;
#             height: 8px;
#             background: rgba(255, 255, 255, 0.1);
#             border-radius: 4px;
#             overflow: hidden;
#             margin: 15px 0;
#             box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
#         }
#         .progress-fill {
#             height: 100%;
#             background: linear-gradient(90deg, #d4af37, #b8860b);
#             width: 0%;
#             transition: width 0.3s ease;
#             border-radius: 4px;
#         }
#         .customization-header {
#             display: flex;
#             align-items: center;
#             gap: 10px;
#             margin-bottom: 20px;
#             padding-bottom: 15px;
#             border-bottom: 1px solid rgba(212, 175, 55, 0.3);
#         }
#         .customization-header h3 {
#             color: #f0f0f0;
#             font-weight: 400;
#         }
#         .customization-header span {
#             color: #cccccc;
#         }
#         .decade-badge {
#             background: linear-gradient(45deg, #d4af37, #b8860b);
#             padding: 4px 12px;
#             border-radius: 20px;
#             font-size: 0.8em;
#             font-weight: bold;
#             color: #1a1a2e;
#         }
#         #fileInfo {
#             margin-top: 15px;
#             padding: 15px;
#             background: rgba(40, 40, 60, 0.5);
#             border-radius: 8px;
#             border: 1px solid rgba(212, 175, 55, 0.3);
#         }
#         #fileInfo p {
#             color: #f0f0f0;
#         }
#         #statusText {
#             color: #d4af37;
#             text-align: center;
#             margin-top: 15px;
#             font-size: 1.1em;
#         }
#         .era-indicator {
#             display: inline-block;
#             width: 12px;
#             height: 12px;
#             border-radius: 50%;
#             margin-right: 8px;
#         }
#         .era-1900s { background: #8B4513; }
#         .era-1910s { background: #2F4F4F; }
#         .era-1920s { background: #000000; }
#         .era-1930s { background: #FFD700; }
#         .era-1940s { background: #696969; }
#         .era-1950s { background: #FF69B4; }
#         .era-1960s { background: #FF4500; }
#         .era-1970s { background: #DA70D6; }
#         .era-1980s { background: #00CED1; }
#         .era-1990s { background: #32CD32; }
#
#         /* 响应式设计 */
#         @media (max-width: 768px) {
#             .container {
#                 padding: 10px;
#             }
#             .header h1 {
#                 font-size: 2.2em;
#             }
#             .decade-grid {
#                 grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
#             }
#             .section {
#                 padding: 20px;
#             }
#         }
#
#         /* 滚动条样式 */
#         .customization-panel::-webkit-scrollbar {
#             width: 8px;
#         }
#         .customization-panel::-webkit-scrollbar-track {
#             background: rgba(255, 255, 255, 0.05);
#             border-radius: 4px;
#         }
#         .customization-panel::-webkit-scrollbar-thumb {
#             background: rgba(212, 175, 55, 0.5);
#             border-radius: 4px;
#         }
#         .customization-panel::-webkit-scrollbar-thumb:hover {
#             background: rgba(212, 175, 55, 0.7);
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>时光影像 - 复古视频滤镜</h1>
#             <p class="subtitle">让现代视频穿越时光，重现经典年代风貌</p>
#             <p><small>从1900年代默片到1990年代家庭录像，重现每个时代的独特影像风格</small></p>
#         </div>
#
#         <div class="section">
#             <h2>上传视频</h2>
#             <div class="upload-area" id="uploadArea">
#                 <div class="upload-icon">📽️</div>
#                 <p>拖放视频文件到此处，或点击浏览</p>
#                 <p><small>支持 MP4, MOV, AVI, WebM 等常见格式</small></p>
#                 <input type="file" id="fileInput" accept="video/*" style="display: none;">
#             </div>
#             <div id="fileInfo" class="hidden">
#                 <p><strong>已选择:</strong> <span id="fileName"></span></p>
#             </div>
#         </div>
#
#         <div class="section">
#             <h2>选择年代风格</h2>
#             <div class="decade-grid" id="decadeGrid">
#                 <!-- 年代选项将通过JavaScript填充 -->
#             </div>
#
#             <!-- 所有年代的自定义设置面板 -->
#             <div class="customization-panel" id="customizationPanel">
#                 <div class="customization-header">
#                     <h3>自定义</h3>
#                     <span class="decade-badge" id="selectedDecadeBadge">1980年代</span>
#                     <span>滤镜参数</span>
#                 </div>
#                 <div id="customizationOptions">
#                     <!-- 动态自定义选项将在这里填充 -->
#                 </div>
#             </div>
#
#             <button class="process-btn" id="processBtn" disabled>应用年代滤镜</button>
#
#             <div class="progress-bar hidden" id="progressBar">
#                 <div class="progress-fill" id="progressFill"></div>
#             </div>
#             <p id="statusText"></p>
#         </div>
#
#         <div class="section hidden" id="resultSection">
#             <h2>时光穿梭后的视频</h2>
#             <video class="video-preview" id="processedVideo" controls></video>
#             <div style="text-align: center;">
#                 <a class="download-btn" id="downloadBtn" download>下载复古视频</a>
#             </div>
#         </div>
#     </div>
#
#     <script>
#         // 注意：所有JavaScript代码和变量名保持不变
#         // 只修改了显示文本，以适应中文语境
#
#         let selectedFile = null;
#         let selectedDecade = '1980s';
#
#         const decades = {
#             '1900s': { name: '1900年代 - 早期电影', desc: '手摇摄像机，复古棕褐色调' },
#             '1910s': { name: '1910年代 - 默片时代', desc: '卓别林时代，闪烁效果' },
#             '1920s': { name: '1920年代 - 爵士时代', desc: '装饰艺术风格，高对比度黑白' },
#             '1930s': { name: '1930年代 - 黄金时代', desc: '早期有声电影，柔焦效果' },
#             '1940s': { name: '1940年代 - 战争时期', desc: '黑色电影，戏剧性阴影' },
#             '1950s': { name: '1950年代 - 彩色电影', desc: '早期彩色电影，饱和色彩' },
#             '1960s': { name: '1960年代 - 柯达克罗姆', desc: '鲜艳色彩，胶片质感' },
#             '1970s': { name: '1970年代 - 超8毫米', desc: '家庭电影，温暖色调' },
#             '1980s': { name: '1980年代 - VHS录像', desc: '扫描线，色彩溢出' },
#             '1990s': { name: '1990年代 - 摄像机', desc: '数字伪影，日期戳' }
#         };
#
#         // 增强的年代配置与自定义选项
#         const decadeConfigs = {
#             '1900s': {
#                 sepia_intensity: { min: 0.5, max: 1.5, default: 1.0, label: '棕褐色强度' },
#                 scratches_level: { min: 30, max: 70, default: 50, label: '胶片划痕' },
#                 vignette_strength: { min: 0.3, max: 1.0, default: 0.7, label: '暗角效果' },
#                 flicker_enabled: { enabled: true, label: '胶片闪烁效果' },
#                 frame_rate: { min: 8, max: 18, default: 12, label: '播放速度 (帧/秒)' }
#             },
#             '1910s': {
#                 contrast_level: { min: 1.0, max: 2.0, default: 1.35, label: '胶片对比度' },
#                 grain_intensity: { min: 20, max: 60, default: 40, label: '胶片颗粒' },
#                 flicker_enabled: { enabled: true, label: '默片闪烁效果' },
#                 title_card_enabled: { enabled: false, label: '添加标题卡片' },
#                 title_card_text: { default: '默片时代', label: '标题卡片文字' }
#             },
#             '1920s': {
#                 contrast_boost: { min: 1.1, max: 1.8, default: 1.3, label: '装饰艺术对比度' },
#                 grain_level: { min: 15, max: 50, default: 35, label: '胶片颗粒' },
#                 vignette_style: { options: ['classic', 'art_deco', 'none'], default: 'classic', label: '暗角风格' },
#                 glamour_glow: { enabled: false, label: '好莱坞魅力光晕' }
#             },
#             '1930s': {
#                 soft_focus: { min: 0.2, max: 1.5, default: 0.5, label: '柔焦强度' },
#                 dramatic_lighting: { min: 0.8, max: 1.5, default: 1.25, label: '戏剧性对比度' },
#                 film_quality: { min: 10, max: 40, default: 25, label: '胶片质感' },
#                 golden_tone: { enabled: false, label: '淡金色调' }
#             },
#             '1940s': {
#                 noir_contrast: { min: 1.2, max: 2.0, default: 1.4, label: '黑色电影对比度' },
#                 shadow_depth: { min: -0.3, max: 0.1, default: 0.0, label: '阴影强度' },
#                 film_grain: { min: 10, max: 35, default: 20, label: '战时胶片质感' },
#                 cigarette_haze: { enabled: false, label: '烟雾氛围效果' }
#             },
#             '1950s': {
#                 technicolor_saturation: { min: 1.0, max: 2.0, default: 1.3, label: '彩色饱和度' },
#                 color_shift: { min: -10, max: 15, default: 5, label: '色温偏移' },
#                 film_grain: { min: 8, max: 30, default: 18, label: '彩色胶片颗粒' },
#                 vibrant_reds: { enabled: true, label: '增强红色通道' },
#                 golden_glow: { enabled: false, label: '好莱坞金色光晕' }
#             },
#             '1960s': {
#                 kodachrome_look: { min: 1.0, max: 1.8, default: 1.2, label: '柯达克罗姆饱和度' },
#                 warm_tone: { min: -8, max: 5, default: -3, label: '暖色调' },
#                 film_texture: { min: 5, max: 25, default: 15, label: '胶片纹理' },
#                 psychedelic_boost: { enabled: false, label: '迷幻色彩增强' },
#                 fade_edges: { enabled: false, label: '复古照片褪色边缘' }
#             },
#             '1970s': {
#                 super8_grain: { min: 10, max: 40, default: 22, label: '超8毫米颗粒' },
#                 warm_vintage: { min: -15, max: 0, default: -8, label: '复古暖色调' },
#                 home_movie_feel: { min: 0.7, max: 1.2, default: 0.9, label: '家庭电影饱和度' },
#                 light_leaks: { enabled: false, label: '漏光效果' },
#                 handheld_shake: { enabled: false, label: '手持摄像机抖动' }
#             },
#             '1980s': {
#                 static_level: { min: 5, max: 25, default: 12, label: 'VHS静电干扰' },
#                 color_bleeding: { min: 1.0, max: 1.8, default: 1.25, label: '色彩溢出' },
#                 timestamp_enabled: { enabled: true, label: 'VHS时间戳' },
#                 timestamp_text: { default: '1985/12/25 14:30', label: '自定义时间戳' },
#                 scanlines_enabled: { enabled: true, label: 'VHS扫描线' },
#                 tracking_issues: { enabled: false, label: '磁迹跟踪问题' }
#             },
#             '1990s': {
#                 digital_noise: { min: 3, max: 15, default: 8, label: '数字伪影' },
#                 camcorder_saturation: { min: 0.9, max: 1.4, default: 1.1, label: '摄像机色彩' },
#                 timestamp_enabled: { enabled: true, label: '数字日期戳' },
#                 timestamp_text: { default: '1995/12/25 14:30:45', label: '自定义日期/时间' },
#                 auto_focus_enabled: { enabled: true, label: '自动对焦搜索' },
#                 zoom_artifacts: { enabled: false, label: '数字缩放伪影' }
#             }
#         };
#
#         // 填充年代网格
#         const decadeGrid = document.getElementById('decadeGrid');
#         Object.entries(decades).forEach(([decade, info]) => {
#             const option = document.createElement('div');
#             option.className = `decade-option ${decade === '1980s' ? 'selected' : ''}`;
#             option.dataset.decade = decade;
#             option.innerHTML = `
#                 <span class="era-indicator era-${decade}"></span>
#                 <h3>${info.name}</h3>
#                 <p>${info.desc}</p>
#             `;
#             decadeGrid.appendChild(option);
#
#             option.addEventListener('click', () => {
#                 document.querySelectorAll('.decade-option').forEach(o => o.classList.remove('selected'));
#                 option.classList.add('selected');
#                 selectedDecade = decade;
#                 updateCustomizationPanel();
#             });
#         });
#
#         // 文件上传处理
#         const uploadArea = document.getElementById('uploadArea');
#         const fileInput = document.getElementById('fileInput');
#         const fileInfo = document.getElementById('fileInfo');
#         const fileName = document.getElementById('fileName');
#         const processBtn = document.getElementById('processBtn');
#
#         uploadArea.addEventListener('click', () => fileInput.click());
#         uploadArea.addEventListener('dragover', (e) => {
#             e.preventDefault();
#             uploadArea.style.background = 'rgba(50, 50, 70, 0.8)';
#         });
#         uploadArea.addEventListener('dragleave', () => {
#             uploadArea.style.background = '';
#         });
#         uploadArea.addEventListener('drop', (e) => {
#             e.preventDefault();
#             uploadArea.style.background = '';
#             const files = e.dataTransfer.files;
#             if (files.length > 0 && files[0].type.startsWith('video/')) {
#                 handleFileSelection(files[0]);
#             }
#         });
#
#         fileInput.addEventListener('change', (e) => {
#             const file = e.target.files[0];
#             if (file && file.type.startsWith('video/')) {
#                 handleFileSelection(file);
#             }
#         });
#
#         function handleFileSelection(file) {
#             selectedFile = file;
#             fileName.textContent = file.name;
#             fileInfo.classList.remove('hidden');
#             processBtn.disabled = false;
#         }
#
#         // 增强的自定义面板
#         function updateCustomizationPanel() {
#             const panel = document.getElementById('customizationPanel');
#             const badge = document.getElementById('selectedDecadeBadge');
#             const optionsContainer = document.getElementById('customizationOptions');
#
#             // 更新年代徽章文本
#             const decadeTextMap = {
#                 '1900s': '1900年代',
#                 '1910s': '1910年代',
#                 '1920s': '1920年代',
#                 '1930s': '1930年代',
#                 '1940s': '1940年代',
#                 '1950s': '1950年代',
#                 '1960s': '1960年代',
#                 '1970s': '1970年代',
#                 '1980s': '1980年代',
#                 '1990s': '1990年代'
#             };
#
#             badge.textContent = decadeTextMap[selectedDecade] || selectedDecade;
#             panel.classList.add('active');
#
#             // 清除现有选项
#             optionsContainer.innerHTML = '';
#
#             // 获取选定年代的配置
#             const config = decadeConfigs[selectedDecade];
#             if (!config) return;
#
#             // 动态生成选项
#             Object.entries(config).forEach(([optionKey, optionConfig]) => {
#                 const groupDiv = document.createElement('div');
#                 groupDiv.className = 'custom-group';
#
#                 if (optionConfig.min !== undefined && optionConfig.max !== undefined) {
#                     // 滑块输入
#                     groupDiv.innerHTML = `
#                         <label for="${optionKey}">${optionConfig.label}</label>
#                         <div class="slider-container">
#                             <span>低</span>
#                             <input type="range" id="${optionKey}" class="slider"
#                                    min="${optionConfig.min}" max="${optionConfig.max}"
#                                    value="${optionConfig.default}" step="0.1">
#                             <span>高</span>
#                             <span class="slider-value" id="${optionKey}_value">${optionConfig.default}</span>
#                         </div>
#                     `;
#
#                     // 为滑块添加事件监听器
#                     setTimeout(() => {
#                         const slider = document.getElementById(optionKey);
#                         const valueSpan = document.getElementById(`${optionKey}_value`);
#                         slider.addEventListener('input', (e) => {
#                             valueSpan.textContent = parseFloat(e.target.value).toFixed(1);
#                         });
#                     }, 0);
#
#                 } else if (optionConfig.options) {
#                     // 选择下拉菜单
#                     const optionsHtml = optionConfig.options.map(opt =>
#                         `<option value="${opt}" ${opt === optionConfig.default ? 'selected' : ''}>${opt.replace('_', ' ').toUpperCase()}</option>`
#                     ).join('');
#
#                     groupDiv.innerHTML = `
#                         <label for="${optionKey}">${optionConfig.label}</label>
#                         <div class="select-container">
#                             <select id="${optionKey}" class="custom-select">
#                                 ${optionsHtml}
#                             </select>
#                         </div>
#                     `;
#
#                 } else if (optionConfig.enabled !== undefined) {
#                     // 复选框
#                     groupDiv.innerHTML = `
#                         <div class="checkbox-container">
#                             <input type="checkbox" id="${optionKey}" ${optionConfig.enabled ? 'checked' : ''}>
#                             <label for="${optionKey}">${optionConfig.label}</label>
#                         </div>
#                     `;
#
#                 } else if (optionConfig.default !== undefined && typeof optionConfig.default === 'string') {
#                     // 文本输入
#                     groupDiv.innerHTML = `
#                         <label for="${optionKey}">${optionConfig.label}</label>
#                         <input type="text" id="${optionKey}" class="custom-input"
#                                value="${optionConfig.default}" placeholder="${optionConfig.label}">
#                     `;
#                 }
#
#                 optionsContainer.appendChild(groupDiv);
#             });
#         }
#
#         // 收集自定义选项
#         function getCustomOptions() {
#             const config = decadeConfigs[selectedDecade];
#             if (!config) return null;
#
#             const customOptions = {};
#
#             Object.keys(config).forEach(optionKey => {
#                 const element = document.getElementById(optionKey);
#                 if (element) {
#                     if (element.type === 'checkbox') {
#                         customOptions[optionKey] = element.checked;
#                     } else if (element.type === 'range') {
#                         customOptions[optionKey] = parseFloat(element.value);
#                     } else {
#                         customOptions[optionKey] = element.value;
#                     }
#                 }
#             });
#
#             return customOptions;
#         }
#
#         // 处理视频
#         processBtn.addEventListener('click', async () => {
#             if (!selectedFile) return;
#
#             const progressBar = document.getElementById('progressBar');
#             const progressFill = document.getElementById('progressFill');
#             const statusText = document.getElementById('statusText');
#             const resultSection = document.getElementById('resultSection');
#
#             processBtn.disabled = true;
#             progressBar.classList.remove('hidden');
#
#             // 更新状态文本
#             const decadeTextMap = {
#                 '1900s': '1900年代',
#                 '1910s': '1910年代',
#                 '1920s': '1920年代',
#                 '1930s': '1930年代',
#                 '1940s': '1940年代',
#                 '1950s': '1950年代',
#                 '1960s': '1960年代',
#                 '1970s': '1970年代',
#                 '1980s': '1980年代',
#                 '1990s': '1990年代'
#             };
#
#             statusText.textContent = `正在应用${decadeTextMap[selectedDecade]}滤镜与自定义设置...`;
#             progressFill.style.width = '30%';
#
#             try {
#                 const formData = new FormData();
#                 formData.append('video', selectedFile);
#                 formData.append('decade', selectedDecade);
#
#                 // 添加自定义选项
#                 const customOptions = getCustomOptions();
#                 if (customOptions) {
#                     formData.append('custom_options', JSON.stringify(customOptions));
#                 }
#
#                 progressFill.style.width = '60%';
#                 statusText.textContent = '正在处理视频并添加复古效果...';
#
#                 const response = await fetch('/api/process-video', {
#                     method: 'POST',
#                     body: formData
#                 });
#
#                 if (response.ok) {
#                     progressFill.style.width = '100%';
#                     statusText.textContent = '完成！ ✨ 您的复古影像杰作已准备就绪！';
#
#                     const blob = await response.blob();
#                     const videoUrl = URL.createObjectURL(blob);
#
#                     document.getElementById('processedVideo').src = videoUrl;
#                     document.getElementById('downloadBtn').href = videoUrl;
#                     document.getElementById('downloadBtn').download = `${selectedDecade}-复古-${Date.now()}.mp4`;
#
#                     resultSection.classList.remove('hidden');
#                 } else {
#                     throw new Error('处理失败');
#                 }
#             } catch (error) {
#                 statusText.textContent = '错误: ' + error.message;
#                 progressFill.style.width = '0%';
#             }
#
#             processBtn.disabled = false;
#             setTimeout(() => {
#                 progressBar.classList.add('hidden');
#             }, 3000);
#         });
#
#         // 初始化
#         updateCustomizationPanel();
#     </script>
# </body>
# </html>
# '''
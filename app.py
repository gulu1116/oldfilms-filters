import socket
import os
import sys
import threading
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox
import requests
from flask import Flask, request, send_file, jsonify, render_template_string, render_template
from flask_cors import CORS
import subprocess
import uuid
import logging
from datetime import datetime
import json

# Add your existing filter functions here
from oldfilms_filters import get_decade_filter_config, build_filter_command, process_video_with_ffmpeg

app = Flask(__name__, template_folder='templates', static_folder='static')  # 添加模板和静态文件配置
CORS(app)

# Disable Flask logging for cleaner output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm', 'mkv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add this helper function to get local IP
def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to determine IP"

# Your existing Flask routes
@app.route('/')
def index():
    return render_template('index.html')  # 使用模板文件

@app.route('/api/process-video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    decade = request.form.get('decade', '1980s')
    custom_options_json = request.form.get('custom_options')
    
    custom_options = None
    if custom_options_json:
        try:
            custom_options = json.loads(custom_options_json)
        except:
            pass
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    file_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    input_filename = f"{timestamp}_{file_id}_input.mp4"
    output_filename = f"{timestamp}_{file_id}_{decade}_output.mp4"
    
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)
    
    file.save(input_path)
    
    success, message = process_video_with_ffmpeg(input_path, output_path, decade, custom_options)
    
    if not success:
        return jsonify({'error': message}), 500
    
    return send_file(
        output_path, 
        as_attachment=True, 
        download_name=f'{decade}-vintage-{timestamp}.mp4'
    )

@app.route('/api/decades', methods=['GET'])
def get_decades():
    return jsonify(get_decade_filter_config())

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown endpoint for clean app exit"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

class RetroVideoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Old Films Filters")
        self.root.geometry("400x450")  # Increased height for mobile features
        self.root.resizable(False, False)
        
        # Set icon if available
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.server_thread = None
        self.server_running = False
        self.local_ip = None
        
        self.setup_ui()
        self.check_ffmpeg()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Old Films Filters",
            font=("Arial", 24, "bold"),
            fg='#4ecdc4',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            main_frame, 
            text="Video Filters 视频滤镜工具",
            font=("Arial", 18),
            fg='#ffd93d',
            bg='#1a1a1a'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Description
        desc_text = "为你的视频一键添加复古滤镜\n重现1900s-1990s的经典影像风格！"
        desc_label = tk.Label(
            main_frame, 
            text=desc_text, 
            font=("Arial", 10),
            fg='#ffffff',
            bg='#1a1a1a',
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))
        
        # Launch button
        self.launch_btn = tk.Button(
            main_frame,
            text="🎬 Launch Video Editor",
            font=("Arial", 14, "bold"),
            bg='#4ecdc4',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.launch_app
        )
        self.launch_btn.pack(pady=10)
        
        # Mobile access frame
        mobile_frame = tk.Frame(main_frame, bg='#1a1a1a')
        mobile_frame.pack(pady=(15, 0), fill=tk.X)
        
        mobile_label = tk.Label(
            mobile_frame,
            text="📱 Connect Your Phone:",
            font=("Arial", 10, "bold"),
            fg='#4ecdc4',
            bg='#1a1a1a'
        )
        mobile_label.pack()
        
        self.ip_label = tk.Label(
            mobile_frame,
            text="Start the app to see mobile URL",
            font=("Arial", 9),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        self.ip_label.pack(pady=(5, 0))
        
        # Copy IP button (initially hidden)
        self.copy_ip_btn = tk.Button(
            mobile_frame,
            text="📋 Copy Mobile URL",
            font=("Arial", 9),
            bg='#666666',
            fg='white',
            relief=tk.FLAT,
            padx=10,
            pady=3,
            command=self.copy_ip_to_clipboard,
            state=tk.DISABLED
        )
        self.copy_ip_btn.pack(pady=(5, 0))
        
        # QR Code button (initially hidden)
        self.qr_btn = tk.Button(
            mobile_frame,
            text="📱 Show QR Code",
            font=("Arial", 9),
            bg='#666666',
            fg='white',
            relief=tk.FLAT,
            padx=10,
            pady=3,
            command=self.show_qr_code,
            state=tk.DISABLED
        )
        self.qr_btn.pack(pady=(3, 0))
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to launch",
            font=("Arial", 9),
            fg='#888888',
            bg='#1a1a1a'
        )
        self.status_label.pack(pady=(15, 0))
        
        # Exit button
        exit_btn = tk.Button(
            main_frame,
            text="Exit",
            font=("Arial", 10),
            bg='#666666',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            command=self.exit_app
        )
        exit_btn.pack(side=tk.BOTTOM, pady=(20, 0))
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.status_label.config(text="✅ FFmpeg detected - Ready to launch", fg='#4ecdc4')
        except:
            self.status_label.config(text="❌ FFmpeg not found! Please install FFmpeg", fg='#ff6b6b')
            self.launch_btn.config(state=tk.DISABLED)
            messagebox.showerror(
                "FFmpeg Missing",
                "FFmpeg is required but not found!\n\nPlease install FFmpeg and make sure it's in your PATH.\n\nDownload from: https://ffmpeg.org/download.html"
            )
    
    def start_flask_server(self):
        """Start Flask server in background thread"""
        try:
            # Allow connections from any device on the network
            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        except:
            pass
    
    def launch_app(self):
        """Launch the web application"""
        if not self.server_running:
            self.status_label.config(text="🚀 Starting server...", fg='#ffd93d')
            self.launch_btn.config(state=tk.DISABLED, text="Starting...")
            
            # Start Flask server in background
            self.server_thread = threading.Thread(target=self.start_flask_server, daemon=True)
            self.server_thread.start()
            
            # Wait a moment for server to start
            self.root.after(2000, self.open_browser)
    
    def open_browser(self):
        """Open browser to the application"""
        try:
            # Test if server is running
            response = requests.get('http://127.0.0.1:5000', timeout=5)
            if response.status_code == 200:
                # Get local IP for mobile access
                self.local_ip = get_local_ip()
                
                # Open browser
                webbrowser.open('http://127.0.0.1:5000')
                self.server_running = True
                self.status_label.config(text="🎬 App running in browser", fg='#4ecdc4')
                self.launch_btn.config(text="🌐 Open in Browser", state=tk.NORMAL)
                self.launch_btn.config(command=lambda: webbrowser.open('http://127.0.0.1:5000'))
                
                # Update mobile access info
                if self.local_ip != "Unable to determine IP":
                    mobile_url = f"http://{self.local_ip}:5000"
                    self.ip_label.config(
                        text=f"Open on phone: {mobile_url}",
                        fg='#4ecdc4'
                    )
                    self.copy_ip_btn.config(state=tk.NORMAL, bg='#4ecdc4')
                    self.qr_btn.config(state=tk.NORMAL, bg='#4ecdc4')
                else:
                    self.ip_label.config(
                        text="Unable to determine network IP",
                        fg='#ff6b6b'
                    )
            else:
                raise Exception("Server not responding")
        except:
            self.status_label.config(text="❌ Failed to start server", fg='#ff6b6b')
            self.launch_btn.config(text="🎬 Launch Video Editor", state=tk.NORMAL)
            messagebox.showerror("Error", "Failed to start the application server.")
    
    def copy_ip_to_clipboard(self):
        """Copy the mobile URL to clipboard"""
        if self.local_ip:
            mobile_url = f"http://{self.local_ip}:5000"
            self.root.clipboard_clear()
            self.root.clipboard_append(mobile_url)
            self.root.update()  # Required for clipboard update
            
            # Show feedback
            original_text = self.copy_ip_btn.cget("text")
            self.copy_ip_btn.config(text="✅ Copied!", bg='#2ecc71')
            self.root.after(2000, lambda: self.copy_ip_btn.config(text=original_text, bg='#4ecdc4'))
    
    def show_qr_code(self):
        """Show QR code for easy mobile scanning"""
        if not self.local_ip:
            return
            
        try:
            import qrcode
            from PIL import Image, ImageTk
            
            # Generate QR code
            mobile_url = f"http://{self.local_ip}:5000"
            qr = qrcode.QRCode(version=1, box_size=8, border=5)
            qr.add_data(mobile_url)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((200, 200))
            
            # Create popup window
            qr_window = tk.Toplevel(self.root)
            qr_window.title("QR Code - Scan with Phone")
            qr_window.geometry("250x280")
            qr_window.resizable(False, False)
            qr_window.configure(bg='white')
            
            # Convert PIL image to Tkinter
            qr_photo = ImageTk.PhotoImage(qr_img)
            
            # Display QR code
            qr_label = tk.Label(qr_window, image=qr_photo, bg='white')
            qr_label.image = qr_photo  # Keep a reference
            qr_label.pack(pady=10)
            
            # Instructions
            instruction_label = tk.Label(
                qr_window,
                text=f"Scan with phone camera\n{mobile_url}",
                font=("Arial", 9),
                bg='white',
                justify=tk.CENTER
            )
            instruction_label.pack(pady=(0, 10))
            
        except ImportError:
            # QR code library not available, show simple dialog
            messagebox.showinfo(
                "Mobile Access",
                f"Connect your phone to the same WiFi network and open:\n\n{self.local_ip}:5000\n\nMake sure both devices are on the same network!"
            )
    
    def exit_app(self):
        """Clean exit"""
        if self.server_running:
            try:
                requests.post('http://127.0.0.1:5000/shutdown', timeout=2)
            except:
                pass
        
        self.root.quit()
        self.root.destroy()
        sys.exit()
    
    def run(self):
        """Start the desktop application"""
        self.root.mainloop()

if __name__ == '__main__':
    # Check if running as compiled executable
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        application_path = sys._MEIPASS
        os.chdir(application_path)
    
    app_instance = RetroVideoApp()
    app_instance.run()
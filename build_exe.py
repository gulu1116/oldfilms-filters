# build_exe.py - Robust PyInstaller build script for Windows
import PyInstaller.__main__
import os
import sys
import shutil

def build_executable():
    """Build the standalone executable with correct paths on Windows"""

    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Get absolute project directory
    source_dir = os.path.dirname(os.path.abspath(__file__))

    # 新增：检查并确保必要的目录存在
    required_dirs = ['templates', 'static', 'uploads', 'processed']
    for dir_name in required_dirs:
        dir_path = os.path.join(source_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"创建缺失的目录: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)

    # Resolve and normalize oldfilms_filters.py path
    oldfilms_filters_path = os.path.join(source_dir, "oldfilms_filters.py")
    if not os.path.exists(oldfilms_filters_path):
        print(f"ERROR: oldfilms_filters.py not found at {oldfilms_filters_path}")
        return False

    # Convert Windows backslashes to forward slashes for PyInstaller
    oldfilms_filters_path = oldfilms_filters_path.replace("\\", "/")

    # Base PyInstaller arguments
    args = [
        os.path.join(source_dir, 'app.py').replace("\\", "/"),
        '--name=OldFilmsFilters',
        '--onefile',
        '--windowed',
        f'--add-data={oldfilms_filters_path};.',
        # 修改：使用绝对路径来确保PyInstaller能找到目录
        f'--add-data={os.path.join(source_dir, "templates")};templates',
        f'--add-data={os.path.join(source_dir, "static")};static',
        f'--add-data={os.path.join(source_dir, "uploads")};uploads',
        f'--add-data={os.path.join(source_dir, "processed")};processed',
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=tkinter',
        '--hidden-import=requests',
        '--collect-all=flask',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=./build',
        '--clean',
    ]

    # Add icon if it exists
    icon_path = os.path.join(source_dir, 'icon.ico')
    if os.path.exists(icon_path):
        # 提前处理路径的斜杠替换，再传入参数
        modified_icon_path = icon_path.replace("\\", "/")
        args.extend(['--icon', modified_icon_path])

    # Detect FFmpeg on PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        # 提前处理FFmpeg路径的斜杠替换
        modified_ffmpeg_path = ffmpeg_path.replace("\\", "/")
        args.extend([f'--add-binary={modified_ffmpeg_path};.'])
        print(f"Including bundled FFmpeg from: {ffmpeg_path}")
    else:
        print("FFmpeg not found - users will need to install it separately")

    print("Building executable...")
    print("Arguments:", ' '.join(args))
    print("Arguments:", ' '.join(args))

    try:
        PyInstaller.__main__.run(args)
        print("Build completed successfully!")
    except Exception as e:
        print(f"Build failed: {e}")
        return False

    return True


if __name__ == '__main__':
    success = build_executable()

    if success:
        print("\nSUCCESS. Your executable is ready.")
    else:
        print("\nBuild failed. Check the error messages above.")
        sys.exit(1)

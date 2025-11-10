
# OldFilms Filters — 复古影像滤镜系统

## 一、项目简介

**OldFilms Filters** 是基于 Python + Flask + FFmpeg 的本地化复古视频滤镜处理系统。作为数字图像处理课程的大作业，旨在实现一个可本地运行的“复古风格视频滤镜”系统。  

用户可通过浏览器上传视频，并选择不同年代的复古滤镜进行处理。系统无需联网或订阅，完全本地运行，轻量、安全且易用。

**特点：**
- 🧩 **完全离线运行**：无需联网，无第三方接口依赖。
- 🕰️ **年代风格滤镜**：支持不同时代的视频复古化效果。
- 🖥️ **多端访问**：可在电脑端或手机浏览器访问。
- ⚙️ **FFmpeg 加速处理**：结合算法与 FFmpeg 实现高效视频转换。
- 🎨 **复古简约界面**：以深色调与动态细节营造沉稳典雅的交互体验。

## 二、系统结构

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   桌面启动程序   │◄──►│   Flask 本地服务  │◄──►│   Web 前端界面   │
│   (Tkinter)     │    │   (Python)      │    │  (HTML/CSS/JS)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │            ┌────────────────────┐             │
         └───────────►│  滤镜算法核心模块  │◄────────────┘
                      │ (oldfilms_filters) │
                      └────────────────────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │   FFmpeg 引擎    │
                      │   (外部程序)     │
                      └──────────────────┘
```

**项目目录结构**

```
oldfilms-filters/
├── app.py                 # 主应用程序
├── oldfilms_filters.py    # 核心滤镜算法
├── build_exe.py           # 打包构建脚本
├── requirements.txt       # Python依赖列表
├── templates/             # Web模板
│   └── index.html         # 主界面
├── static/                # 静态资源
│   ├── css/style.css      # 样式表
│   └── js/app.js          # 前端逻辑
├── uploads/               # 上传文件存储
├── processed/             # 处理结果输出
└── README.md              # 项目文档
```

**模块说明**

|模块|功能描述|
|---|---|
|**app.py**|启动 Flask 服务，处理上传与前端交互|
|**oldfilms_filters.py**|定义复古滤镜算法与图像处理逻辑|
|**app.js / style.css / index.html**|提供网页端交互与样式界面|
|**build_exe.py**|调用 PyInstaller 打包为独立可执行程序|

## 三、运行流程

1. 用户在网页界面选择视频与目标年代
2. Flask 服务器调用 `oldfilms_filters.py` 获取对应滤镜参数
3. 构建 FFmpeg 命令并执行视频处理
4. 输出复古风格视频至 `processed/` 文件夹
5. 用户可直接下载或预览生成结果


## 四、环境配置与运行

### 1️. 环境准备

确保 Windows 系统已安装以下组件：
- **Python 3.8+**
- **FFmpeg**（需加入系统 PATH）
- **Git**（可选，用于项目分发）

### 2️. 克隆与安装依赖

```bash
git clone https://github.com/gulu1116/oldfilms-filters.git
cd oldfilms-filters

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3️. 启动本地服务

```bash
python app.py
```

在浏览器中访问：  `http://127.0.0.1:5000`
即可进入复古视频滤镜界面。


## 五、打包为可执行程序（Windows）

可使用 `PyInstaller` 生成独立的 `.exe` 文件：

```bash
# 激活虚拟环境
venv\Scripts\activate

# 执行打包脚本
python build_exe.py
```

生成的可执行文件位于：

```
dist/OldFilmsFilters.exe
```


## 六、核心算法说明

`oldfilms_filters.py` 实现了各年代滤镜的参数定义与映射逻辑，包括：

- 色彩老化（色相偏移、饱和度下降）
- 胶片颗粒噪声模拟
- 对比度与亮度复古调节
- 模拟旧时代曝光与模糊特征

所有滤镜最终通过 **FFmpeg 命令行滤镜组合** 实现，兼顾速度与画质。

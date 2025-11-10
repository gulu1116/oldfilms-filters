// =====================
// 时光影像 - 复古视频滤镜应用
// =====================

// 应用状态
let selectedFile = null;
let selectedDecade = '1980s';

// 创建动态星空背景
function createStarfield() {
    const stars = document.createElement('div');
    stars.className = 'stars';
    document.body.appendChild(stars);

    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 3 + 1 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 4 + 's';
        star.style.opacity = Math.random() * 0.7 + 0.3;
        stars.appendChild(star);
    }
}

// 年代配置
const decades = {
    '1900s': { name: '1900年代 - 早期电影', desc: '手摇摄像机，复古棕褐色调' },
    '1910s': { name: '1910年代 - 默片时代', desc: '卓别林时代，闪烁效果' },
    '1920s': { name: '1920年代 - 爵士时代', desc: '装饰艺术风格，高对比度黑白' },
    '1930s': { name: '1930年代 - 黄金时代', desc: '早期有声电影，柔焦效果' },
    '1940s': { name: '1940年代 - 战争时期', desc: '黑色电影，戏剧性阴影' },
    '1950s': { name: '1950年代 - 彩色电影', desc: '早期彩色电影，饱和色彩' },
    '1960s': { name: '1960年代 - 柯达克罗姆', desc: '鲜艳色彩，胶片质感' },
    '1970s': { name: '1970年代 - 超8毫米', desc: '家庭电影，温暖色调' },
    '1980s': { name: '1980年代 - VHS录像', desc: '扫描线，色彩溢出' },
    '1990s': { name: '1990年代 - 摄像机', desc: '数字伪影，日期戳' }
};

// 年代滤镜配置 - 与后端保持一致
const decadeConfigs = {
    '1900s': {
        'sepia_intensity': {'min': 0.5, 'max': 1.5, 'default': 1.0, 'label': '棕褐色强度'},
        'scratches_level': {'min': 30, 'max': 70, 'default': 50, 'label': '胶片划痕'},
        'vignette_strength': {'min': 0.3, 'max': 1.0, 'default': 0.7, 'label': '暗角效果'},
        'flicker_enabled': {'enabled': true, 'label': '胶片闪烁效果'},
        'frame_rate': {'min': 8, 'max': 18, 'default': 12, 'label': '播放速度 (帧/秒)'}
    },
    '1910s': {
        'contrast_level': {'min': 1.0, 'max': 2.0, 'default': 1.35, 'label': '胶片对比度'},
        'grain_intensity': {'min': 20, 'max': 60, 'default': 40, 'label': '胶片颗粒'},
        'flicker_enabled': {'enabled': true, 'label': '默片闪烁效果'},
        'title_card_enabled': {'enabled': false, 'label': '添加标题卡片'},
        'title_card_text': {'default': '默片时代', 'label': '标题卡片文字'}
    },
    '1920s': {
        'contrast_boost': {'min': 1.1, 'max': 1.8, 'default': 1.3, 'label': '装饰艺术对比度'},
        'grain_level': {'min': 15, 'max': 50, 'default': 35, 'label': '胶片颗粒'},
        'vignette_style': {'options': ['classic', 'art_deco', 'none'], 'default': 'classic', 'label': '暗角风格'},
        'glamour_glow': {'enabled': false, 'label': '好莱坞魅力光晕'}
    },
    '1930s': {
        'soft_focus': {'min': 0.2, 'max': 1.5, 'default': 0.5, 'label': '柔焦强度'},
        'dramatic_lighting': {'min': 0.8, 'max': 1.5, 'default': 1.25, 'label': '戏剧性对比度'},
        'film_quality': {'min': 10, 'max': 40, 'default': 25, 'label': '胶片质感'},
        'golden_tone': {'enabled': false, 'label': '淡金色调'}
    },
    '1940s': {
        'noir_contrast': {'min': 1.2, 'max': 2.0, 'default': 1.4, 'label': '黑色电影对比度'},
        'shadow_depth': {'min': -0.3, 'max': 0.1, 'default': 0.0, 'label': '阴影强度'},
        'film_grain': {'min': 10, 'max': 35, 'default': 20, 'label': '战时胶片质感'},
        'cigarette_haze': {'enabled': false, 'label': '烟雾氛围效果'}
    },
    '1950s': {
        'technicolor_saturation': {'min': 1.0, 'max': 2.0, 'default': 1.3, 'label': '彩色饱和度'},
        'color_shift': {'min': -10, 'max': 15, 'default': 5, 'label': '色温偏移'},
        'film_grain': {'min': 8, 'max': 30, 'default': 18, 'label': '彩色胶片颗粒'},
        'vibrant_reds': {'enabled': true, 'label': '增强红色通道'},
        'golden_glow': {'enabled': false, 'label': '好莱坞金色光晕'}
    },
    '1960s': {
        'kodachrome_look': {'min': 1.0, 'max': 1.8, 'default': 1.2, 'label': '柯达克罗姆饱和度'},
        'warm_tone': {'min': -8, 'max': 5, 'default': -3, 'label': '暖色调'},
        'film_texture': {'min': 5, 'max': 25, 'default': 15, 'label': '胶片纹理'},
        'psychedelic_boost': {'enabled': false, 'label': '迷幻色彩增强'},
        'fade_edges': {'enabled': false, 'label': '复古照片褪色边缘'}
    },
    '1970s': {
        'super8_grain': {'min': 10, 'max': 40, 'default': 22, 'label': '超8毫米颗粒'},
        'warm_vintage': {'min': -15, 'max': 0, 'default': -8, 'label': '复古暖色调'},
        'home_movie_feel': {'min': 0.7, 'max': 1.2, 'default': 0.9, 'label': '家庭电影饱和度'},
        'light_leaks': {'enabled': false, 'label': '漏光效果'},
        'handheld_shake': {'enabled': false, 'label': '手持摄像机抖动'}
    },
    '1980s': {
        'static_level': {'min': 5, 'max': 25, 'default': 12, 'label': 'VHS静电干扰'},
        'color_bleeding': {'min': 1.0, 'max': 1.8, 'default': 1.25, 'label': '色彩溢出'},
        'timestamp_enabled': {'enabled': true, 'label': 'VHS时间戳'},
        'timestamp_text': {'default': '1985/12/25 14:30', 'label': '自定义时间戳'},
        'scanlines_enabled': {'enabled': true, 'label': 'VHS扫描线'},
        'tracking_issues': {'enabled': false, 'label': '磁迹跟踪问题'}
    },
    '1990s': {
        'digital_noise': {'min': 3, 'max': 15, 'default': 8, 'label': '数字伪影'},
        'camcorder_saturation': {'min': 0.9, 'max': 1.4, 'default': 1.1, 'label': '摄像机色彩'},
        'timestamp_enabled': {'enabled': true, 'label': '数字日期戳'},
        'timestamp_text': {'default': '1995/12/25 14:30:45', 'label': '自定义日期/时间'},
        'auto_focus_enabled': {'enabled': true, 'label': '自动对焦搜索'},
        'zoom_artifacts': {'enabled': false, 'label': '数字缩放伪影'}
    }
};

// DOM 元素
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const decadeGrid = document.getElementById('decadeGrid');
const processBtn = document.getElementById('processBtn');
const progressBar = document.getElementById('progressBar');
const progressFill = document.getElementById('progressFill');
const statusText = document.getElementById('statusText');
const customizationPanel = document.getElementById('customizationPanel');
const selectedDecadeBadge = document.getElementById('selectedDecadeBadge');
const resultSection = document.getElementById('resultSection');
const processedVideo = document.getElementById('processedVideo');
const downloadBtn = document.getElementById('downloadBtn');

// 初始化年代选项
function initializeDecades() {
    Object.entries(decades).forEach(([decade, info]) => {
        const option = document.createElement('div');
        option.className = `decade-option ${decade === '1980s' ? 'selected' : ''}`;
        option.dataset.decade = decade;
        option.innerHTML = `<h3>${info.name}</h3><p>${info.desc}</p>`;
        decadeGrid.appendChild(option);

        option.addEventListener('click', () => {
            document.querySelectorAll('.decade-option').forEach(o => {
                o.classList.remove('selected');
                o.style.animation = 'none';
                setTimeout(() => {
                    o.style.animation = '';
                }, 10);
            });
            option.classList.add('selected');
            selectedDecade = decade;
            updateCustomizationPanel();

            // 添加点击动画
            option.style.animation = 'decadeCardAppear 0.6s ease-out';
        });
    });
}

// 文件上传处理
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
    uploadArea.style.background = 'rgba(50, 51, 71, 0.8)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    uploadArea.style.background = '';
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('video/')) {
        handleFileSelection(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('video/')) {
        handleFileSelection(file);
    }
});

function handleFileSelection(file) {
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.classList.remove('hidden');
    processBtn.disabled = false;

    // 添加文件选择动画
    fileInfo.style.animation = 'fileInfoSlide 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
}

// 更新自定义面板
function updateCustomizationPanel() {
    const panel = document.getElementById('customizationPanel');
    const badge = document.getElementById('selectedDecadeBadge');
    const optionsContainer = document.getElementById('customizationOptions');

    // 更新年代徽章文本
    const decadeTextMap = {
        '1900s': '1900年代',
        '1910s': '1910年代',
        '1920s': '1920年代',
        '1930s': '1930年代',
        '1940s': '1940年代',
        '1950s': '1950年代',
        '1960s': '1960年代',
        '1970s': '1970年代',
        '1980s': '1980年代',
        '1990s': '1990年代'
    };

    badge.textContent = decadeTextMap[selectedDecade] || selectedDecade;
    panel.classList.add('active');

    // 清除现有选项
    optionsContainer.innerHTML = '';

    // 获取选定年代的配置
    const config = decadeConfigs[selectedDecade];
    if (!config) return;

    // 动态生成选项
    Object.entries(config).forEach(([optionKey, optionConfig]) => {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'custom-group';

        if (optionConfig.min !== undefined && optionConfig.max !== undefined) {
            // 滑块输入
            groupDiv.innerHTML = `
                <label for="${optionKey}">${optionConfig.label}</label>
                <div class="slider-container">
                    <span>低</span>
                    <input type="range" id="${optionKey}" class="slider"
                           min="${optionConfig.min}" max="${optionConfig.max}"
                           value="${optionConfig.default}" step="0.1">
                    <span>高</span>
                    <span class="slider-value" id="${optionKey}_value">${optionConfig.default}</span>
                </div>
            `;

            // 为滑块添加事件监听器
            setTimeout(() => {
                const slider = document.getElementById(optionKey);
                const valueSpan = document.getElementById(`${optionKey}_value`);
                slider.addEventListener('input', (e) => {
                    valueSpan.textContent = parseFloat(e.target.value).toFixed(1);
                    // 添加滑块值变化动画
                    valueSpan.style.animation = 'none';
                    setTimeout(() => {
                        valueSpan.style.animation = 'badgePulse 0.3s ease';
                    }, 10);
                });
            }, 0);

        } else if (optionConfig.options) {
            // 选择下拉菜单
            const optionsHtml = optionConfig.options.map(opt =>
                `<option value="${opt}" ${opt === optionConfig.default ? 'selected' : ''}>${opt.replace('_', ' ').toUpperCase()}</option>`
            ).join('');

            groupDiv.innerHTML = `
                <label for="${optionKey}">${optionConfig.label}</label>
                <div class="select-container">
                    <select id="${optionKey}" class="custom-select">
                        ${optionsHtml}
                    </select>
                </div>
            `;

        } else if (optionConfig.enabled !== undefined) {
            // 复选框
            groupDiv.innerHTML = `
                <div class="checkbox-container">
                    <input type="checkbox" id="${optionKey}" ${optionConfig.enabled ? 'checked' : ''}>
                    <label for="${optionKey}">${optionConfig.label}</label>
                </div>
            `;

        } else if (optionConfig.default !== undefined && typeof optionConfig.default === 'string') {
            // 文本输入
            groupDiv.innerHTML = `
                <label for="${optionKey}">${optionConfig.label}</label>
                <input type="text" id="${optionKey}" class="custom-input"
                       value="${optionConfig.default}" placeholder="${optionConfig.label}">
            `;
        }

        optionsContainer.appendChild(groupDiv);
    });
}

// 收集自定义选项
function getCustomOptions() {
    const config = decadeConfigs[selectedDecade];
    if (!config) return null;

    const customOptions = {};

    Object.keys(config).forEach(optionKey => {
        const element = document.getElementById(optionKey);
        if (element) {
            if (element.type === 'checkbox') {
                customOptions[optionKey] = element.checked;
            } else if (element.type === 'range') {
                customOptions[optionKey] = parseFloat(element.value);
            } else {
                customOptions[optionKey] = element.value;
            }
        }
    });

    return customOptions;
}

// 处理视频
processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const statusText = document.getElementById('statusText');
    const resultSection = document.getElementById('resultSection');

    processBtn.disabled = true;
    progressBar.classList.remove('hidden');

    // 更新状态文本
    const decadeTextMap = {
        '1900s': '1900年代',
        '1910s': '1910年代',
        '1920s': '1920年代',
        '1930s': '1930年代',
        '1940s': '1940年代',
        '1950s': '1950年代',
        '1960s': '1960年代',
        '1970s': '1970年代',
        '1980s': '1980年代',
        '1990s': '1990年代'
    };

    statusText.textContent = `正在应用${decadeTextMap[selectedDecade]}滤镜与自定义设置...`;
    progressFill.style.width = '30%';

    try {
        const formData = new FormData();
        formData.append('video', selectedFile);
        formData.append('decade', selectedDecade);

        // 添加自定义选项
        const customOptions = getCustomOptions();
        if (customOptions) {
            formData.append('custom_options', JSON.stringify(customOptions));
        }

        progressFill.style.width = '60%';
        statusText.textContent = '正在处理视频并添加复古效果...';

        const response = await fetch('/api/process-video', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            progressFill.style.width = '100%';
            statusText.textContent = '完成！ ✨ 您的复古影像杰作已准备就绪！';

            const blob = await response.blob();
            const videoUrl = URL.createObjectURL(blob);

            document.getElementById('processedVideo').src = videoUrl;
            document.getElementById('downloadBtn').href = videoUrl;
            document.getElementById('downloadBtn').download = `${selectedDecade}-复古-${Date.now()}.mp4`;

            resultSection.classList.remove('hidden');

            // 滚动到结果区域
            setTimeout(() => {
                resultSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 500);
        } else {
            const errorText = await response.text();
            console.error('Server error:', errorText);
            throw new Error('视频处理失败，请稍后重试');
        }
    } catch (error) {
        console.error('Processing error:', error);
        statusText.textContent = '错误: ' + error.message;
        progressFill.style.width = '0%';

        // 添加错误状态动画
        statusText.style.animation = 'statusPulse 0.5s ease 3';
    }

    processBtn.disabled = false;
    setTimeout(() => {
        progressBar.classList.add('hidden');
    }, 3000);
});

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 创建星空背景
    createStarfield();

    // 初始化组件
    initializeDecades();
    updateCustomizationPanel();

    // 添加页面加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.8s ease';
        document.body.style.opacity = '1';
    }, 100);

    console.log('🎬 时光影像应用已初始化 - 深度美化版');
});
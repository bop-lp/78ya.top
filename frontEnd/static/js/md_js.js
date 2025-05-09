// js/scripts.js
document.addEventListener('DOMContentLoaded', () => {
    // 每日一言（处理text响应）
    const fetchDailyQuote = async () => {
        const quoteElement = document.getElementById('dailyQuote');
        try {
            const response = await fetch('/api/dmyiyan/api');
            const text = await response.text();

            if (text && text.trim().length > 0) {
                quoteElement.textContent = text;

            } else {
                quoteElement.textContent = '代码是现实的诗歌，算法是逻辑的舞蹈';
            }
        } catch {
            quoteElement.textContent = '连接知识星海的航路暂时中断';
        }
    };

    fetchDailyQuote();

});


// 增强图片自适应函数
function adaptMarkdownImages() {
    const container = document.querySelector('.markdown-content');
    if (!container) return;

    const images = container.querySelectorAll('img');
    // 获取容器实际宽度（减20px边距）
    const containerWidth = container.offsetWidth - 60;

    images.forEach(img => {
        const effectiveWidth = Math.min(
            containerWidth * 0.95,
            img.naturalWidth
        );

        // 设置最终尺寸（保留5%的边距空间）
        img.style.width = `${effectiveWidth}px`;
        img.style.height = 'auto'; // 保持宽高比
    });
}

// 添加监听器
document.addEventListener('DOMContentLoaded', adaptMarkdownImages);
window.addEventListener('resize', adaptMarkdownImages);

// 观察 Markdown 内容区变化
const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length) {
            adaptMarkdownImages();
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

// 添加图片点击事件
document.querySelectorAll('.stack-img').forEach(img => {
    img.addEventListener('click', function() {
        this.classList.toggle('fullscreen');
    });
});


document.querySelectorAll('.markdown-content img').forEach(img => {
    // 点击放大（可选功能）
    img.addEventListener('click', function() {
        this.classList.toggle('active');
    });
});



// 使用现代浏览器API实现容器尺寸监听
const initImageAdaption = () => {
    const container = document.querySelector('.image-container');
    if (!container) return;

    // 创建观察器实例
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            const containerWidth = entry.contentRect.width;
            updateImageSizes(containerWidth);
        }
    });

    // 开始观察容器
    resizeObserver.observe(container);

    // 初始化首次加载
    updateImageSizes(container.offsetWidth);
};

// 核心尺寸计算逻辑
const updateImageSizes = (containerWidth) => {
    const images = Array.from(document.querySelectorAll('.image-container img'));
    const GAP = 15; // 图片间距
    const MIN_COLUMN_WIDTH = 200; // 最小列宽

    // 计算列数和实际列宽
    const columns = Math.max(1, Math.floor((containerWidth + GAP) / (MIN_COLUMN_WIDTH + GAP)));
    const columnWidth = (containerWidth - GAP * (columns - 1)) / columns;

    // 批量处理图片
    images.forEach(img => {
        const aspectRatio = img.naturalWidth / img.naturalHeight;
        const maxDisplayWidth = Math.min(columnWidth, img.naturalWidth);

        // 应用尺寸
        img.style.cssText = `
      width: ${maxDisplayWidth}px;
      height: ${maxDisplayWidth / aspectRatio}px;
      flex: 0 0 ${maxDisplayWidth}px; /* 防止flex布局挤压 */
    `;
    });

    // 更新容器布局
    container.style.gap = `${GAP}px`;
    container.style.gridTemplateColumns = `repeat(auto-fill, minmax(${MIN_COLUMN_WIDTH}px, 1fr))`; // 备用布局方案
};

// 初始化
document.addEventListener('DOMContentLoaded', initImageAdaption);
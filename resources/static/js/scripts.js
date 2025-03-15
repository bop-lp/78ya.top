// js/scripts.js
document.addEventListener('DOMContentLoaded', () => {
    // 打字机动画
    const typeWriter = (text, element, speed = 100) => {
        let i = 0;
        element.innerHTML = '';
        const timer = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    };

    // 当前时间显示
    const showCurrentTime = () => {
        const runtimeElement = document.getElementById('runtime');
        const updateTime = () => {
            const now = new Date();
            runtimeElement.textContent = now.toLocaleTimeString('zh-CN', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        };
        updateTime();
        setInterval(updateTime, 1000);
    };

    // 每日一言（处理text响应）
    const fetchDailyQuote = async () => {
        const quoteElement = document.getElementById('dailyQuote');
        try {
            const response = await fetch('https://api.lolimi.cn/API/dmyiyan/api.php');
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

    // 图片自适应
    const adaptImages = () => {
        const container = document.querySelector('.image-container');
        const images = container.querySelectorAll('img');

        const resizeImages = () => {
            const containerWidth = container.offsetWidth;
            const gap = 15;
            const minWidth = 200;
            const columns = Math.max(1, Math.floor((containerWidth + gap) / (minWidth + gap)));

            images.forEach(img => {
                const width = (containerWidth - gap * (columns - 1)) / columns;
                img.style.width = `${width}px`;
                img.style.height = 'auto';
            });
        };

        window.addEventListener('resize', resizeImages);
        resizeImages();
    };

    // 初始化所有功能
    typeWriter('「代码如诗，算法似歌」—— 这里分享编程艺术、技术洞见与数字世界的奇妙旅程',
        document.getElementById('animatedMotto'));

    showCurrentTime();
    fetchDailyQuote();
    adaptImages();
    // # 可以在这里添加更多功能

});

// 动态内容加载逻辑
let currentPage = 1
let isLoading = false

// 修改后的加载函数
async function loadMoreContent() {
    if (isLoading) return;
    document.getElementById('globalErrorContainer').innerHTML = '';

    // 新增：每次加载尝试时隐藏旧错误
    const existingError = document.getElementById('globalError');
    if (existingError) {
        existingError.style.display = 'none';
    }

    isLoading = true;
    showLoading(true);

    try {
        const response = await fetch(`http://localhost:83/md/list/${currentPage}`);
        if (!response.ok) throw new Error(`HTTP错误! 状态码: ${response.status}`);

        const { content } = await response.json(); // 不再需要page参数

        if (content.trim() === '') {
            window.removeEventListener('scroll', scrollHandler);
            showNoMore();
            return;
        }

        const sanitized = DOMPurify.sanitize(content);
        document.getElementById('contentContainer').insertAdjacentHTML('beforeend', sanitized);

        currentPage += 1;  // 正确递增页码

    } catch (error) {
        console.error('加载错误:', error);
        showError('内容加载失败: ' + error.message);
    } finally {
        isLoading = false;
        showLoading(false);
    }
}

// 滚动事件处理
function scrollHandler() {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement
    if (scrollTop + clientHeight >= scrollHeight - 200) {
        loadMoreContent()
    }
}

// 初始化加载
window.addEventListener('DOMContentLoaded', () => {
    loadMoreContent()
    window.addEventListener('scroll', scrollHandler)
})

// 新增辅助函数
function showLoading(visible) {
    document.getElementById('loadingIndicator').style.display = visible ? 'block' : 'none'
}

function showNoMore() {
    const msg = document.createElement('div')
    msg.className = 'no-more'
    msg.textContent = '已经到底啦~'
    document.getElementById('contentContainer').appendChild(msg)
}

function showError(message) {
    // 先尝试获取已有错误提示
    const container = document.getElementById('globalErrorContainer');

    container.innerHTML = '';
    // 如果不存在则创建新元素
    if (!errorDiv) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'global-error';
        errorDiv.textContent = message;
        // 插入到内容容器前
        container.appendChild(errorDiv);
    }

    // 自动消失逻辑
    setTimeout(() => {
        container.removeChild(errorDiv);
    }, 5000);
}

document.querySelectorAll('div img').forEach(img => {
    img.addEventListener('mouseenter', () => {
        img.style.transform = 'scale(1.05)';
    });
    img.addEventListener('mouseleave', () => {
        img.style.transform = 'scale(1)';
    });
});


// 渐进式加载优化
document.querySelectorAll('div img').forEach(img => {
    // 监听加载完成
    img.onload = () => {
        img.style.opacity = 1;
        img.parentElement.style.background = 'none';
    };

    // 点击放大功能
    img.addEventListener('click', () => {
        img.classList.toggle('zoomed');
    });
});

document.getElementById('contentCONtainer').addEventListener('mouseover', (e) => {
    if (e.targer.tagName === 'IMG') {
        e.targer.style.transform = 'scale(1.05)';
    }
})

function createOverlay(imgSrc) {
    const overlay = document.createElement('div');
    overlay.className = 'image-overlay';
    overlay.innerHTML = `
      <div class="overlay-background"></div>
      <img src="${imgSrc}" class="zoomed-image">
      <button class="close-btn">×</button>
    `;
    overlay.querySelector('.close-btn').addEventListener('click', () => {
      document.body.removeChild(overlay);
    });
    document.body.appendChild(overlay);
  }
  
  // 修改点击事件
  img.addEventListener('click', () => createOverlay(img.src));

  function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
      const now = Date.now();
      if (now - lastCall >= delay) {
        func.apply(this, args);
        lastCall = now;
      }
    };
  }
  
  window.addEventListener('scroll', throttle(scrollHandler, 200));
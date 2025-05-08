// gallery-manager.js
class GalleryManager {
    constructor(container) {
      this.container = container;
      this.images = [];
      this.baseOffsetRatio = 0.08;
      this.hoverOffsetRatio = 0.12;
      this.resizeObserver = null;
      this.mutationObserver = null;
  
      this.init();
    }
  
    init() {
      // 初始图片收集
      this.images = Array.from(this.container.querySelectorAll('.stack-img'));
      this.setupObservers();
      this.updateLayout();
      this.setupEvents();
    }
  
    setupObservers() {
      // 响应式观察
      this.resizeObserver = new ResizeObserver(entries => {
        entries.forEach(entry => {
          this.updateLayout();
          this.resetAllPositions();
        });
      });
      this.resizeObserver.observe(this.container);
  
      // DOM变化观察
      this.mutationObserver = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
          if (mutation.addedNodes.length) {
            this.handleNewImages(mutation.addedNodes);
          }
        });
      });
      this.mutationObserver.observe(this.container, {
        childList: true,
        subtree: true
      });
    }
  
    handleNewImages(nodes) {
      Array.from(nodes).forEach(node => {
        if (node.classList?.contains('stack-img')) {
          this.images.push(node);
          this.updateSingleImage(node);
          this.setupImageEvents(node);
        }
      });
    }
  
    updateLayout() {
      const containerWidth = this.container.offsetWidth;
      const baseOffset = containerWidth * this.baseOffsetRatio;
  
      this.images.forEach((img, index) => {
        img.style.zIndex = index + 1;
        img.style.left = `${index * baseOffset}px`;
        img.dataset.originalLeft = index * baseOffset;
        img.dataset.galleryId = this.container.id; // 关联画廊ID
      });
    }
  
    updateSingleImage(img) {
      const containerWidth = this.container.offsetWidth;
      const baseOffset = containerWidth * this.baseOffsetRatio;
      const index = this.images.indexOf(img);
  
      img.style.zIndex = index + 1;
      img.style.left = `${index * baseOffset}px`;
      img.dataset.originalLeft = index * baseOffset;
      img.dataset.galleryId = this.container.id;
    }
  
    setupEvents() {
      this.images.forEach(img => {
        this.setupImageEvents(img);
      });
    }
  
    setupImageEvents(img) {
      const handleEnter = e => {
        const target = e.target;
        if (target.dataset.galleryId !== this.container.id) return;
  
        const index = this.images.indexOf(target);
        const hoverOffset = this.container.offsetWidth * this.hoverOffsetRatio;
  
        target.style.zIndex = this.images.length + 1;
        target.style.transform = `translateX(-${hoverOffset}px) scale(1.05)`;
  
        this.images.slice(index + 1).forEach(nextImg => {
          nextImg.style.left = `${parseFloat(nextImg.dataset.originalLeft) + hoverOffset}px`;
        });
      };
  
      const handleLeave = e => {
        const target = e.target;
        if (target.dataset.galleryId !== this.container.id) return;
  
        const index = this.images.indexOf(target);
        target.style.zIndex = index + 1;
        this.resetAllPositions();
      };
  
      img.removeEventListener('mouseenter', handleEnter);
      img.removeEventListener('mouseleave', handleLeave);
      img.addEventListener('mouseenter', handleEnter);
      img.addEventListener('mouseleave', handleLeave);
    }
  
    resetAllPositions() {
      this.images.forEach(img => {
        img.style.transform = 'none';
        img.style.left = `${img.dataset.originalLeft}px`;
      });
    }
  
    destroy() {
      this.resizeObserver.disconnect();
      this.mutationObserver.disconnect();
      this.images.forEach(img => {
        img.removeEventListener('mouseenter', this.handleMouseEnter);
        img.removeEventListener('mouseleave', this.handleMouseLeave);
      });
    }
  }
  
  // 初始化所有画廊容器
  document.addEventListener('DOMContentLoaded', () => {
    const galleries = document.querySelectorAll('.gallery');
    galleries.forEach(container => {
      // 自动生成唯一ID如果不存在
      if (!container.id) {
        container.id = `gallery-${Math.random().toString(36).substr(2, 9)}`;
      }
      new GalleryManager(container);
    });
  });
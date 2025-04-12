// 校验规则配置
const validationRules = {
    username: {
        pattern: /^[a-zA-Z0-9_]{4,16}$/,
        message: '用户名应为4-16位字母、数字或下划线'
    },
    password: {
        pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,18}$/,
        message: '密码需包含字母和数字（6-18位）'
    }
};

// 显示错误信息
function showError(input, message) {
    const formGroup = input.parentElement;
    formGroup.classList.add('error');

    // 防止重复添加错误信息
    let error = formGroup.querySelector('.error-message');
    if (!error) {
        error = document.createElement('div');
        error.className = 'error-message';
        formGroup.appendChild(error);
    }
    error.textContent = message;
}

// 清除错误状态
function clearError(input) {
    const formGroup = input.parentElement;
    formGroup.classList.remove('error');

    const error = formGroup.querySelector('.error-message');
    if (error) error.remove();
}

// 实时输入校验
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('input', function() {
        const rule = validationRules[this.id];
        if (rule) {
            if (this.value && !rule.pattern.test(this.value)) {
                showError(this, rule.message);
            } else {
                clearError(this);
            }
        }
    });
});

// 表单提交处理
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let isValid = true;

    // 验证所有字段
    Object.keys(validationRules).forEach(fieldId => {
        const input = document.getElementById(fieldId);
        const rule = validationRules[fieldId];

        if (!rule.pattern.test(input.value)) {
            showError(input, rule.message);
            isValid = false;
        } else {
            clearError(input);
        }
    });

    // 通过验证后的处理
    if (isValid) {
        alert('表单验证通过，正在跳转...');
        // 此处可添加实际的登录逻辑
        this.reset();
    }
});

// 输入框动态效果
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });

    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});
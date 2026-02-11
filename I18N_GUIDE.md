# 国际化支持文档

## 🌍 功能概述

网站现已支持中英文双语，方便全球用户使用。

## 🎯 支持的语言

- **中文（简体）** - zh
- **English** - en

## 🔧 实现方式

### 1. 后端国际化

**文件**: `i18n.py`

包含所有翻译文本的字典：
```python
TRANSLATIONS = {
    'zh': {
        'page_title': '智能图书推荐系统',
        'main_title': '智能图书推荐系统',
        ...
    },
    'en': {
        'page_title': 'Smart Book Recommendation System',
        'main_title': 'Smart Book Recommendation',
        ...
    }
}
```

### 2. Flask路由

**文件**: `app.py`

```python
@app.route('/')
def index():
    lang = request.args.get('lang', 'zh')
    return render_template('index.html', lang=lang, translations=TRANSLATIONS[lang])

@app.route('/api/translations/<lang>')
def get_translations(lang):
    return jsonify({'translations': TRANSLATIONS[lang]})
```

### 3. 前端模板

**文件**: `templates/index.html`

使用Jinja2模板语法：
```html
<h1>{{ translations.main_title }}</h1>
<p>{{ translations.subtitle }}</p>
```

### 4. JavaScript国际化

**文件**: `static/js/app.js`

```javascript
// 翻译函数
function t(key) {
    return state.translations[key] || key;
}

// 使用示例
showMessage(t('msg_book_added'), 'success');
```

## 📝 使用方法

### 访问不同语言版本

**中文版本**:
```
http://localhost:5000/?lang=zh
```

**英文版本**:
```
http://localhost:5000/?lang=en
```

### 切换语言

点击页面右上角的语言切换按钮：
- **中文** - 切换到中文界面
- **English** - 切换到英文界面

## 🎨 界面元素翻译

### 页面标题和头部
- 页面标题
- 主标题
- 副标题
- 统计信息标签

### 输入区域
- 输入提示
- 按钮文本
- 空状态提示

### 关键词选择
- 标题和说明
- 按钮文本
- 加载提示

### 推荐策略
- 策略名称
- 策略描述
- 关系类型名称

### 推荐结果
- 结果标题
- 匹配度
- 推荐理由
- 查看详情

### 消息提示
- 成功消息
- 警告消息
- 错误消息

## 🔄 添加新语言

### 步骤1: 添加翻译文本

在 `i18n.py` 中添加新语言：

```python
TRANSLATIONS = {
    'zh': {...},
    'en': {...},
    'ja': {  # 日语
        'page_title': 'スマートブック推薦システム',
        'main_title': 'スマートブック推薦',
        ...
    }
}
```

### 步骤2: 更新语言切换按钮

在 `templates/index.html` 中添加按钮：

```html
<div class="lang-switcher">
    <button class="lang-btn" onclick="switchLanguage('zh')">中文</button>
    <button class="lang-btn" onclick="switchLanguage('en')">English</button>
    <button class="lang-btn" onclick="switchLanguage('ja')">日本語</button>
</div>
```

### 步骤3: 更新验证逻辑

在 `app.py` 中更新语言验证：

```python
@app.route('/')
def index():
    lang = request.args.get('lang', 'zh')
    if lang not in ['zh', 'en', 'ja']:
        lang = 'zh'
    return render_template('index.html', lang=lang, translations=TRANSLATIONS[lang])
```

## 📊 翻译覆盖范围

| 类别 | 翻译项数量 | 覆盖率 |
|------|-----------|--------|
| 页面标题 | 3 | 100% |
| 统计信息 | 4 | 100% |
| 输入区域 | 5 | 100% |
| 关键词选择 | 4 | 100% |
| 推荐策略 | 9 | 100% |
| 按钮文本 | 5 | 100% |
| 推荐结果 | 7 | 100% |
| 消息提示 | 13 | 100% |
| **总计** | **50** | **100%** |

## 🌐 SEO优化

### HTML lang属性

```html
<html lang="{{ lang }}">
```

根据当前语言自动设置，有利于搜索引擎优化。

### 页面标题

```html
<title>{{ translations.page_title }}</title>
```

每种语言都有独立的页面标题。

## 💡 最佳实践

### 1. 保持翻译一致性

- 使用统一的术语
- 保持语气和风格一致
- 注意文化差异

### 2. 处理动态内容

```javascript
// 好的做法
showMessage(`${t('msg_book_added')}《${bookName}》`, 'success');

// 避免硬编码
showMessage(`已添加《${bookName}》`, 'success');
```

### 3. 测试所有语言

- 检查文本长度是否合适
- 确保布局不会因文本长度而破坏
- 测试所有交互功能

### 4. 提供语言切换

- 显眼的位置放置语言切换按钮
- 保持当前页面状态
- 提供清晰的视觉反馈

## 🔍 调试技巧

### 查看当前语言

```javascript
console.log('Current language:', state.currentLang);
```

### 查看所有翻译

```javascript
console.log('Translations:', state.translations);
```

### 测试缺失的翻译

```javascript
function t(key) {
    const text = state.translations[key];
    if (!text) {
        console.warn(`Missing translation: ${key}`);
    }
    return text || key;
}
```

## 📱 响应式设计

语言切换按钮在移动设备上的适配：

```css
@media (max-width: 768px) {
    .lang-switcher {
        top: 10px;
        right: 10px;
    }
    
    .lang-btn {
        padding: 6px 12px;
        font-size: 0.8rem;
    }
}
```

## 🚀 性能优化

### 1. 翻译文本缓存

翻译文本在页面加载时一次性传递给JavaScript，避免重复请求。

### 2. 按需加载

只加载当前语言的翻译文本，减少数据传输。

### 3. 浏览器缓存

利用浏览器缓存存储语言偏好：

```javascript
// 保存语言偏好
localStorage.setItem('preferred_lang', lang);

// 读取语言偏好
const preferredLang = localStorage.getItem('preferred_lang') || 'zh';
```

## 📝 总结

通过实现完整的国际化支持，网站现在可以服务全球用户。系统采用了：

- ✅ 后端模板渲染
- ✅ 前端动态翻译
- ✅ 统一的翻译管理
- ✅ 灵活的语言切换
- ✅ 完整的界面覆盖

未来可以轻松添加更多语言支持！


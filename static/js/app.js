// 应用状态
const state = {
    favoriteBooks: [],
    favoriteBooksIds: {},  // 书名到ID的映射
    searchTimeout: null,
    recommendations: [],
    allKeywords: [],  // 所有关键词
    selectedKeywords: [],  // 用户选择的关键词
    currentLang: window.currentLang || 'zh',  // 当前语言
    translations: window.translations || {}  // 翻译文本
};

// API基础URL
const API_BASE = window.location.origin;

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    bindEvents();
    loadStats();
});

// 初始化应用
function initApp() {
    console.log('图书推荐系统初始化...');
}

// 切换语言
function switchLanguage(lang) {
    if (lang === state.currentLang) return;
    
    // 重新加载页面并传递语言参数
    window.location.href = `${API_BASE}/?lang=${lang}`;
}

// 获取翻译文本
function t(key) {
    return state.translations[key] || key;
}

// 绑定事件
function bindEvents() {
    const bookInput = document.getElementById('bookInput');
    const addBookBtn = document.getElementById('addBookBtn');
    const recommendBtn = document.getElementById('recommendBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    // 输入框事件
    bookInput.addEventListener('input', handleBookInput);
    bookInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addBook();
        }
    });
    
    // 按钮事件
    addBookBtn.addEventListener('click', addBook);
    recommendBtn.addEventListener('click', getRecommendations);
    clearBtn.addEventListener('click', clearFavoriteBooks);
    
    // 策略选择事件
    const strategyRadios = document.querySelectorAll('input[name="strategy"]');
    strategyRadios.forEach(radio => {
        radio.addEventListener('change', handleStrategyChange);
    });
    
    // 初始化关系选择区域的显示状态
    handleStrategyChange();
}

// 处理策略变化
function handleStrategyChange() {
    const selectedStrategy = document.querySelector('input[name="strategy"]:checked').value;
    const relationsSection = document.getElementById('relationsSection');
    
    // 只有在知识图谱或混合策略时显示关系选择
    if (selectedStrategy === 'kg_only' || selectedStrategy === 'mixed') {
        relationsSection.classList.remove('hidden');
    } else {
        relationsSection.classList.add('hidden');
    }
}

// 处理书籍输入
function handleBookInput(e) {
    const query = e.target.value.trim();
    
    // 清除之前的定时器
    if (state.searchTimeout) {
        clearTimeout(state.searchTimeout);
    }
    
    // 如果输入为空，隐藏建议
    if (!query) {
        hideSuggestions();
        return;
    }
    
    // 延迟搜索
    state.searchTimeout = setTimeout(() => {
        searchBooks(query);
    }, 300);
}

// 搜索书籍
async function searchBooks(query) {
    try {
        const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}&limit=10`);
        const data = await response.json();
        
        if (data.success && data.data.results.length > 0) {
            showSuggestions(data.data.results);
        } else {
            hideSuggestions();
        }
    } catch (error) {
        console.error('搜索失败:', error);
        hideSuggestions();
    }
}

// 显示搜索建议
function showSuggestions(results) {
    const suggestionsDiv = document.getElementById('searchSuggestions');
    
    suggestionsDiv.innerHTML = results.map(book => `
        <div class="suggestion-item" onclick="selectBook('${escapeHtml(book.book_name)}')">
            <div class="suggestion-name">${escapeHtml(book.book_name)}</div>
            <div class="suggestion-rating">⭐ ${book.rating || '暂无评分'}</div>
        </div>
    `).join('');
    
    suggestionsDiv.classList.add('show');
}

// 隐藏搜索建议
function hideSuggestions() {
    const suggestionsDiv = document.getElementById('searchSuggestions');
    suggestionsDiv.classList.remove('show');
    suggestionsDiv.innerHTML = '';
}

// 选择书籍
function selectBook(bookName) {
    document.getElementById('bookInput').value = bookName;
    hideSuggestions();
    addBook();
}

// 添加书籍
async function addBook() {
    const bookInput = document.getElementById('bookInput');
    const bookName = bookInput.value.trim();
    
    if (!bookName) {
        showMessage(t('msg_input_book'), 'warning');
        return;
    }
    
    // 检查是否已添加
    if (state.favoriteBooks.includes(bookName)) {
        showMessage(t('msg_book_exists'), 'warning');
        return;
    }
    
    // 搜索书籍获取ID
    try {
        const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(bookName)}&limit=1`);
        const data = await response.json();
        
        if (data.success && data.data.results.length > 0) {
            const book = data.data.results[0];
            state.favoriteBooks.push(bookName);
            state.favoriteBooksIds[bookName] = book.book_id;
            
            bookInput.value = '';
            hideSuggestions();
            
            // 更新UI
            updateFavoriteBooksUI();
            updateRecommendButton();
            
            // 加载关键词
            await loadKeywords();
            
            showMessage(`${t('msg_book_added')}《${bookName}》`, 'success');
        } else {
            showMessage(t('msg_book_not_found'), 'warning');
        }
    } catch (error) {
        console.error('添加书籍失败:', error);
        showMessage('添加失败，请重试', 'error');
    }
}

// 移除书籍
async function removeBook(bookName) {
    const index = state.favoriteBooks.indexOf(bookName);
    if (index > -1) {
        state.favoriteBooks.splice(index, 1);
        delete state.favoriteBooksIds[bookName];
        updateFavoriteBooksUI();
        updateRecommendButton();
        
        // 重新加载关键词
        await loadKeywords();
        
        showMessage(`${t('msg_book_removed')}《${bookName}》`, 'info');
    }
}

// 加载关键词
async function loadKeywords() {
    const keywordsSection = document.getElementById('keywordsSection');
    const keywordsContainer = document.getElementById('keywordsContainer');
    
    if (state.favoriteBooks.length === 0) {
        keywordsSection.style.display = 'none';
        state.allKeywords = [];
        state.selectedKeywords = [];
        return;
    }
    
    // 显示关键词区域
    keywordsSection.style.display = 'block';
    keywordsContainer.innerHTML = `
        <div class="loading-keywords">
            <div class="loading-spinner-small"></div>
            <p>正在加载关键词...</p>
        </div>
    `;
    
    try {
        // 获取所有书籍的关键词
        const allKeywordsMap = new Map();
        
        for (const bookName of state.favoriteBooks) {
            const bookId = state.favoriteBooksIds[bookName];
            if (!bookId) continue;
            
            const response = await fetch(`${API_BASE}/api/book/${bookId}/keywords`);
            const data = await response.json();
            
            if (data.success && data.data.keywords) {
                data.data.keywords.forEach(kw => {
                    if (allKeywordsMap.has(kw.word)) {
                        allKeywordsMap.get(kw.word).weight += kw.weight;
                        allKeywordsMap.get(kw.word).count += 1;
                    } else {
                        allKeywordsMap.set(kw.word, {
                            word: kw.word,
                            weight: kw.weight,
                            count: 1
                        });
                    }
                });
            }
        }
        
        // 转换为数组并排序
        state.allKeywords = Array.from(allKeywordsMap.values())
            .sort((a, b) => b.weight - a.weight)
            .slice(0, 50);  // 最多显示50个
        
        // 显示关键词
        displayKeywords();
        
    } catch (error) {
        console.error('加载关键词失败:', error);
        keywordsContainer.innerHTML = `
            <div class="empty-state">
                <p>加载关键词失败</p>
            </div>
        `;
    }
}

// 显示关键词
function displayKeywords() {
    const keywordsContainer = document.getElementById('keywordsContainer');
    
    if (state.allKeywords.length === 0) {
        keywordsContainer.innerHTML = `
            <div class="empty-state">
                <p>${t('empty_books')}</p>
            </div>
        `;
        return;
    }
    
    keywordsContainer.innerHTML = `
        <div class="keywords-grid" id="keywordsGrid"></div>
        <div class="keywords-actions">
            <button class="btn-small btn-select-all" onclick="selectAllKeywords()">${t('btn_select_all')}</button>
            <button class="btn-small btn-clear-selection" onclick="clearKeywordSelection()">${t('btn_clear_selection')}</button>
        </div>
    `;
    
    const keywordsGrid = document.getElementById('keywordsGrid');
    keywordsGrid.innerHTML = state.allKeywords.map(kw => `
        <div class="keyword-chip ${state.selectedKeywords.includes(kw.word) ? 'selected' : ''}" 
             onclick="toggleKeyword('${escapeHtml(kw.word)}')">
            <span class="keyword-chip-text">${escapeHtml(kw.word)}</span>
            <span class="keyword-chip-weight">${(kw.weight * 100).toFixed(0)}%</span>
        </div>
    `).join('');
}

// 切换关键词选择
function toggleKeyword(keyword) {
    const index = state.selectedKeywords.indexOf(keyword);
    if (index > -1) {
        state.selectedKeywords.splice(index, 1);
    } else {
        state.selectedKeywords.push(keyword);
    }
    displayKeywords();
}

// 全选关键词
function selectAllKeywords() {
    state.selectedKeywords = state.allKeywords.map(kw => kw.word);
    displayKeywords();
    showMessage(t('msg_keywords_selected'), 'info');
}

// 清空关键词选择
function clearKeywordSelection() {
    state.selectedKeywords = [];
    displayKeywords();
    showMessage(t('msg_keywords_cleared'), 'info');
}

// 更新喜欢的书籍UI
function updateFavoriteBooksUI() {
    const favoriteBooksDiv = document.getElementById('favoriteBooks');
    
    if (state.favoriteBooks.length === 0) {
        favoriteBooksDiv.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📖</span>
                <p>还没有添加喜欢的书籍</p>
            </div>
        `;
    } else {
        favoriteBooksDiv.innerHTML = state.favoriteBooks.map(book => `
            <div class="book-tag">
                <span class="book-tag-name">${escapeHtml(book)}</span>
                <button class="remove-book" onclick="removeBook('${escapeHtml(book)}')" title="移除">×</button>
            </div>
        `).join('');
    }
}

// 更新推荐按钮状态
function updateRecommendButton() {
    const recommendBtn = document.getElementById('recommendBtn');
    recommendBtn.disabled = state.favoriteBooks.length === 0;
}

// 清空喜欢的书籍
function clearFavoriteBooks() {
    if (state.favoriteBooks.length === 0) {
        return;
    }
    
    if (confirm(t('msg_confirm_clear'))) {
        state.favoriteBooks = [];
        state.favoriteBooksIds = {};
        updateFavoriteBooksUI();
        updateRecommendButton();
        hideResults();
        
        // 隐藏关键词区域
        document.getElementById('keywordsSection').style.display = 'none';
        state.allKeywords = [];
        state.selectedKeywords = [];
        
        showMessage(t('msg_cleared'), 'info');
    }
}

// 获取推荐
async function getRecommendations() {
    if (state.favoriteBooks.length === 0) {
        showMessage(t('msg_select_book'), 'warning');
        return;
    }
    
    // 获取选中的策略
    const strategy = document.querySelector('input[name="strategy"]:checked').value;
    
    // 获取选中的关系（仅在kg_only或mixed策略时）
    let relations = null;
    if (strategy === 'kg_only' || strategy === 'mixed') {
        const selectedRelations = Array.from(document.querySelectorAll('input[name="relation"]:checked'))
            .map(checkbox => checkbox.value);
        
        if (selectedRelations.length === 0) {
            showMessage(t('msg_select_relation'), 'warning');
            return;
        }
        
        relations = selectedRelations;
    }
    
    // 获取用户选择的关键词
    const selectedKeywords = state.selectedKeywords.length > 0 ? state.selectedKeywords : null;
    
    // 显示加载状态
    showLoading();
    
    try {
        const requestBody = {
            favorite_books: state.favoriteBooks,
            top_k: 20,
            strategy: strategy
        };
        
        // 只在需要时添加relations参数
        if (relations) {
            requestBody.relations = relations;
        }
        
        // 添加选择的关键词
        if (selectedKeywords) {
            requestBody.selected_keywords = selectedKeywords;
        }
        
        const response = await fetch(`${API_BASE}/api/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.recommendations = data.data.recommendations;
            displayRecommendations(data.data.recommendations, strategy, relations);
            showMessage(`${t('msg_recommend_success')} ${data.data.recommendations.length} ${t('msg_recommend_books')}`, 'success');
        } else {
            showMessage(data.message || '推荐失败', 'error');
            hideLoading();
        }
    } catch (error) {
        console.error('推荐失败:', error);
        showMessage('推荐失败，请稍后重试', 'error');
        hideLoading();
    }
}

// 显示加载状态
function showLoading() {
    const resultsSection = document.getElementById('resultsSection');
    const loading = document.getElementById('loading');
    const recommendations = document.getElementById('recommendations');
    
    resultsSection.style.display = 'block';
    loading.style.display = 'block';
    recommendations.innerHTML = '';
    
    // 滚动到结果区域
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 隐藏加载状态
function hideLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'none';
}

// 隐藏结果
function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'none';
}

// 显示推荐结果
function displayRecommendations(recommendations, strategy, relations) {
    hideLoading();
    
    const recommendationsDiv = document.getElementById('recommendations');
    const resultsSubtitle = document.getElementById('resultsSubtitle');
    
    // 更新副标题，显示使用的策略
    const strategyNames = {
        'mixed': t('strategy_mixed'),
        'kg_only': t('strategy_kg'),
        'keyword_only': t('strategy_keyword')
    };
    
    let subtitleText = `${t('results_subtitle')} (${strategyNames[strategy]})`;
    if (relations && relations.length > 0) {
        const relationNames = {
            'series': t('relation_series'),
            'author': t('relation_author'),
            'translator': t('relation_translator'),
            'publisher': t('relation_publisher')
        };
        const relationText = relations.map(r => relationNames[r]).join('、');
        subtitleText += ` - ${relationText}`;
    }
    resultsSubtitle.textContent = subtitleText;
    
    if (recommendations.length === 0) {
        recommendationsDiv.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">😔</span>
                <p>${t('no_results')}</p>
            </div>
        `;
        return;
    }
    
    recommendationsDiv.innerHTML = recommendations.map((rec, index) => `
        <div class="recommendation-card">
            <div class="card-header">
                <div class="card-rank">#${index + 1}</div>
                <div class="card-score">${t('match_score')} ${(rec.score * 100).toFixed(1)}%</div>
            </div>
            
            <h3 class="card-title">${escapeHtml(rec.book_name)}</h3>
            
            ${rec.rating ? `
                <div class="card-rating">
                    <span>⭐</span>
                    <span>${rec.rating}</span>
                </div>
            ` : ''}
            
            ${rec.reasons && rec.reasons.length > 0 ? `
                <div class="card-reasons">
                    <div class="reasons-title">📖 ${t('reason_title')}</div>
                    ${rec.reasons.map(reason => `
                        <div class="reason-item">${escapeHtml(reason)}</div>
                    `).join('')}
                </div>
            ` : ''}
            
            ${rec.book_url ? `
                <a href="${escapeHtml(rec.book_url)}" target="_blank" class="card-link">
                    ${t('view_detail')} →
                </a>
            ` : ''}
        </div>
    `).join('');
}

// 加载统计信息
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/api/stats`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.data;
            document.getElementById('statBooks').textContent = formatNumber(stats.books);
            document.getElementById('statAuthors').textContent = formatNumber(stats.authors);
            document.getElementById('statPublishers').textContent = formatNumber(stats.publishers);
            document.getElementById('statRelations').textContent = formatNumber(stats.total_relations);
        }
    } catch (error) {
        console.error('加载统计信息失败:', error);
    }
}

// 格式化数字
function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
}

// 显示消息
function showMessage(message, type = 'info') {
    // 创建消息元素
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : type === 'warning' ? '#f39c12' : '#3498db'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 700;
    `;
    
    document.body.appendChild(messageDiv);
    
    // 3秒后移除
    setTimeout(() => {
        messageDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 300);
    }, 3000);
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);


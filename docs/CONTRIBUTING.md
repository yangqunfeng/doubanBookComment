# 贡献指南 / Contributing Guide

[中文](#中文) | [English](#english)

---

## 中文

感谢你考虑为本项目做出贡献！

### 🤝 如何贡献

#### 报告 Bug

如果你发现了 Bug，请：

1. 检查 [Issues](https://github.com/yourusername/doubanBookComment/issues) 中是否已有相同问题
2. 如果没有，创建新的 Issue，包含：
   - 清晰的标题和描述
   - 复现步骤
   - 预期行为和实际行为
   - 系统环境（Python 版本、操作系统等）
   - 相关的错误日志或截图

#### 提出新功能

如果你有新功能的想法：

1. 先创建 Issue 讨论该功能的必要性和实现方案
2. 等待维护者反馈
3. 获得认可后再开始开发

#### 提交代码

1. **Fork 项目**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/your-username/doubanBookComment.git
   cd doubanBookComment
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行开发**
   - 遵循项目的代码风格
   - 添加必要的注释
   - 编写或更新测试
   - 更新相关文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加某某功能"
   ```

6. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 填写 PR 模板
   - 等待代码审查

### 📝 代码规范

#### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 4 个空格缩进
- 函数和类添加文档字符串
- 变量命名使用小写加下划线

示例：
```python
def calculate_similarity(book_a, book_b):
    """
    计算两本书的相似度
    
    Args:
        book_a: 第一本书的ID
        book_b: 第二本书的ID
        
    Returns:
        float: 相似度分数 (0-1)
    """
    # 实现代码
    pass
```

#### JavaScript 代码风格

- 使用 2 个空格缩进
- 使用 `const` 和 `let`，避免 `var`
- 函数添加注释说明
- 使用驼峰命名法

示例：
```javascript
/**
 * 获取推荐结果
 * @param {Array} favoriteBooks - 用户喜欢的书籍列表
 * @param {string} strategy - 推荐策略
 * @returns {Promise} 推荐结果
 */
async function getRecommendations(favoriteBooks, strategy) {
  // 实现代码
}
```

#### 提交信息规范

使用语义化的提交信息：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建或辅助工具的变动

示例：
```
feat: 添加用户反馈功能
fix: 修复关键词提取的编码问题
docs: 更新 API 文档
```

### 🧪 测试

在提交 PR 前，请确保：

1. **运行现有测试**
   ```bash
   python test_keyword_quality.py
   python test_strategies.py
   ```

2. **添加新测试**（如果你添加了新功能）
   ```python
   def test_new_feature():
       # 测试代码
       assert result == expected
   ```

3. **手动测试**
   - 启动服务并测试 Web 界面
   - 测试各种边界情况
   - 确保中英文界面都正常工作

### 📚 文档

如果你的更改涉及：

- **新功能**: 更新 README.md 和相关文档
- **API 变更**: 更新 API 文档
- **配置变更**: 更新 config.py 的注释
- **重大变更**: 在 CHANGELOG.md 中记录

### 🎨 UI/UX 改进

如果你想改进界面：

1. 保持与现有设计风格一致
2. 确保响应式设计
3. 测试中英文界面
4. 提供前后对比截图

### ❓ 需要帮助？

- 查看 [文档](docs/)
- 在 Issue 中提问
- 联系维护者

---

## English

Thank you for considering contributing to this project!

### 🤝 How to Contribute

#### Report Bugs

If you find a bug, please:

1. Check if the issue already exists in [Issues](https://github.com/yourusername/doubanBookComment/issues)
2. If not, create a new Issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System environment (Python version, OS, etc.)
   - Relevant error logs or screenshots

#### Suggest Features

If you have an idea for a new feature:

1. Create an Issue to discuss the necessity and implementation
2. Wait for maintainer feedback
3. Start development after approval

#### Submit Code

1. **Fork the Project**
   ```bash
   # Click the Fork button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/doubanBookComment.git
   cd doubanBookComment
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Develop**
   - Follow the project's code style
   - Add necessary comments
   - Write or update tests
   - Update relevant documentation

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add some feature"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Create PR on GitHub
   - Fill in the PR template
   - Wait for code review

### 📝 Code Standards

#### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Add docstrings to functions and classes
- Use lowercase with underscores for variable names

Example:
```python
def calculate_similarity(book_a, book_b):
    """
    Calculate similarity between two books
    
    Args:
        book_a: ID of the first book
        book_b: ID of the second book
        
    Returns:
        float: Similarity score (0-1)
    """
    # Implementation
    pass
```

#### JavaScript Code Style

- Use 2 spaces for indentation
- Use `const` and `let`, avoid `var`
- Add comments to functions
- Use camelCase naming

Example:
```javascript
/**
 * Get recommendations
 * @param {Array} favoriteBooks - List of user's favorite books
 * @param {string} strategy - Recommendation strategy
 * @returns {Promise} Recommendation results
 */
async function getRecommendations(favoriteBooks, strategy) {
  // Implementation
}
```

#### Commit Message Convention

Use semantic commit messages:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code formatting (no functional change)
- `refactor`: Code refactoring
- `test`: Test related
- `chore`: Build or auxiliary tool changes

Example:
```
feat: add user feedback feature
fix: fix encoding issue in keyword extraction
docs: update API documentation
```

### 🧪 Testing

Before submitting a PR, please ensure:

1. **Run Existing Tests**
   ```bash
   python test_keyword_quality.py
   python test_strategies.py
   ```

2. **Add New Tests** (if you added new features)
   ```python
   def test_new_feature():
       # Test code
       assert result == expected
   ```

3. **Manual Testing**
   - Start the service and test the web interface
   - Test various edge cases
   - Ensure both Chinese and English interfaces work

### 📚 Documentation

If your changes involve:

- **New Features**: Update README.md and related docs
- **API Changes**: Update API documentation
- **Config Changes**: Update comments in config.py
- **Breaking Changes**: Record in CHANGELOG.md

### 🎨 UI/UX Improvements

If you want to improve the interface:

1. Keep consistent with existing design style
2. Ensure responsive design
3. Test both Chinese and English interfaces
4. Provide before/after screenshots

### ❓ Need Help?

- Check the [documentation](docs/)
- Ask in Issues
- Contact maintainers

---

## 🙏 Thank You!

Your contributions make this project better!


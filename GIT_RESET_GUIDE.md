# Git 历史清理指南

## 🔄 清理 Git 历史，重新开始

如果你想删除所有之前的提交记录，只保留当前状态作为初始提交，按以下步骤操作：

### 方法一：删除 .git 文件夹重新初始化（最简单）

```bash
# 1. 删除 Git 历史
Remove-Item -Recurse -Force .git

# 2. 重新初始化
git init

# 3. 添加所有文件
git add .

# 4. 创建初始提交
git commit -m "Initial commit: 基于知识图谱的智能图书推荐系统"

# 5. 添加远程仓库（如果已有 GitHub 仓库）
git remote add origin https://github.com/你的用户名/doubanBookComment.git

# 6. 强制推送（会覆盖远程仓库）
git branch -M main
git push -u origin main --force
```

### 方法二：使用 Git 命令清理历史（保留 .git 配置）

```bash
# 1. 创建一个新的孤立分支
git checkout --orphan latest_branch

# 2. 添加所有文件
git add -A

# 3. 提交
git commit -m "Initial commit: 基于知识图谱的智能图书推荐系统"

# 4. 删除旧的 main 分支
git branch -D main

# 5. 重命名当前分支为 main
git branch -m main

# 6. 强制推送到远程（如果已有远程仓库）
git push -f origin main
```

### 方法三：如果还没有推送到 GitHub（最简单）

```bash
# 直接删除 .git 重新开始
Remove-Item -Recurse -Force .git
git init
git add .
git commit -m "Initial commit: 基于知识图谱的智能图书推荐系统"
```

## ⚠️ 注意事项

1. **强制推送会覆盖远程仓库**
   - 如果远程仓库有其他人的提交，会丢失
   - 确保只有你一个人在使用这个仓库

2. **备份重要数据**
   - 清理前确保本地代码是最新的
   - 如果不确定，先备份整个项目文件夹

3. **如果是新项目**
   - 还没推送到 GitHub，直接用方法一最简单

## ✅ 推荐流程（全新开始）

```bash
# 进入项目目录
cd c:\Users\yangq\PycharmProjects\doubanBookComment

# 删除旧的 Git 历史
Remove-Item -Recurse -Force .git

# 重新初始化
git init

# 添加所有文件
git add .

# 查看将要提交的文件（确认数据文件没有被添加）
git status

# 创建初始提交
git commit -m "Initial commit: 基于知识图谱的智能图书推荐系统"

# 如果要推送到 GitHub
git remote add origin https://github.com/你的用户名/doubanBookComment.git
git branch -M main
git push -u origin main --force
```

## 🎯 完成后

你将得到一个干净的 Git 历史，只有一个初始提交，包含当前所有的代码和文档。


# Data Structures and Algorithms Notes

这个目录是个人数据结构与算法学习笔记站点，使用 MkDocs Material 构建。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再在本目录运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## MathJax

公式渲染由 `pymdownx.arithmatex` 和笔记总入口托管的共享 MathJax 统一管理，不需要在单篇 Markdown 文件中插入 `<script>`。

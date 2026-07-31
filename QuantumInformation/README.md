# Quantum Information Notes

这个目录是量子信息学习笔记的 MkDocs Material 工程，内容由相邻 `../quan_info/《量子信息》知识梳理` 中的原始 Markdown 与配图整理而来。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## 数学公式

公式渲染统一由 `pymdownx.arithmatex` 和笔记总入口托管的共享 MathJax 负责。量子态的 bra-ket 记号中有大量竖线，迁移和编辑时尽量把公式完整保留在 `$...$` 或 `$$...$$` 内，避免 Markdown 表格或普通文本先把符号拆开。

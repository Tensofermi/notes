# Computer Organization Notes

这是计算机组成原理学习笔记的独立 MkDocs Material 工程。内容从信息表示和数字逻辑出发，经 ISA、CPU、流水线、存储层次和 I/O，最终用一组 `load/add/store` 指令把各层机制串成完整路径。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## 写作约定

- 普通页面不使用 front matter。
- 行内公式使用 `$...$`，独立公式使用 `$$...$$`。
- 每个 Markdown 页面都显式登记在 `mkdocs.yml` 的 `nav` 中。
- 章节尽量同时回答动机、机制、最小例子、权衡、限制、历史联系与自测问题。

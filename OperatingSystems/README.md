# Operating Systems Notes

这是操作系统学习笔记的独立 MkDocs Material 工程。内容从“操作系统为什么存在”出发，依次讨论进程与调度、并发同步、虚拟内存、文件系统与 I/O、保护与虚拟化，最后用一次 `read` 系统调用把整条路径串起来。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## 数学公式

公式渲染由 `pymdownx.arithmatex` 和笔记总入口托管的共享 MathJax 负责。Markdown 源文件统一使用 `$...$` 书写行内公式，使用 `$$...$$` 书写独立公式。

## 内容约定

- 根目录和站点目录使用 PascalCase，章节与页面文件使用 snake_case。
- 每章有独立 `index.md`，专题页按推荐阅读顺序编号。
- 每个专题尽量回答动机、机制、最小例子、权衡、限制、历史联系与自测问题。
- `mkdocs.yml` 显式维护全部站内 Markdown 页面，避免新增页面后失去导航入口。

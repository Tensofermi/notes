# Computer Networks Notes

这个目录是一套独立的计算机网络 MkDocs Material 学习笔记。正文从“浏览器为何能取得远端页面”这一问题出发，依次建立分层、应用层、传输层、网络层、链路层和安全知识，再用端到端案例与诊断工具把各层重新串起来。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## 目录约定

- 站点目录使用 PascalCase，章节和页面文件使用 snake_case。
- 每章包含 `index.md` 作为学习入口，专题页负责形成一个可独立复习的知识闭环。
- 所有 Markdown 页面都显式登记在 `mkdocs.yml` 的 `nav` 中。
- `site/` 是构建产物，正文修改应发生在 `docs/`。

## 数学公式

Markdown 中的行内公式统一写成 `$E=mc^2$`，独立公式统一写成 `$$E=mc^2$$`。渲染由 `pymdownx.arithmatex` 和笔记总入口托管的共享 MathJax 负责。

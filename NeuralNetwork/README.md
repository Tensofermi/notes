# Neural Network Notes

这是神经网络与 NNQS 相关笔记的 MkDocs 工程。目录名已经统一为 `NeuralNetwork`，网页标题使用 `Neural Network Notes`。

## 构建与发布

先在仓库根目录安装 `requirements.txt`，再运行：

```bash
python -m mkdocs serve
python -m mkdocs build --strict
```

推送到 `main` 后由仓库根目录的 GitHub Actions 统一构建和发布。

## 数学公式

公式渲染由本站配置和笔记总入口托管的共享 MathJax 完成：

- `docs/javascripts/mathjax.js`
- `https://tensofermi.github.io/notes/_shared/mathjax/es5/tex-chtml.js`

# Tensofermi Notes

个人学习笔记的源码仓库。正文使用 Markdown 编写，MkDocs Material 负责构建，GitHub Actions 将统一产物部署到：

<https://tensofermi.github.io/notes/>

## 仓库结构

- 根 `mkdocs.yml` 与 `home/`：笔记总入口。
- 各 PascalCase 目录：一套独立 MkDocs 笔记。
- `home/_shared/mathjax/`：所有子站共用的一份 MathJax 运行时。
- `mkdocs_file_search.py`：为构建产物补充本地文件搜索支持。
- `scripts/normalize_formula_delimiters.py`：检查公式是否统一使用 `$...$` 与 `$$...$$`。
- `scripts/build_all.sh`：按统一顺序严格构建全部站点。

生成的 `site/` 和 `_site/` 均被忽略，不进入 Git 历史。

## 本地环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

预览单个站点：

```bash
cd ComputerNetworks
python -m mkdocs serve
```

严格构建全部站点：

```bash
./scripts/build_all.sh
```

## 发布

推送到 `main` 后，`.github/workflows/pages.yml` 会构建一个 Pages artifact。仓库只保存 Markdown、配置和必要资源，不提交生成的 HTML。

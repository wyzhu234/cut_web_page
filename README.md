# cut_web_page

个人学习笔记仓库：收集深度学习、计算机视觉与工程实践相关的 HTML 页面，通过 GitHub Pages 在线浏览。

**在线地址：** [https://wyzhu234.github.io/cut_web_page/](https://wyzhu234.github.io/cut_web_page/)

## 目录结构

```
.
├── dl/                 # 深度学习（CNN / Transformer / RAG / LLM / YOLO / 概念 / 任务）
├── dl_cicd/            # CI/CD、数据标注
├── dl_deploy/          # 模型部署
├── hardware/           # 硬件 / 传感器
├── tool_develop/       # 开发工具（docker / git / gdb / cmake）
├── cv/                 # 计算机视觉
├── robot/              # 机器人
├── package_python/     # Python 生态
├── package_cpp/        # C++ 生态
├── clash/              # 网络工具
├── scripts/
│   └── generate_nav.py # 扫描全部 HTML，生成导航页
└── index.html          # 导航页（由脚本生成，勿手动编辑）
```

## 添加笔记

```bash
# 1. 将 .html 放入对应分类目录
# 2. 必须 git add，否则不会部署
git add dl/xxx/你的笔记.html
git commit -m "add,xxx笔记"
git push github main
# 3. 约 1–2 分钟后自动部署完成
```

## 本地预览

```bash
python scripts/generate_nav.py
# 用浏览器打开 index.html
```

## 自动部署

push 到 `main` 且有 `.html` 变更时，GitHub Actions 会：

1. 运行 `scripts/generate_nav.py` 生成导航页  
2. 部署到 GitHub Pages  

也可在 Actions 页手动触发 `workflow_dispatch`。

## 远程仓库

| 远程 | 地址 | 说明 |
|------|------|------|
| `github` | GitHub | 自动部署 Pages |
| `origin` | Gitee | 手动更新 Pages |

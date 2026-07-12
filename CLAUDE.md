# CLAUDE.md

个人学习笔记仓库，保存了从各处收集的深度学习、计算机视觉、工程实践相关的 HTML 页面。

## 仓库结构

```
.
├── dl/                     # 深度学习核心笔记
│   ├── 1_cnn/              # CNN 卷积神经网络
│   ├── 2_transformer/      # Transformer（含 Attention/encoding/sam/vit 子目录）
│   ├── 3_rag/              # RAG 检索增强生成（含 langchain 子目录）
│   ├── conception/         # 深度学习概念（激活函数/backbone/损失函数/IOU/卷积等）
│   ├── llm/                # 大语言模型（含 1_rag 子目录）
│   ├── task/               # 论文与任务（含 detection/track/segment 子目录）
│   └── yolo/               # YOLO 目标检测系列
├── dl_cicd/                # CI/CD、数据标注（cvat/fiftyone）
├── dl_deploy/              # 模型部署
├── hardware/               # 硬件/传感器（rgb/rgbd/range_image）
├── tool_develop/           # 开发工具（docker/git/gdb/cmake）
├── cv/                     # 计算机视觉
├── robot/                  # 机器人
├── package_python/         # Python 生态
├── package_cpp/            # C++ 生态
├── clash/                  # 网络工具
├── scripts/
│   └── generate_nav.py     # 递归扫描所有 HTML 生成 index.html 导航页
├── .github/workflows/
│   └── deploy.yml          # GitHub Actions → GitHub Pages 自动部署
└── index.html              # 导航页（由脚本自动生成，不手动编辑）
```

## 关键工作流

### 部署到 Pages
每次 push 到 `master` 分支自动触发 GitHub Actions：
1. checkout 代码
2. 运行 `python scripts/generate_nav.py` 生成导航页
3. 上传全部文件并部署到 `https://wyzhu234.github.io/cut_web_page/`

```bash
git push github master
```

### 添加新笔记

```bash
# 1. 放入对应分类目录，确保是 .html 文件
# 2. git add 新增文件（非常重要！漏加则不会部署）
git add dl/xxx/你的笔记.html
git commit -m "add,xxx笔记"
git push github master
# 3. 等 1-2 分钟自动部署完成
```

> **注意：** 新增的 .html 文件必须 `git add`，否则不会推送到 GitHub，也不会部署到 Pages。

### 本地预览

```bash
# 重新生成导航页
python scripts/generate_nav.py

# 然后直接用浏览器打开 index.html
```

## 远程仓库

- `github` → GitHub（自动部署 Pages）
- `origin` → Gitee（手动更新 Pages）

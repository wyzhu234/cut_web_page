#!/usr/bin/env python3
"""递归扫描所有 HTML 文件，生成静态导航页 index.html"""

import os
import re
from html import escape
from urllib.parse import quote

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(REPO_ROOT, "index.html")

# 目录分组配置： (目录路径, 显示名称, 图标)
CATEGORIES = [
    ("dl/yolo",           "YOLO 目标检测",        "🎯"),
    ("dl/1_cnn",          "CNN 卷积神经网络",     "🧠"),
    ("dl/2_transformer",  "Transformer",          "🔄"),
    ("dl/3_rag",          "RAG 检索增强生成",     "📎"),
    ("dl/llm",            "大语言模型",           "🤖"),
    ("dl/conception",     "深度学习概念",         "📐"),
    ("dl/task",           "论文与任务",           "📄"),
    ("dl_cicd",           "CI/CD / 数据标注",     "⚙️"),
    ("dl_deploy",         "模型部署",             "🚀"),
    ("hardware",          "硬件 / 传感器",        "📷"),
    ("clash",             "网络工具",             "🌐"),
    ("tool_develop",      "开发工具",             "🛠"),
    ("cv",                "计算机视觉",           "👁"),
    ("robot",             "机器人",               "🤖"),
    ("package_python",    "Python 生态",          "🐍"),
    ("package_cpp",       "C++ 生态",             "⚡"),
    ("",                  "根目录",               "📁"),
]


def collect_html_files(root_dir, subdir):
    """递归收集子目录下所有 .html 文件"""
    base = os.path.join(root_dir, subdir) if subdir else root_dir
    files = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for f in sorted(filenames, key=lambda x: x.lower()):
            if f.endswith(".html"):
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root_dir)
                # 获取相对于 category 的显示名（保留子目录路径）
                display = os.path.splitext(f)[0]
                files.append((rel, display))
    return files


def build_css():
    return """<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, 'Segoe UI', system-ui, sans-serif;
           background: #f5f5f5; color: #333; }
    .layout { display: flex; max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    /* 左侧导航栏 */
    .sidebar { width: 180px; flex-shrink: 0; position: sticky; top: 0;
               height: 100vh; overflow-y: auto; padding: 30px 0 20px;
               border-right: 1px solid #e0e0e0; margin-right: 30px; }
    .sidebar h3 { font-size: 13px; color: #999; margin-bottom: 10px;
                  padding-left: 12px; font-weight: 600; letter-spacing: 1px; }
    .sidebar a { display: block; padding: 6px 12px; color: #555; text-decoration: none;
                 font-size: 13.5px; border-radius: 6px; margin-bottom: 2px;
                 overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
                 transition: background .15s; }
    .sidebar a:hover { background: #e8f0fe; color: #0366d6; }
    .sidebar a .icon { margin-right: 4px; }
    /* 右侧主内容 */
    .main { flex: 1; min-width: 0; padding: 30px 0; }
    h1 { font-size: 26px; margin-bottom: 4px; }
    .subtitle { color: #666; margin-bottom: 24px; font-size: 14px; }
    .category { background: #fff; border-radius: 8px; padding: 20px; margin-bottom: 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,.08); }
    .category h2 { font-size: 17px; margin-bottom: 10px; padding-bottom: 6px;
                   border-bottom: 2px solid #e8e8e8; color: #2c3e50; }
    .category h2 .count { font-size: 12px; color: #999; font-weight: normal; margin-left: 6px; }
    .file-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2px; }
    .file-list a { display: block; padding: 5px 8px; color: #0366d6; text-decoration: none;
                   font-size: 13.5px; border-radius: 4px; overflow: hidden;
                   text-overflow: ellipsis; white-space: nowrap; }
    .file-list a:hover { background: #f0f6ff; }
    .file-list .subdir-label { grid-column: 1 / -1; font-size: 12px; color: #999;
                               padding: 8px 8px 2px; margin-top: 4px; border-top: 1px dashed #eee; }
    .search-box { width: 100%; padding: 10px 14px; font-size: 15px; border: 2px solid #ddd;
                  border-radius: 8px; margin-bottom: 20px; outline: none; transition: .2s; }
    .search-box:focus { border-color: #0366d6; }
    /* 移动端适配：侧边栏折叠到顶部 */
    @media (max-width: 768px) {
        .layout { flex-direction: column; }
        .sidebar { width: 100%; height: auto; position: static;
                   border-right: none; border-bottom: 1px solid #e0e0e0;
                   padding: 15px 0; margin-right: 0; display: flex; flex-wrap: wrap; gap: 4px; }
        .sidebar h3 { display: none; }
        .sidebar a { font-size: 12px; padding: 4px 10px; }
    }
</style>"""


def build_js():
    return """<script>
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', function() {
    const q = this.value.toLowerCase().trim();
    document.querySelectorAll('.category').forEach(cat => {
        let visible = false;
        cat.querySelectorAll('.file-list a').forEach(a => {
            const match = !q || a.textContent.toLowerCase().includes(q);
            a.style.display = match ? '' : 'none';
            if (match) visible = true;
        });
        cat.style.display = (!q || visible) ? '' : 'none';
    });
});
</script>"""


def build_section(cat_path, icon, name, files, section_id):
    if not files:
        return "", ""

    # 按子目录分组
    groups = {}
    for rel, display in files:
        dir_part = os.path.dirname(rel)
        # 去掉 category 前缀
        if cat_path:
            prefix = cat_path + "/"
            sub = dir_part[len(prefix):] if dir_part.startswith(prefix) else dir_part
        else:
            sub = dir_part
        groups.setdefault(sub, []).append((rel, display))

    lines = []
    lines.append(f'<div class="category" id="{section_id}">')
    lines.append(f'  <h2>{icon} {name} <span class="count">({len(files)} 篇)</span></h2>')
    lines.append(f'  <div class="file-list">')

    # 根目录中的文件优先
    root_files = groups.pop("", [])
    for rel, display in root_files:
        href = quote(rel)
        lines.append(f'    <a href="{href}" title="{escape(display)}">{escape(display)}</a>')

    # 子目录分组
    for sub in sorted(groups.keys()):
        # 跳过太深的嵌套，展示时用 "›" 表示层级
        parts = sub.split("/")
        label = " › ".join(parts)
        lines.append(f'    <div class="subdir-label">📂 {escape(label)}</div>')
        for rel, display in groups[sub]:
            href = quote(rel)
            lines.append(f'    <a href="{href}" title="{escape(display)}">{escape(display)}</a>')

    lines.append('  </div>')
    lines.append('</div>')
    return "\n".join(lines), name


def slugify(name):
    """将中文名转为拼音风格的 id"""
    s = name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    return re.sub(r'[^a-zA-Z0-9_一-鿿]', '', s)


def main():
    seen = set()        # 已分配的 relpath，避免重复
    sections_html = []
    sidebar_links = []  # (section_id, icon, name)

    # 先处理子目录分类，标记已分配的文件
    for cat_path, name, icon in CATEGORIES:
        if not cat_path:
            continue
        files = collect_html_files(REPO_ROOT, cat_path)
        if not files:
            continue
        for rel, _display in files:
            seen.add(rel)
        section_id = slugify(name)
        html, _ = build_section(cat_path, icon, name, files, section_id)
        if html:
            sections_html.append(html)
            sidebar_links.append((section_id, icon, name))

    # 最后处理根目录（仅包含未被分类的文件）
    root_files = collect_html_files(REPO_ROOT, "")
    root_files = [(r, d) for r, d in root_files if r not in seen]
    if root_files:
        section_id = "root"
        html, _ = build_section("", "📁", "根目录", root_files, section_id)
        if html:
            sections_html.append(html)
            sidebar_links.append((section_id, "📁", "根目录"))

    total = len(seen) + len(root_files)

    # 构建侧边栏
    sidebar_items = "\n".join(
        f'      <a href="#{sid}"><span class="icon">{ico}</span>{nm}</a>'
        for sid, ico, nm in sidebar_links
    )

    sections_body = "\n".join(sections_html)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>学习笔记导航</title>
  {build_css()}
</head>
<body>
<div class="layout">
  <div class="sidebar">
    <h3>📂 分类导航</h3>
{sidebar_items}
  </div>
  <div class="main">
    <h1>📚 学习笔记</h1>
    <p class="subtitle">深度学习 / 计算机视觉 / 工程实践 · 共 {total} 篇</p>
    <input type="text" id="search" class="search-box" placeholder="🔍 搜索笔记标题..." autofocus>
    {sections_body}
    <p style="text-align:center;color:#999;font-size:12px;margin:40px 0;">自动生成于 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
  </div>
</div>
{build_js()}
</body>
</html>"""

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 导航页已生成: {OUTPUT} ({total} 篇)")


if __name__ == "__main__":
    main()

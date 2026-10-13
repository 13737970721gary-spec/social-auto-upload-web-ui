# 图标说明

## 主图标

- **`icon.png`**（1024×1024，~64KB）—— electron-builder 自动识别为主图标
  - macOS：自动生成 `.icns`（需要在 macOS 上用 `iconutil`）
  - Windows：自动生成 `.ico`（multi-size）
  - Linux：自动缩放至 512/256/128 等
- **`icon.svg`**（矢量版）—— 可在 Figma/Illustrator 中二次修改

## 设计

- 圆角矩形（半径 224px ≈ macOS Big Sur 标准）
- 渐变：`#4F46E5` (indigo) → `#2563EB` (blue) → `#06B6D4` (cyan)，呼应「千帆」海天意象
- 主元素：白色「千」字（微软雅黑 Bold，720pt），加柔阴影
- 装饰：底部两道斜线（极低透明度 28/18），象征航行

## 重新生成

如需调整设计（颜色、字号、装饰），编辑 `icon.svg` 或修改原 Python 脚本（脚本可让 Cursor/Claude 重新生成）。
原脚本逻辑已删除（保持目录干净），需要时根据 `icon.svg` 反推。

## 多尺寸（可选）

正式发布前可生成多套：

```bash
# Windows ICO（用 ImageMagick 或 Pillow）
# macOS ICNS（在 macOS 上执行：iconutil -c icns icon.iconset/）
# Linux: 保持 PNG 即可，electron-builder 自动缩放
```
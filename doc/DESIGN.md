The core pillars of the new design:
- [ ] The action-driven time system (every keypress advances the clock).
- [ ] The message log UI.
- [ ] interacting with objects.
- [ ] The data structure for crafting recipes.

# 实现

1. 颜色方案：使用不同的颜色区分各种元素：
   - 背景色: 羊皮纸色 #F5F0E5
   - 文字主色/墙壁/脏地板: 深褐色 #3A2E2A
   - 干净地板(.): #C4BAA3 (浅灰褐色)
   - 玩家(@): #A52A2A (深红色) 
   - 门(+): #8B4513 (深 saddle brown)
   - 强调色/可交互物品: #556B2F (深绿色)
2. 交互设计
   - 消息日志支持滚动以查看历史消息（使用Page Up/Page Down键）。
   - 操作菜单根据上下文动态更新显示的可操作命令。
- [ ] The data structure for crafting recipes.

# 实现

1. 交互设计
   - 消息日志支持滚动以查看历史消息（使用Page Up/Page Down键）。
   - 操作菜单根据上下文动态更新显示的可操作命令。
     - 当有可收获对象时，显示: (H)arvest | (L)ook | (I)nventory
     - 按下'E'键进入检查模式
     - 显示所有附近可检查对象，如: 
     - (B)rewing Tower | (S)ilver Leaf | (C)ancel
     - (B)rewing Tower | (R)usted Pipe | (A)nvil | (C)ancel
     - (C)rystal | (B)ack

# 优先开发清单

1. 「家园修复」核心玩法
    - 一个问题：从主工作区开始，看到主酿造台的一根堵塞管道
    - 一次采集：前往香草培育室采集银叶和酸柠檬果
    - 一次制作：返回工作台制作简易清洁膏
    - 一次修复：成功疏通一根管道
    - 视觉/文本反馈：收到导师的魔法传信，给予鼓励和感谢
2. 丰富的环境叙事与氛围营造
   - 工坊描述：每个区域都有详细的、沉浸式的文本描述
   - 导师痕迹：到处散落着希尔达的个人物品和笔记，展现她的性格
   - 小细节：那把「焦虑的扫帚」等小元素立即建立独特的世界观
3. 「非战斗」互动系统
    - 安抚扫帚：实现「同步节奏」安抚机制
    - 检查工具：可以检查工坊工具并获取描述
    - 阅读笔记：与导师的笔记和书籍互动
4. 简洁但有效的制作系统
    - 实现 2-3 个简单配方（如清洁膏、基础药剂）
    - 专注于流程而非复杂合成：收集材料 -> 前往工作台 -> 选择配方 -> 制作
5. 时间与进度系统
   - 实现简单的行动消耗时间机制
   - 显示当前天数/时间（如「第3天，上午」）
   - 显示主要任务进度（如「订单剩余时间：5天」）
6. 库存系统：
   - 只需实现物品的获取和使用
   - 简单列出物品而非复杂网格界面
7. 地图
    - 不需要多层或复杂地图
    - 专注于把核心区域（工作区、培育室、储藏室）做细致

# Creating Distinctive Interactions

1. Gentle, non-violent interactions:
```py
actions = {
    "Comfort": lambda obj, game: "The anxious broom calms down and begins sweeping properly.",
    "Prune": lambda obj, game: "You carefully trim the overgrown plant, encouraging healthy growth.",
    "Organize": lambda obj, game: "You sort the scattered components into neat piles."
}
```
2. Progress through crafting and repair:

```py
def fix_pipe_callback(obj, game):
    if game.player.has_tool("Wrench"):
        game.world_state["fixed_pipes"] += 1
        return "You tighten the fittings, stopping the leak."
    return "You need a wrench to fix this properly."
```
3. Atmospheric interactions:
```py
def listen_callback(obj, game):
   sounds = [
        "The gentle hum of magic permeates the air.",
        "Somewhere, water drips rhythmically.",
        "You hear the faint rustling of plants growing."
   ]
   return random.choice(sounds)
```
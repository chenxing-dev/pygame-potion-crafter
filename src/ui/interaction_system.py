
from typing import TYPE_CHECKING, List, Tuple
import pygame

if TYPE_CHECKING:
    from game import Game


class InteractionSystem:
    def __init__(self, game: 'Game'):
        self.game = game
        self.world = game.world
        self.interaction_mode = None
        self.available_targets = []
        self.cancel_key = "C"  # 默认取消键
        self.cancel_text = "(C)ancel"

        # 定义交互动作
        self.interaction_types = {
            "clean": "C",
            "examine": "E",
            "harvest": "H",
            "open": "O",
            "close": "O",
            "talk": "T",
            "use": "U",
        }

    def get_available_interactions(self):
        """获取玩家当前位置可用的交互动作"""
        available = set()

        for action_type, key in self.interaction_types.items():
            # 检查附近是否有此类可交互对象
            targets, _ = self.get_nearby_interaction_targets(action_type)
            if targets:
                available.add((action_type, key))

        return list(available)

    def get_nearby_interaction_targets(self, action_type: str) -> Tuple[List[dict], set]:
        """获取玩家附近可交互的对象"""
        if not self.world or not self.game.player:
            return [], set()

        directions = [(0, 0), (0, -1), (-1, 0), (1, 0), (0, 1)]
        # Check all 4 directions around player plus current position
        targets = []
        used_keys = set()

        for dx, dy in directions:
            x, y = self.game.player.x + dx, self.game.player.y + dy

            # Check for objects at this position
            for ref in self.world.references:
                if ref.x == x and ref.y == y:
                    # Check if the object has a get_actions method
                    if hasattr(ref, "get_actions") and action_type in ref.object.get_actions():
                        # 为每个对象生成唯一的选择键
                        key = self.get_unique_key(ref.name, targets)
                        used_keys.add(key)
                        targets.append({"key": key, "object": ref,
                                        "position": (x, y), "name": ref.name})

        return targets, used_keys

    def get_unique_key(self, name, used_keys):
        """为对象生成唯一的选择键（首字母）"""

        # 尝试使用名称中的每个字母
        for char in name:
            if char.isalpha() and char.upper():
                if char.upper() not in used_keys:
                    return char.upper()

        # 如果所有字母都被使用，返回数字键
        for i in range(1, 10):
            num_key = str(i)
            if num_key not in used_keys:
                return num_key

        # Fallback: 使用*
        return "*"

    def start_interaction(self, action_type):
        """开始交互模式"""
        self.interaction_mode = action_type
        self.available_targets, used_keys = self.get_nearby_interaction_targets(
            action_type)

        # 确定取消键
        self.cancel_key, self.cancel_text = self.get_cancel_key(used_keys)

    def get_cancel_key(self, used_keys) -> Tuple[str, str]:
        """获取唯一的取消键"""
        # Try 'C' first
        if "C" not in used_keys:
            return "C", "ancel"
        # 尝试B (Back)
        if "B" not in used_keys:
            return "B", "ack"
        # 尝试X (eXit)
        if "X" not in used_keys:
            return "X", " Exit"
        # 尝试Z (cancel)
        if "Z" not in used_keys:
            return "Z", " Cancel"
        # Final fallback
        return "*", " Cancel"

    def handle_interaction_input(self, key):
        """处理交互模式下的输入"""
        key_char = pygame.key.name(key).upper()

        # 检查是否按下了取消键
        if key_char == self.cancel_key:
            self.cancel_interaction()
            return True

        # 检查是否按下了某个目标的选择键
        if self.interaction_mode and self.available_targets:
            for target in self.available_targets:
                if target['key'] == key_char:
                    self.perform_action(target['object'])
                    return True

        return False

    def perform_action(self, target_object):
        """在目标对象上执行交互动作"""
        result = target_object.activate(self.interaction_mode, self.game)
        if result:
            self.game.add_message(result)
        self.cancel_interaction()

    def cancel_interaction(self):
        """取消交互模式"""
        self.interaction_mode = None
        self.available_targets = []

    def get_interaction_menu_items(self):
        """获取当前交互菜单项"""
        if not self.interaction_mode or not self.available_targets:
            return []

        menu_items = []
        # 添加目标选项
        for target in self.available_targets:
            if target['key'] == target['name'][0].upper():
                menu_items.append((target['key'], target['name'][1:]))
            else:
                menu_items.append((target['key'], f" {target['name']}"))

        # 添加取消选项
        menu_items.append((self.cancel_key, self.cancel_text))

        return menu_items

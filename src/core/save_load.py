"""保存和加载游戏状态的功能模块"""
import json
import os
from typing import TYPE_CHECKING
from datetime import datetime
from config import CURRENT_VERSION

if TYPE_CHECKING:
    from game import Game


class SaveLoadSystem:
    """保存和加载游戏状态的系统"""

    def __init__(self, game: 'Game'):
        self.game = game
        self.save_dir = "saves"
        self.save_slots = 3  # 默认保存槽数量
        self.current_slot = 1  # 当前使用的保存槽
        self.save_file = "save_slot_1.json"  # 默认保存文件名
        print("SaveLoadSystem initialized.")

    def save_game(self, slot: int) -> bool:
        """将游戏状态保存到slot指定的文件中"""
        if slot is None:
            slot = self.current_slot

        if slot < 1 or slot > self.save_slots:
            print(f"Invalid save slot: {slot}")
            return False

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir, exist_ok=True)

        try:
            # Prepare data to save
            save_data = self.prepare_save_data()

            # Write to file
            filename = f"save_slot_{slot}.json"
            filepath = os.path.join(self.save_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)  # Plain JSON for readability

            # Update save metadata
            self.update_save_metadata(slot, save_data)

            self.game.message_log.add_message(f"Game saved to slot {slot}.")
            print(f"Game saved to {filepath}")
            return True

        except (OSError, IOError, TypeError, ValueError, json.JSONDecodeError) as e:
            print(f"Error saving game: {e}")
            self.game.message_log.add_message("Error saving game.")
            return False

    def update_save_metadata(self, slot: int, save_data: dict):
        """"更新保存文件的元数据"""
        try:
            # Load existing metadata
            metadata_file = os.path.join(self.save_dir, "metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {}

            # Update metadata for the specific slot
            if "saves" not in metadata:
                metadata["saves"] = {}

            metadata["saves"][str(slot)] = {
                "day": save_data.get("world_state", {}).get("day", 1),
                "progress": save_data.get("world_state", {}).get("progress", 0),
                "skills": save_data.get("mobile_player", {}).get("skills", {}),
                "timestamp": save_data.get("timestamp", datetime.now().isoformat()),
            }

            # Save updated metadata back to file
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
        except (OSError, IOError, TypeError, ValueError, json.JSONDecodeError) as e:
            print(f"Error updating save metadata: {e}")

    def load_game(self, slot: int) -> bool:
        """从slot指定的文件中加载游戏状态"""
        if slot < 1 or slot > self.save_slots:
            print(f"Invalid save slot: {slot}")
            return False
        try:
            filename = f"save_slot_{slot}.json"
            filepath = os.path.join(self.save_dir, filename)

            # Check if file exists
            if not os.path.exists(filepath):
                print(f"No save file found at {filepath}")
                return False

            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Apply loaded data to game state
            self.apply_save_data(save_data)

            print(f"Game loaded from {filepath}")
            return True
        except (OSError, IOError, TypeError, ValueError, json.JSONDecodeError) as e:
            print(f"Error loading game: {e}")
            self.game.message_log.add_message("Error loading game.")
            return False

    def prepare_save_data(self) -> dict:
        """准备要保存的数据字典"""
        save_data = {
            "version": CURRENT_VERSION,
            "timestamp": datetime.now().isoformat(),
            "game": self.game.to_dict(),
        }
        return save_data

    def apply_save_data(self, save_data: dict):
        """将加载的数据应用到游戏状态"""
        # Check version compatibility
        if save_data.get("version") != CURRENT_VERSION:
            print(
                f"Incompatible save file version: {save_data.get('version')} != {CURRENT_VERSION}")
            self.game.message_log.add_message(
                "Warning: Save file version may be incompatible.")

        self.game.from_dict(save_data.get("game", {}))

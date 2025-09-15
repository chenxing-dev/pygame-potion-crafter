from typing import Dict, List, Optional

from crafting.crafting_recipe import CraftingRecipe


class RecipeManager:
    """管理所有制作配方"""

    def __init__(self):
        self.recipes: Dict[str, 'CraftingRecipe'] = {}
        self.recipes_by_category: Dict[str, List['CraftingRecipe']] = {}
        self.recipes_by_tag: Dict[str, List['CraftingRecipe']] = {}

    def add_recipe(self, recipe: 'CraftingRecipe'):
        """添加新配方"""
        self.recipes[recipe.id] = recipe
        # 按类别索引配方
        if recipe.category not in self.recipes_by_category:
            self.recipes_by_category[recipe.category] = []
        self.recipes_by_category[recipe.category].append(recipe)
        # 按标签索引配方
        for tag in recipe.tags:
            if tag not in self.recipes_by_tag:
                self.recipes_by_tag[tag] = []
            self.recipes_by_tag[tag].append(recipe)

    def get_recipe(self, recipe_id: str) -> Optional[CraftingRecipe]:
        """根据ID获取配方"""
        return self.recipes.get(recipe_id)

    def get_recipes_by_category(self, category: str) -> List[CraftingRecipe]:
        """根据类别获取所有配方"""
        return self.recipes_by_category.get(category, [])

    def get_recipes_by_tag(self, tag: str) -> List[CraftingRecipe]:
        """根据标签获取所有配方"""
        return self.recipes_by_tag.get(tag, [])

    def find_recipes_by_ingredient(self, item_id: str) -> List[CraftingRecipe]:
        """查找包含指定原料的所有配方"""
        result = []
        for recipe in self.recipes.values():
            if any(ing.item_id == item_id for ing in recipe.ingredients):
                result.append(recipe)
        return result

    def find_recipes_by_station(self, station_id: str) -> List[CraftingRecipe]:
        """查找在指定工作台可制作的所有配方"""
        return [r for r in self.recipes.values() if r.required_station == station_id]

    def find_recipes_by_tool(self, tool_id: str) -> List[CraftingRecipe]:
        """查找使用指定工具可制作的所有配方"""
        return [r for r in self.recipes.values() if r.required_tool == tool_id]

    def get_available_recipes(self, inventory: Dict[str, int],
                              station: Optional[str] = None,
                              tools: Optional[List[str]] = None,
                              skills: Optional[Dict[str, int]] = None) -> List[CraftingRecipe]:
        """获取玩家当前可制作的所有配方"""
        available = []
        for recipe in self.recipes.values():
            can_craft = True
            # 检查是否有足够的原料
            for ing in recipe.ingredients:
                if inventory.get(ing.item_id, 0) < ing.quantity:
                    can_craft = False
                    break

            # 检查工作台要求
            if recipe.required_station and recipe.required_station != station:
                can_craft = False

            # 检查工具要求
            if can_craft and recipe.required_tool:
                if not tools or recipe.required_tool not in tools:
                    can_craft = False

            # 检查技能要求
            if can_craft and recipe.required_skill and skills:
                for skill, level in recipe.required_skill.items():
                    if skills.get(skill, 0) < level:
                        can_craft = False
                        break

            if can_craft:
                available.append(recipe)

        return available

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Ingredient:
    """配方原料"""
    item_id: str  # 物品ID
    quantity: int  # 所需数量


@dataclass
class CraftingRecipe:
    """制作配方"""
    id: str  # 配方ID
    name: str  # 配方名称
    description: str  # 配方描述
    ingredients: List[Ingredient]  # 所需原料列表
    result: Ingredient  # 产出物品
    required_station: Optional[str] = None  # 所需工作台
    required_tool: Optional[str] = None  # 所需工具
    time: int = 1  # 制作时间，单位为回合
    required_skill: Optional[Dict[str, int]] = None  # 所需技能及等级

    # 配方分类和标签
    category: str = "General"  # 配方类别
    tags: List[str] = field(default_factory=list)  # 配方标签

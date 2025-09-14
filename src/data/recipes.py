from crafting import CraftingRecipe, Ingredient, RecipeManager


def load_recipes(recipe_manager: RecipeManager):
    # 添加清洁膏配方
    recipe_manager.add_recipe(
        CraftingRecipe(
            id="cleaning_gloop",
            name="Cleaning Gloop",
            description="A sticky substance used for cleaning.",
            ingredients=[
                Ingredient(item_id="silver_leaf", quantity=3),
                Ingredient(item_id="lemon", quantity=1),
            ],
            result=Ingredient(item_id="cleaning_gloop", quantity=1),
            required_station="workbench",
            time=2,
            category="Alchemy",
            tags=["cleaning"],
        )
    )

    # 添加荧光菇精华配方
    recipe_manager.add_recipe(
        CraftingRecipe(
            id="glowshroom_essence",
            name="Glowshroom Essence",
            description="A luminous essence extracted from glowshrooms.",
            ingredients=[
                Ingredient(item_id="glowshroom", quantity=5),
                Ingredient(item_id="moon_dew", quantity=2),
                Ingredient(item_id="glowing_moss", quantity=1),
            ],
            result=Ingredient(item_id="glowshroom_essence", quantity=1),
            required_station="brewing_station",
            time=50,
            category="Alchemy",
            tags=["magical", "order"],
        )
    )

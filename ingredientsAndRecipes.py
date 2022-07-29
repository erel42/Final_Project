import random

ing_dic = {
    "tomato": 0,
    "patty": 1,
    "pickles": 2,
    "hamburger_buns": 3,
    "pasta": 4,
    "tomato_sauce": 5
}

ing_list = list(ing_dic.keys())

num_of_ingredients = len(ing_dic.keys())

meal_dic = {
    "burger": 0,
    "pasta": 1,
}

meal_list = list(meal_dic.keys())

meal_count = len(meal_dic)

meal_revenue = [50]*meal_count
meal_max = [60]*meal_count  # The maximum price of a meal
meal_min = [30]*meal_count  # The minimum price of a meal

supplier_names = ["Foody", "Burgers and co", "All about that bass"]
num_of_ing_suppliers = len(supplier_names)
supplier_prices = [[50]*num_of_ingredients] * num_of_ing_suppliers
max_price = 100  # The maximum price of an ingredient
min_price = 10  # The minimum price of an ingredient


def update_prices():
    for j in range(0, num_of_ing_suppliers):
        price_list = supplier_prices[j][:]
        for i in range(0, num_of_ingredients):
            ing = price_list[i]
            ing = int(ing * random.uniform(0.85, 1.15))
            if ing > max_price:
                ing = max_price
            elif ing < min_price:
                ing = min_price
            price_list[i] = ing
        supplier_prices[j] = price_list[:]
    for i in range(0, meal_count):
        meal = meal_revenue[i]
        meal = int(meal * random.uniform(0.85, 1.15))
        if meal > meal_max[i]:
            meal = meal_max[i]
        elif meal < meal_min[i]:
            meal = meal_min[i]
        meal_revenue[i] = meal


class Recipe:
    def __init__(self):
        self.ing_list = [0]*num_of_ingredients
        self.meal_index = 0

    def use_ing(self, stock: list, times_to_cook: int):
        for i in range(0, num_of_ingredients):
            if stock[i] < times_to_cook and self.ing_list[i] != 0:
                times_to_cook = stock[i]
        for i in range(0, num_of_ingredients):
            stock[i] = stock[i] - self.ing_list[i] * times_to_cook
        return times_to_cook * meal_revenue[self.meal_index]


class BurgerRecipe(Recipe):
    def __init__(self):
        super().__init__()
        self.ing_list[ing_dic["tomato"]] = 1
        self.ing_list[ing_dic["patty"]] = 1
        self.ing_list[ing_dic["pickles"]] = 1
        self.ing_list[ing_dic["hamburger_buns"]] = 1

        self.meal_index = meal_dic["burger"]


class PastaRecipe(Recipe):
    def __init__(self):
        super().__init__()
        self.ing_list[ing_dic["tomato"]] = 1
        self.ing_list[ing_dic["pasta"]] = 1
        self.ing_list[ing_dic["tomato_sauce"]] = 1

        self.meal_index = meal_dic["pasta"]


recipes = [BurgerRecipe(), PastaRecipe()]



ing_dic = {
    "tomato": 0,
    "patty": 1,
    "pickles": 2,
    "hamburger buns": 3,
}

num_of_ingredients = len(ing_dic.keys())

supplier_names = ["Foody", "Burgers and co", "All about that bass"]
num_of_ing_suppliers = len(supplier_names)
supplier_prices = [[50]*num_of_ingredients] * num_of_ing_suppliers

meal_dic = {
    "burger": 0,
}

meal_revenue = [10]*len(meal_dic)


class Recipe:
    ing_list = [0]*num_of_ingredients
    meal_index = 0

    def use_ing(self, stock: list, times_to_cook: int):
        for i in range(0, num_of_ingredients):
            if stock[i] < times_to_cook and self.ing_list[i] != 0:
                times_to_cook = stock[i]
        for i in range(0, num_of_ingredients):
            stock[i] = stock[i] - self.ing_list[i] * times_to_cook
        return times_to_cook * meal_revenue[self.meal_index]


class BurgerRecipe(Recipe):
    def __init__(self):
        self.ing_list[ing_dic["tomato"]] = 1
        self.ing_list[ing_dic["patty"]] = 1
        self.ing_list[ing_dic["pickles"]] = 1
        self.ing_list[ing_dic["hamburger buns"]] = 1

        self.meal_index = meal_dic["burger"]

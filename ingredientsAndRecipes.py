

ing_dic = {
    "tomato": 0,
    "patty": 1,
    "pickles": 2,
    "hamburger buns": 3,
}

num_of_ingredients = len(ing_dic.keys())


class Recipe:
    ing_list = [None]*num_of_ingredients

    def can_cook(self, stock: list):
        result = True
        for i in range(0, num_of_ingredients):
            result = result and stock[i] >= self.ing_list[i]
        return result

    def use_ing(self, stock: list):
        for i in range(0, num_of_ingredients):
            stock[i] = stock[i] - self.ing_list[i]

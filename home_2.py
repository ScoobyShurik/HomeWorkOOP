
def read_cook_book(file_name):
    cook_book = {}
    with open(file_name, 'r', encoding='utf-8') as file:
        while True:
            dish_name = file.readline().strip()
            if not dish_name:
                break
            ingredient_count = int(file.readline().strip())
            ingredients = []
            for _ in range(ingredient_count):
                line = file.readline().strip()
                ingredient_name, quantity, measure = line.split(' | ')
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'quantity': int(quantity),
                    'measure': measure
                })
            cook_book[dish_name] = ingredients
            file.readline()
    return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}

    for dish in dishes:
        for ingredient in recipes[dish]:
            ingredient_name = ingredient['ingredient_name']
            quantity = ingredient['quantity'] * person_count
            measure = ingredient['measure']
            if ingredient_name in shop_list:
                shop_list[ingredient_name]['quantity'] += quantity
            else:
                shop_list[ingredient_name] = {
                    'measure': measure,
                    'quantity': quantity
                }
    return shop_list



if __name__ == "__main__":
    recipes = read_cook_book('recipes.txt')
    print(recipes)
    print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
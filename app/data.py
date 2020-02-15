import pickle

with open("data.pickle", "rb") as f:
    full_recipe_data = pickle.load(f)


# restructure the data
# there are 8 recipes in the data with multi part instructions we are only
# showing the first part for simplicity 238 recipes have one section of steps
recipe_data = {
    recipe["id"]: {
        "steps": [step["step"] for step in recipe["analyzedInstructions"][0]["steps"]],
        "name": recipe["title"],
        "image": recipe["image"],
        "likes": recipe["aggregateLikes"],
        "ingredients": {
            ing["id"]: {
                "name": ing["name"],
                "string": ing["originalString"],
                "amount": ing["amount"],
                "unit": ing["unit"],
            }
            for ing in recipe["extendedIngredients"]
        },
    }
    for recipe in full_recipe_data
}


class Recipe:
    def __init__(self, spoonacular_id):
        self.id = spoonacular_id
        rdict = recipe_data[int(spoonacular_id)]

        self.image = rdict["image"]
        self.ingredients = rdict["ingredients"]
        self.likes = rdict["likes"]
        self.name = rdict["name"]
        self.steps =rdict["steps"]

    def _diff_ingredients(self, r):
        """ returns ingredients that are added in r, and ingredients that are
        removed from this recipe and present in r """
        our_ings = set(self.ingredients)
        r_ings = set(r.ingredients)

        # exclusive to r
        added = {id:r.ingredients[id] for id in r_ings.difference(our_ings)}

        # exclusive to this recipe
        removed = {id:self.ingredients[id] for id in our_ings.difference(r_ings)}

        return added, removed

    def ingredients_added_in(self, other):
        """Returns a list of ingredient names exclusive to other"""
        added, _ = self._diff_ingredients(other)
        return [d["name"]   for d in added.values() ]

    def ingredients_removed_from(self, other):
        """Returns a list of ingredient names exclusive to this recipe"""
        _, removed = self._diff_ingredients(other)
        return [d["name"]   for d in removed.values() ]

    def similarity(self, other):
        """Returns the length of the set of the symmetric difference, the total
        number of items not in common"""

        our_ings = set(self.ingredients)
        other_ings = set(other.ingredients)
        return len(our_ings.symmetric_difference(other_ings))



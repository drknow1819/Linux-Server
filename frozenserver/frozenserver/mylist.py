from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup import User, Base, Item, Category

engine = create_engine('postgresql+psycopg2://postgres:test@localhost/frozen')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Hany Mikhael", email="frozenmarket@example.com",
             picture='https://lh4.googleusercontent.com/-02tSrDVwrUo'
                     '/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdhdrCYkyfxqiiZU4RUX'
                     '-FsRUe1AQ/s96-c/photo.jpg')
session.add(User1)
session.commit()

# List for Meat
category1 = Category(user_id=1, name="Meat",
                     description="Meat is animal flesh that is eaten as "
                                 "food. Humans have hunted and killed "
                                 "animals for meat since prehistoric times. "
                                 "The advent of civilization allowed the "
                                 "domestication of animals such as "
                                 "chickens, sheep, rabbits, pigs and cattle.")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Bacon",
             nutrients="One 10-g slice of cooked side bacon contains 4.5 g "
                       "of fat, 3.0 g of protein, and 205 mg of sodium.",
             price="$7.50", weight="100 grams", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Chicken Breasts",
             nutrients="A whole chicken breast with skin provides 366 "
                       "calories, 55 grams of protein, 0 grams of "
                       "carbohydrate, 14 grams of fat, 4 grams of saturated "
                       "fat and 132 milligrams of sodium.",
             price="$12.99", weight="500 grams", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Minced Meat",
             nutrients="Minced Beef 80% Lean 20% Fat", price="$9.50",
             weight="250 grams", category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Hot dogs",
             nutrients="A beef hot dog contains 5 g of protein, less than 2 "
                       "g of carbohydrates, no fiber, small amounts of "
                       "sugar and a trace amount of iron",
             price="$6.99", weight="250 grams", category=category1)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="Beef Steak",
             nutrients="Made with grade A beef contains about 158 calories, "
                       "just over 5 grams of fat, zero carbohydrates and a "
                       "whopping 26 grams of protein",
             price="$15.99", weight="250 grams", category=category1)

session.add(item5)
session.commit()

# List for Seafood

category2 = Category(user_id=1, name="Seafood",
                     description="Seafood is any form of sea life regarded "
                                 "as food by humans. Seafood prominently "
                                 "includes fish and shellfish. Shellfish "
                                 "include various species of molluscs, "
                                 "crustaceans, and echinoderms.")

session.add(category2)
session.commit()

item1 = Item(user_id=1, name="Pacific cod",
             nutrients="Cod is a low fat flaky white meat fish that is a "
                       "good source of protein, phosphorus, niacin, "
                       "and Vitamin B-12. A 3 ounce cooked portion of cod "
                       "has less than 90 calories and one gram of fat, "
                       "and 15 to 20 grams of protein.",
             price="$17.99", weight="250 grams", category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Sockeye salmon",
             nutrients="Wild sockeye salmon is a rich protein source, "
                       "with nearly 16 g of protein in each 3-oz. serving. "
                       "Each portion also contains close to 35 g of sodium, "
                       "318.9 g of potassium and 6 mg of calcium. Canning "
                       "salmon with the bones increases the calcium content "
                       "to 188 mg per serving.",
             price="$15.99", weight="250 grams", category=category2)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Shrimp",
             nutrients="Shrimp is high in cholesterol, but it also contains "
                       "nutrients including antioxidants and omega-3 fatty "
                       "acids, which have been shown to promote heart health",
             price="$23.49", weight="1 KG", category=category2)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Squid",
             nutrients="Squid contains 78 calories, composed of about 70 "
                       "percent protein, 15 percent carbohydrates and 15 "
                       "percent fat per serving",
             price="$15.99", weight="1 KG", category=category2)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="King Crab Legs",
             nutrients="(134g serving (or 1 leg), calories 130, calories "
                       "from fat 18.5, total fat 2.06g, saturated fat 0g, "
                       "trans fat 0g, cholesterol 71mg, sodium 1436mg, "
                       "total carbohydrate 0g, dietary fiber 0g, sugars 0g, "
                       "protein 25.93g, vitamin a >1%, vitamin c 1.7%, "
                       "calcium 7.9%, iron 5.6%.",
             price="$25.99", weight="500 grams", category=category2)

session.add(item5)
session.commit()

# List of Pizza
category3 = Category(user_id=1, name="Pizza",
                     description="Pizza is a savory dish of Italian origin, "
                                 "consisting of a usually round, flattened "
                                 "base of leavened wheat-based dough topped "
                                 "with tomatoes, cheese, and various other "
                                 "ingredients baked at a high temperature, "
                                 "traditionally in a wood-fired oven.")

session.add(category3)
session.commit()

item1 = Item(user_id=1, name="Cheese Pizza",
             nutrients="Fresh spinach and chopped cherry tomatoes, "
                       "less than 5 grams of sugar, and 18 grams of filling "
                       "and satiating protein using only organic "
                       "ingredients.",
             price="$7.99", weight="Medium", category=category3)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Crispy White Pizza",
             nutrients="Lean ground turkey and pairs well with spinach and "
                       "cheese.",
             price="$18", weight="Medium", category=category3)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Pepperoni Pizza",
             nutrients="This pie packs plenty of protein, thanks to the "
                       "pepperoni and cheese added a mix of bell peppers, "
                       "mushrooms, red onions, and zucchini.",
             price="$15", weight="Large", category=category3)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Veggie Pizza",
             nutrients="With only 10 grams of protein per serving, "
                       "this veggie-packed, gluten-free pizza is another "
                       "that needs a protein boost topped with lean chicken "
                       "sausage.",
             price="$17.99", weight="Medium", category=category3)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="Margherita Pizza",
             nutrients="This pizza has less than a gram of added sugar and "
                       "about 15 grams of protein per serving",
             price="$14", weight="Small", category=category3)

session.add(item5)
session.commit()

# List of Vegetables
category4 = Category(user_id=1, name="Vegetables",
                     description="Vegetables are parts of plants that are "
                                 "consumed by humans or other animals as "
                                 "food. The original meaning is still "
                                 "commonly used and is applied to plants "
                                 "collectively to refer to all edible plant "
                                 "matter, including the flowers, fruits, "
                                 "stems, leaves, roots, and seeds.")

session.add(category4)
session.commit()

item1 = Item(user_id=1, name="Broccoli",
             nutrients="high in fiber, very high in vitamin C and has "
                       "potassium, B6 and vitamin A.",
             price="$7.99", weight="1 KG", category=category4)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Brussels Sprouts",
             nutrients="Brussels sprouts are low in calories but high in "
                       "many nutrients, especially fiber, vitamin K and "
                       "vitamin C.",
             price="$18", weight="1 KG", category=category4)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Carrots",
             nutrients="One cup of chopped carrots provides more than 100 "
                       "percent of an average adult male or female's "
                       "recommended daily allowance (RDA) of vitamin A also "
                       "contain various B vitamins.",
             price="$7", weight="1 KG", category=category4)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Corn",
             nutrients="Corn is rich in vitamin C, magnesium, B vitamins "
                       "and carotenoids, such as lutein and zeaxanthin.",
             price="17.99", weight="500 grams", category=category4)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="Spinach",
             nutrients="Dark, leafy greens like spinach are important for "
                       "skin, hair, and bone health. They also provide "
                       "protein, iron, vitamins, and minerals.",
             price="$9", weight="500 grams", category=category4)

session.add(item5)
session.commit()

# List of Fruits
category5 = Category(user_id=1, name="Fruits",
                     description="Most fruits are naturally low in fat, "
                                 "sodium, and calories. None have "
                                 "cholesterol. Fruits are sources of many "
                                 "essential nutrients that are "
                                 "underconsumed, including potassium, "
                                 "dietary fiber, vitamin C, and folate ("
                                 "folic acid). Diets rich in potassium may "
                                 "help to maintain healthy blood pressure.")

session.add(category5)
session.commit()

item1 = Item(user_id=1, name="Strawberries",
             nutrients="One cup of sliced, fresh strawberries contains "
                       "Calories: 53 kcal. Protein: 1.11 g. Carbohydrates: "
                       "12.75 g. Dietary fiber: 3.3 g. Calcium: 27 mg. "
                       "Iron: 0.68 mg. Magnesium: 22 mg. Phosphorus: 40 mg.",
             price="$9.99", weight="1 KG", category=category5)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Blackberries",
             nutrients="This food is very low in Saturated Fat, Cholesterol "
                       "and Sodium. It is also a good source of Vitamin E, "
                       "Folate, Magnesium, Potassium and Copper, and a very "
                       "good source of Dietary Fiber, Vitamin C, Vitamin K "
                       "and Manganese.",
             price="$18", weight="1 KG", category=category5)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Raspberries",
             nutrients="One cup of raspberries (about 123 grams) contains "
                       "64 calories, 1.5 grams of protein, 0.8 grams of "
                       "fat, and 15 grams of carbohydrate (including 8 "
                       "grams of fiber and 5 grams of sugar).",
             price="$7", weight="1 KG", category=category5)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Peaches",
             nutrients="One cup of sliced peach, weighing 154 grams (g) "
                       "contains: 60 calories. 1.4 g of protein. 0.4 g of "
                       "fat. 0 g of cholesterol and sodium. 16.7 g of "
                       "carbohydrate. 13 g of sugar. 2.3 g of fiber. 9 "
                       "milligrams (mg) of calcium.",
             price="17.99", weight="500 grams", category=category5)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="Cherries",
             nutrients="One cup serving of sweet cherries. 16% Vitamin C "
                       "Daily Value. 10% Dietary Fiber Daily Value. Grams "
                       "of fat, sodium, and cholesterol. 260. Milligrams of "
                       "potassium.",
             price="$9.99", weight="500 grams", category=category5)

session.add(item5)
session.commit()

print
"added all items!"

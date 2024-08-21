import operator

grocery_cart = []


def Merge(dict1, dict2, dict3, dict4, dict5, ):
    res = {**dict1, **dict2, **dict3, **dict4, **dict5, }
    return res


d = {"Milk": 2.30, "Butter": 4.50, "Eggs": 3.40, "Cheese slices": 3.15, "Evaporated Milk Creamer": 1.40, "Milo": 12.50,
     "Biscuits": 5.30, "Yogurt": 0.95}
pg = {"Bread": 2.70, "Cereal": 7.00, "Crackers": 3.10, "Chips": 2.60, "Raisin": 2.10, "Nuts": 2.00, "Green Bean": 1.05,
      "Barley": 1.05}
cg = {"Tomato": 1.45, "Button Mushroom": 1.15, "Baking Bean": 1.35, "Tuna Fish": 1.45, "Kernel Corn": 1.25,
      "Sardine Fish": 0.95, "Chicken Luncheon Meat": 1.95, "Pickled Lettuce": 0.95}
cs = {"Fine Salt": 0.80, "Sea Salt Flakes": 1.30, "Chicken Stock": 3.15, "Chilli Sauce": 2.65, "Oyster Sauce": 4.50,
      "Sweet Soy Sauce": 3.75, "Tomato Ketchup": 3.20, "Sesame Oil": 4.95}
db = {'Green Tea Canned 330': 15.00, "Blackcurrant Ribena 330 ML": 31.00, "100 Plus 24 Cans": 15.00,
      "Orange Cordial 2 Lite": 3.90, "Mineral Water 24 x 600": 7.00, "Pineapple juice": 0.80, "Nescafe Coffee": 9.90,
      "Coke 24 Cans": 12.40}
goods = Merge(d, pg, cg, cs, db)
a = dict(sorted(goods.items(), key=operator.itemgetter(0)))
b = dict(sorted(goods.items(), key=operator.itemgetter(1)))


def mainMenu():
    while True:
        print()
        print('''### Grocery cart ###         

         Select a number for the action that you would like to do :

         1. View Category Table
         2. list of grocery items in alphabetical order 
         3. list of items in ascending price 
         4. Add items
         5. View your cart
         6. Remove the item from the cart
         7. Check out
         8. Exit
         ''')
        selection2 = input("Choose an option: ")

        if selection2 == "1":
            displayCategory()
        elif selection2 == "2":
            lgia()
        elif selection2 == "3":
            lgin()
        elif selection2 == "4":
            addItem()
        elif selection2 == "5":
            displayList()
        elif selection2 == "6":
            removeItem()
        elif selection2 == "7":
            checkOut()
        elif selection2 == "8":
            quit()


def displayCategory():
    print()
    print('''### Category List ###         

         Select a number for the C1
         Category List :

         1. Dairy
         2. Packaged Goods
         3. Canned Goods
         4. Condiments/Sauces
         5. Drink & Beverages
         6. Back
         ''')
    selection1 = input("Choose an option: ")
    if selection1 == "1":
        print("### Dairy List ### "
              "\n|%-10s | %-30s | %-s" % ("Category", "ITEM", "Price Exclusive GST"))
        for i in d:
            print("|%-10s | %-30s | %-s" % ("Dairy", i, d[i]))
        addItem()
    elif selection1 == "2":
        print("### Packaged Goods List ### "
              "\n|%-14s | %-30s | %-s" % ("Category", "ITEM", "Price Exclusive GST"))
        for i in pg:
            print("|%-10s | %-30s | %-s" % ("Packaged Goods", i, pg[i]))
        addItem()
    elif selection1 == "3":
        print("### Canned Goods List ### "
              "\n|%-12s | %-30s | %-s" % ("Category", "ITEM", "Price Exclusive GST"))
        for i in cg:
            print("|%-10s | %-30s | %-s" % ("Canned Goods", i, cg[i]))
        addItem()
    elif selection1 == "4":
        print("### Condiments/Sauces List ### "
              "\n|%-17s | %-30s | %-s" % ("Category", "ITEM", "Price Exclusive GST"))
        for i in cs:
            print("|%-10s | %-30s | %-s" % ("Condiments/Sauces", i, cs[i]))
        addItem()
    elif selection1 == "5":
        print("### Drink & Beverages List ### "
              "\n|%-17s | %-30s | %-s" % ("Category", "ITEM", "Price Exclusive GST"))
        for i in db:
            print("|%-10s | %-30s | %-s" % ("Drink & Beverages", i, db[i]))
        addItem()
    elif selection1 == "6":
        mainMenu()
    else:
        print("\n###Please input a valid input###")


def addItem():
    while True:
        buy = str.lower(input("Is there anything in there that you need?(Yes/No)"))
        if (buy == "yes" or buy == "no"):
            break
        else:
            print("Sorry, please enter a valid input")
    if buy == "no":
        mainMenu()
    else:
        item = input("Enter the item you wish to add to your cart: ")
        if item not in goods:
            print("The item you chose is not valid")
            return
        quantity = input("Enter the quantity of the item you wish to add to your cart: ")
        for _ in range(0, int(quantity)):
            grocery_cart.append(item)
        print(item + " has been added to your cart.")


def displayList():
    while True:
        if len(grocery_cart) == 0:
            print("Sorry there are no items in your cart")
            input("You can press ENTER to continue")
            mainMenu()
        else:
            break
    print()
    print("---Grocery List---")
    print("------------------- Grocery Bill --------------------")
    print("ITEM                          | QUANTITY | ITEM PRICE")
    unique_cart = set(grocery_cart)
    for item in unique_cart:
        item_quantity = grocery_cart.count(item)
        item_price = goods[item] * item_quantity
        spaces = 30 - len(item)
        print(item, end="")
        for _ in range(0, spaces):
            print(" ", end="")

    print("|    ", item_quantity, "  |  ", "${:.2f}".format(item_price))
    input("You can press ENTER to continue")


def checkOut():
    while True:
        if len(grocery_cart) == 0:
            print("Sorry there are no items in your cart")
            input("You can press ENTER to continue")
            mainMenu()
        else:
            break

    membership = str.lower(input("Do you have a discount card?"))
    total_price = 0
    if (membership == "yes"):
        print("Here is your bill...", end="\n\n")
        print("------------------- Grocery Bill --------------------")
        print("ITEM                          | QUANTITY | ITEM PRICE")

        unique_cart = set(grocery_cart)
        for item in unique_cart:
            item_quantity = grocery_cart.count(item)
            item_price = goods[item]
            item_GST = goods[item] * 0.07
            total_pw = item_price * item_quantity
            item_Rprice = item_price + item_GST
            total_price = item_Rprice * item_quantity * 0.9

            spaces = 30 - len(item)
            print(item, end="")
            for _ in range(0, spaces):
                print(" ", end="")

            print("|    ", item_quantity, "  |  ", "${:.2f}".format(item_price))
    elif (membership == "no"):
        print("Here is your bill...", end="\n\n")
        print("------------------- Grocery Bill --------------------")
        print("ITEM                          | QUANTITY | EACH ITEMS PRICE(without GST)")

        unique_cart = set(grocery_cart)
        for item in unique_cart:
            item_quantity = grocery_cart.count(item)
            item_price = goods[item]
            item_GST = goods[item] * 0.07
            total_pw = item_price * item_quantity
            item_Rprice = item_price + item_GST
            total_price = item_Rprice * item_quantity

            spaces = 30 - len(item)
            print(item, end="")
            for _ in range(0, spaces):
                print(" ", end="")

            print("|    ", item_quantity, "  |  ", "${:.2f}".format(item_price))

    print("-----------------------------------------------------")

    print("Total Price (without GST):", "${:.2f}".format(total_pw))
    print("Total Cost:", "${:.2f}".format(total_price))
    print("------------------- Hello Dear Customer --------------------")
    print("Thank you for shopping with zkj Grocery!"
          "\nDo remember to register to become a member if you wish to receive a membership discount")
    input("You can press ENTER to continue")
    quit()
    grocery_cart.clear()


def removeItem():
    displayList()
    item = str.lower(input("Enter the item you wish to remove from your cart: "))
    if item not in grocery_cart:
        print("The item you chose is not in the cart")
        return
    quantity = input("Enter the quantity of the item you wish to remove from your cart: ")
    if int(quantity) < 0:
        print("Invalid quantity")
    else:
        for i in range(0, int(quantity)):
            grocery_cart.remove(item)
        print(item + " has been removed from your cart.")


def lgia():
    print("---- list of grocery items in alphabetical order ----"
          "\n%-30s | %10s$" % ("ITEM", "Price Exclusive GST"))
    for i in a:
        print("%-30s | $%-s" % (i, a[i]))
    addItem()


def lgin():
    print("--------- list of items in ascending price ----------"
          "\n%-30s | %10s$" % ("ITEM", "Price Exclusive GST"))
    for i in b:
        print("%-30s | $%-s" % (i, b[i]))
    addItem()


mainMenu()



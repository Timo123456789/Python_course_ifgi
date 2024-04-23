import easy_shopping




cal = easy_shopping.calculator.calculator()

print(cal.addition(7,5))
print(cal.substract(34,21))
print(cal.multiply(54,2))
print(cal.division(144,2))
print(cal.division(45,0))

shopping = easy_shopping.shopping.ShoppingCart()
shopping.addItem("kiwi", 5)
shopping.addItem("apple", 7)
shopping.addItem("blueberriy", 3)
print(shopping.itemsDict)

shopping.totalAmount()

print(shopping.removeItem("kiwi"))
shopping.totalAmount()
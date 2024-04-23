class ShoppingCart:
    def __init__(self):
        self.itemsDict = {}
        
    def addItem(self, item, quantity):
        if item in self.itemsDict:
            self.itemsDict[item] += quantity
        else:
            self.itemsDict[item] = quantity
            
        
    def removeItem(self, item):
        if item in self.itemsDict:
            del self.itemsDict[item]
            return(self.itemsDict)
        else:
            print("item not in shopping Cart")
            
    def totalAmount(self):
        sum = 0
        for i in self.itemsDict:
            sum = sum + self.itemsDict[i]
        print(f'The number of items is {sum}')
            
        

# if __name__ == "__main__":
#     shopping = ShoppingCart()
#     shopping.addItem("kiwi", 5)
#     shopping.addItem("apple", 7)
#     shopping.addItem("blueberriy", 3)
#     print(shopping.itemsDict)
    
#     shopping.totalAmount()
    
#     print(shopping.removeItem("kiwi"))
#     shopping.totalAmount()
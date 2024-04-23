class calculator:

    def addition(self, a, b):
        return a + b

    def substract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a*b
    
    def division(self, a, b):
        if a == 0 or b == 0: 
            return("Cant divide by Zero")
        else: 
            return(a/b)    

# if __name__ == "__main__":
#     cal = calculator()

#     print(cal.addition(7,5))
#     print(cal.substract(34,21))
#     print(cal.multiply(54,2))
#     print(cal.division(144,2))
#     print(cal.division(45,0))

 
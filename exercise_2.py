#function for return number of donut
def donuts(count):
    #if parameter is a string return error
    if type(count) == str:
        return "This is not an integar"
    if count >= 10:
        count = "many"
    return f"number of donuts: {count}"


def verbing(s):
    #check for length and ending with "ing"
    if len(s) >= 3 and s.endswith("ing") == False:
        return s + "ing"
    #check for length and ending with "ing" if True replace ing with ly
    elif len(s) >= 3 and s.endswith("ing") == True:
        return s.replace("ing", "ly")
    #if string is smaller 3 do nothing
    elif len(s) < 3:
        return s
    else:
        return "s is not a String"


#function for removing duplicates in a list
def remove_adjacent(nums):
    l = []
    #loop through list, if this value already does not exist append it to the list else skip
    for num in nums: 
        if num not in l:
            l.append(num)
        else:
            continue
    return l

def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))
    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))


if __name__ == "__main__":
    main()
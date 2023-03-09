

mylist = ["a","","a","","","a","","","","a","a","a","","","","a","a"]




def func(mylist):
    for item in mylist:
        if item:
            continue

        print(item)



print(func(mylist))
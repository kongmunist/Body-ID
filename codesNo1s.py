def findSmallest(x):

    prevLowest = 0
    count = 1
    k = 0
    j = 0

    while True:
        if (x[k] == '0'):
            j = k
            break
        else:
            k += 1
            
    for i in range(j+1,len(x)):
        if x[i] == x[i-1]:
            count += 1
        elif (prevLowest > count or prevLowest == 0):
            prevLowest = count
            count = 1
        else:
            count = 1
    
    return prevLowest

def condense(x,length):

    newArr = []

    k = 0
    j = 0

    while True:
        if (x[k] == '0'):
            j = k
            break
        else:
            k += 1

    for i in range(0,(len(x)-j)//4):
        newArr.append(x[j+length*i])
    
    return newArr

print(findSmallest("11111111111111000011111111111111110000111100000000"))
print(condense("11111111111111111111000011111111111111110000111100000000",4))
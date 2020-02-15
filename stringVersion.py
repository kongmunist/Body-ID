def findSmallest(x):

    prevLowest = 0
    count = 1
    k = 0
    j = 0
    l = 0

    while True:
        if (x[k] == '1'):
            j = k
            break
        else:
            k += 1
    
    while True:
        if (x[j] == '0'):
            l = j
            break
        else:
            j += 1
            
    for i in range(l+1,len(x)):
        if x[i] == x[i-1]:
            count += 1
        elif (prevLowest > count or prevLowest == 0):
            prevLowest = count
            count = 1
        else:
            count = 1
    
    return prevLowest

def condense(x,length):

    newStr = ""

    k = 0
    j = 0
    l = 0

    while True:
        if (x[k] == '1'):
            j = k
            break
        else:
            k += 1
    
    while True:
        if (x[j] == '0'):
            l = j
            break
        else:
            j += 1

    for i in range (0,(len(x)-l)//4):
        newStr += x[l+length*i]
    
    return newStr

# print condense("00000011111111111111000011111111111111110000111100000000",findSmallest("11111111111111000011111111111111110000111100000000"))
# print condense("000001111111100000000111100000000000011111111000011110000111100000000",findSmallest("1111111100000000111100000000000011111111000011110000111100000000"))
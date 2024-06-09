import random
class Generation():

    #'n' is the horizontal side length of the canvas

    #the aspect ratio of the canvas is by default 5:3, this is the fraction in the 'height' variable

    #'landValue' is the amount of land scaling from 0 being none to 100 being almost 100%
    #avoid setting this number higher than 100 as overflow errors may prevent proper generation
    #default is 30
    #recommended value range is 20-50, any higher and certain generation features become too prominent,
    #any lower and the visible majority of the map is water
    
    #'string' is the number that, when changed, most affected the "stringyness" of the final generation
    #'string' scales from 1 to 5, with 1 being the highest stringyness and 5 the lowest
    #'string' MUST NOT have a value of 0, this will return an error
    #it is set to 3 by default

    def continents(n):
        #determines features and values of the final generation
        landValue = 40
        string = 3
        height = n*3//5
        board = []
        terNum = (n*height)*(landValue/100)
        conNum = random.randint(4,8)
        conWeight = []
        for i in range(conNum):
            conWeight.append(random.randint(1,4))
        totalWeight = 0
        for i in range(len(conWeight)):
            totalWeight += conWeight[i]
        conTerNum = []
        #assigns each continent a number of territories based on total territory number and the weight of
        #that continent
        for i in range(conNum):
            conTerNum.append((terNum//totalWeight)*conWeight[i])
        for r in range(height):
            tempList = []
            for c in range(n):
                tempList.append(['-'])
            board.append(tempList)
        nodeList = []
        blackList = []
        def tListGen():
            tList = [random.randint(1,height-2), random.randint(1,n)-2]
            while tList in blackList:
                tList = [random.randint(1,height-2), random.randint(1,n)-2]
            return tList
        
        #'+' is denoted as the baseline for land as opposed to '-' for water. With some small exceptions
        #such as Ice ('I'), all features after initial generation are done in land areas

        #for any given generation the number that denotes its size is "depoNum"
        #each generation uses the board that is modified by its preceding function

        #creates a "node" and builds a continent around it

        for i in range(conNum):
            value = i
            tList = tListGen()
            nodeList.append(tList)
            board[nodeList[i][0]][nodeList[i][1]] = ['+',value]
            failNum = 0
            count = 0
            cNode = nodeList[i]
            rNode = nodeList[i]
            failMax = n*(n//20)
            while count < conTerNum[i]:
                if failNum > failMax:
                    break
                if count%string == 0 and rNode != cNode:
                    cNode = rNode
                    a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                    b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                    rNode = [a,b]
                    cNode = rNode
                a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                for m in range(8):
                    if board[a][b].count('-') == 1 and [a,b] not in blackList:
                        cNode = [a,b]
                        board[a][b] = ['+',value]
                        blackList.append([a,b])
                        count+=1
                        break
                if board[a][b].count('+') == 1:
                    cNode = [a,b]
                else:
                    failNum+=1
                    cNode = rNode
        #this is my amaazing code
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value == '-':
                    if neighbors(board, "otherWater", x, y, n) == 1:
                        board[y][x] = ['+','%']
        return board
    
    #changes some of the previously generated land to be "badlands" using a similar node method
    def badlands(n):
        height = n*3//5
        board = Generation.continents(n)
        badlandsBList = []
        for r in range(height):
            for c in range(n):
                depoNum = 0
                if r > height*5/8 or r < height*3/8:
                    if board[r][c].count('-') == 0 and [r,c] not in badlandsBList:
                        target = random.randint(n*12,n*18)
                        number = random.randint(n*12,n*18)
                        diff = abs(number-target)
                        depoNum = 0
                        if diff == 0 or diff == 1:
                            depoNum = number*8
                rNode = [r,c]
                cNode = rNode
                count = 0
                while count < depoNum:
                    if count%5 == 0 and rNode != cNode:
                        cNode = rNode
                        a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                        b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                        rNode = [a,b]
                        cNode = rNode
                    a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                    b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                    if board[a][b].count('-') == 0 and [a,b] not in badlandsBList:
                        board[a][b].append('&')
                        cNode = [a,b]
                        badlandsBList.append(cNode)
                        count+=1
                    elif board[a][b].count('&') == 1:
                        cNode = [a,b]
                    else:
                        cNode = rNode
                        count += 1
        return board
    
    #changes the top and bottom of the canvas to be Icier(tm)
    #this function uses notably different generative paths
    def tundra(n):
        height = n*3//5
        board = Generation.badlands(n)
        northLine = []
        southLine = []
        nIceLine = []
        sIceLine = []
        for c in range(n):
            tNorth = height*(7/8) + random.randint(0,2) - random.randint(0,2)
            northLine.append(tNorth)
            tSouth = height*(1/8) + random.randint(0,2) - random.randint(0,2)
            southLine.append(tSouth)
            tNIce = height*(24/25) + random.randint(0,3) - random.randint(0,3)
            nIceLine.append(tNIce)
            tSIce = height*(1/25) + random.randint(0,3) - random.randint(0,3)
            sIceLine.append(tSIce)
        for r in range(height):
            for c in range(n):
                if (r > nIceLine[c] or r < sIceLine[c]) and board[r][c].count('-') == 1:
                    board[r][c].append('I')
                elif (r > nIceLine[c] or r < sIceLine[c]) and board[r][c].count('-') == 0:
                    board[r][c].append('!!')
                elif (r > northLine[c] or r < southLine[c]) and board[r][c].count('-') == 0:
                    board[r][c].append('!')
        return board
    
    #creates a random number of large deserts based on "desertNum"
    def desert(n):
        height = n*3//5
        board = Generation.tundra(n)
        desertBList = []
        desertNum = random.randint(0,3)
        for i in range(desertNum):
            r,c = random.randint(height*3//8,height*5//8),random.randint(0,n-1)
            while board[r][c].count('-') == 1:
                r,c = random.randint(height*3//8,height*5//8),random.randint(0,n-1)
            depoNum = random.randint(n*30,n*40)/(2000/n)
            rNode = [r,c]
            cNode = rNode
            count = 0
            oceanCount = 0
            while count < depoNum:
                if count%5 == 0 and rNode != cNode:
                    cNode = rNode
                    a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                    b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                    rNode = [a,b]
                    cNode = rNode
                a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                if board[a][b].count('-') == 1 or board[a][b].count('!') == 1 or board[a][b].count('!!') == 1:
                    cNode = [r,c]
                    oceanCount+=1
                    if oceanCount >= depoNum*3:
                        break
                elif board[a][b].count('-') == 0 and [a,b] not in desertBList:
                    board[a][b].append('@')
                    cNode = [a,b]
                    desertBList.append(cNode)
                    count+=1
                elif board[a][b].count('@') == 1:
                    cNode = [a,b]
                else:
                    cNode = rNode
        return board
    
    #first highly-sensitive function that has extremely specific generative restraints
    #functions from here down do not follow a strict top-down hierarchy
    def forest(n):
        height = n*3//5
        board = Generation.desert(n)
        forestBList = []
        for r in range(height):
            for c in range(n):
                if board[r][c].count('-') == 0 and [r,c] not in forestBList:
                    if board[r][c].count('!!') == 1 or board[r][c].count('I') == 1 or board[r][c].count('@') == 1:
                        continue
                    if ((r > height*(2/3) or r < height*(1/3)) and (c > (n*3//4) or c < (n*1//4))) or ((r > height*(2/3) or r < height*(1/3)) and (c > (n*2//3) or c < (n*1//3))):
                        target = random.randint(1,n*2)
                        number = random.randint(1,n*2)
                        diff = abs(number-target)
                        depoNum = 0
                        if diff < 3:
                            depoNum = (number//3) - diff
                        elif diff == 0:
                            depoNum = number*2//3
                    else:
                        target = random.randint(1,n)
                        number = random.randint(1,n)
                        diff = abs(number-target)
                        depoNum = 0
                        if diff < 3:
                            depoNum = (number//4) - diff
                        elif diff == 0:
                            depoNum = number*2//3
                    rNode = [r,c]
                    cNode = rNode
                    count = 0
                    while count < depoNum:
                        if count%5 == 0 and rNode != cNode:
                            cNode = rNode
                            a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                            b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                            rNode = [a,b]
                            cNode = rNode
                        a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                        b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                        if board[a][b].count('!!') or board[a][b].count('%') == 1 or board[a][b].count('@') == 1:
                            cNode = rNode
                            count+=1
                            continue
                        if board[a][b].count('-') == 0 and board[a][b].count('I') == 0 and [a,b] not in forestBList:
                            if board[a][b].count('!') == 1:
                                remove = random.randint(0,1)
                                if remove == 0:
                                    board[a][b].append('#')
                            elif board[a][b].count('&') == 1:
                                remove = random.randint(0,2)
                                if remove == 0:
                                    board[a][b].append('#')
                            else:
                                board[a][b].append('#')
                            cNode = [a,b]
                            forestBList.append(cNode)
                            count+=1
                        elif board[a][b].count('#') == 1:
                            cNode = [a,b]
                        else:
                            cNode = rNode
                            count += 1
        return board
    
def finalGen(n):
    board = Generation.forest(n)
    return board
'''
is there any way to make this code more efficient?
\/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/
'''
def neighbors(grid,type,x,y,n,):
    if type == "water":
        # Checks for 1 away
        one_step_checks = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for row, col in one_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col].count('-') == 0 and grid[row][col].count('I') == 0:
                    return 1 
        # check for 2 away
        two_step_checks = [
            (y - 2, x), (y + 2, x), (y, x - 2), (y, x + 2),
            (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)
        ]
        for row, col in two_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col].count('-') == 0:
                    return 2
        #check for 3 away
        three_step_checks = [
            (y - 3, x), (y + 3, x), (y, x - 3), (y, x + 3),
            (y - 2, x - 1), (y - 2, x + 1), (y + 2, x - 1), (y + 2, x + 1),
            (y - 1, x - 2), (y - 1, x + 2), (y + 1, x - 2), (y + 1, x + 2)
        ]
        for row, col in three_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col].count('-') == 0:
                    #adds a 50/50 to make it more random
                    if random.randint(1,2) == 1:
                        return 3
    elif type == "otherWater":
        one_step_checks = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for row, col in one_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col].count('-') == 0 and grid[row][col].count('%') == 0:
                    return 1

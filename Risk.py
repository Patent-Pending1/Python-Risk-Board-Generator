import random
class Generation():
    def __init__(self,n):
        self.n = n
    def continents(n):
        height = n*3//5
        board = []
        terNum = (n*height)*(100/100)
        conNum = random.randint(4,10)
        conWeight = []
        for i in range(conNum):
            conWeight.append(random.randint(1,n//15))
        tempWeight = 0
        for i in range(len(conWeight)):
            tempWeight += conWeight[i]
        conTerNum = []
        for i in range(conNum):
            conTerNum.append((terNum//tempWeight)*conWeight[i])
        for i in range(len(conTerNum)):
            conTerNum[i]+=random.randint(0,2)
            conTerNum[i]-=random.randint(0,2)
        for r in range(height):
            tempList = []
            for c in range(n):
                tempList.append(' ')
            board.append(tempList)
        nodeList = []
        blackList = []
        def tListGen():
            tList = [random.randint(1,height-2), random.randint(1,n)-2]
            while tList in blackList:
                tList = [random.randint(1,height-2), random.randint(1,n)-2]
            return tList 
        for i in range(conNum):
            value = '0'
            tList = tListGen()
            nodeList.append(tList)
            board[nodeList[i][0]][nodeList[i][1]] = value
            failNum = 0
            count = 0
            cNode = nodeList[i]
            rNode = nodeList[i]
            failMax = n*(n//20)
            while count < conTerNum[i]:
                if failNum > failMax:
                    break
                if count%5 == 0 and rNode != cNode:
                    rNode = cNode
                a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                for m in range(8):
                    if board[a][b] == ' ' and [a,b] not in blackList:
                        cNode = [a,b]
                        board[a][b] = value
                        blackList.append([a,b])
                        count+=1
                        break
                if board[a][b] == value:
                    cNode = [a,b]
                    count+=1
                else:
                    failNum+=1
                    cNode = rNode
            for i in range(height):
                for j in range(n):
                    if board[i][j] != ' ':
                        for r in range(3):
                                for c in range(3):
                                    blackList.append([(i+1-r)%height,(j+1-c)%n])
        #this is my amaazing code
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value == ' ':
                    if neighbors(board, "otherWater", x, y, n) == 1:
                        board[y][x] = "%"
        return board
    def badlands(n):
        height = n*3//5
        board = Generation.continents(n)
        badlandsBList = []
        for r in range(height):
            for c in range(n):
                depoNum = 0
                if r > height*5/8 or r < height*3/8:
                    if board[r][c] != ' ' and [r,c] not in badlandsBList:
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
                    if count % 5 == 0 and rNode != cNode:
                        cNode = rNode
                        a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                        b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                        rNode = [a,b]
                        cNode = rNode
                    a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                    b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                    if board[a][b] != ' ' and [a,b] not in badlandsBList:
                        board[a][b] = '&'
                        cNode = [a,b]
                        badlandsBList.append(cNode)
                        count+=1
                    elif board[a][b] == '&':
                        cNode = [a,b]
                    else:
                        cNode = rNode
                        count += 1
        return board
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
                if (r > nIceLine[c] or r < sIceLine[c]) and board[r][c] == ' ':
                    board[r][c] = 'I'
                elif (r > nIceLine[c] or r < sIceLine[c]) and board[r][c] != ' ':
                    board[r][c] = '!!'
                elif (r > northLine[c] or r < southLine[c]) and board[r][c] != ' ':
                    board[r][c] = '!'
        return board
    def desert(n):
            height = n*3//5
            board = Generation.tundra(n)
            desertBList = []
            for r in range(height):
                for c in range(n):
                    depoNum = 0
                    if r < height*5/8 and r > height*3/8:
                        if board[r][c] != ' ' and [r,c] not in desertBList:
                            target = random.randint(n*16,n*32)
                            number = random.randint(n*16,n*32)
                            diff = abs(number-target)
                            depoNum = 0
                            if diff == 0:
                                depoNum = number*6
                    rNode = [r,c]
                    cNode = rNode
                    count = 0
                    while count < depoNum:
                        if count % 5 == 0 and rNode != cNode:
                            cNode = rNode
                            a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                            b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                            rNode = [a,b]
                            cNode = rNode
                        a = random.randint(int(cNode[0])-1,int(cNode[0])+1)%height
                        b = random.randint(int(cNode[1])-1,int(cNode[1])+1)%n
                        if board[a][b] != ' ' and [a,b] not in desertBList:
                            board[a][b] = '@'
                            cNode = [a,b]
                            desertBList.append(cNode)
                            count+=1
                        elif board[a][b] == '@':
                            cNode = [a,b]
                        else:
                            cNode = rNode
                            count += 1
            return board
class Deposit():
    def __init__(self,n):
        self.n = n
    def forest(n):
        height = n*3//5
        board = Generation.desert(n)
        forestBList = []
        for r in range(height):
            for c in range(n):
                if board[r][c] != ' ' and [r,c] not in forestBList:
                    if board[r][c] == '!!' or board[r][c] == 'I' or board[r][c] == '@':
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
                        if board[a][b] == '!!':
                            cNode = rNode
                            count+=1
                            continue
                        elif board[a][b] == '%':
                            cNode = rNode
                            count+=1
                            continue
                        if board[a][b] != ' ' and board[a][b] != 'I' and [a,b] not in forestBList:
                            if board[a][b] == '!':
                                remove = random.randint(0,1)
                                if remove == 0:
                                    board[a][b] = '#'
                            elif board[a][b] == '&':
                                remove = random.randint(0,2)
                                if remove == 0:
                                    board[a][b] = '#'
                            else:
                                board[a][b] = '#'
                            cNode = [a,b]
                            forestBList.append(cNode)
                            count+=1
                        elif board[a][b] == '#':
                            cNode = [a,b]
                        else:
                            cNode = rNode
                            count += 1
        return board
def finalGen(n):
    board = Generation.badlands(n)
    board = Deposit.forest(n)
    return board
def neighbors(grid,type,x,y,n,):
    if type == "water":
        # Checks for 1 away
        one_step_checks = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for row, col in one_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col] != ' ' and grid[row][col] != 'I':
                    return 1 
        # check for 2 away
        two_step_checks = [
            (y - 2, x), (y + 2, x), (y, x - 2), (y, x + 2),
            (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)
        ]
        for row, col in two_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col] != ' ':
                    return 2
        #check for 3 away
        three_step_checks = [
            (y - 3, x), (y + 3, x), (y, x - 3), (y, x + 3),
            (y - 2, x - 1), (y - 2, x + 1), (y + 2, x - 1), (y + 2, x + 1),
            (y - 1, x - 2), (y - 1, x + 2), (y + 1, x - 2), (y + 1, x + 2)
        ]
        for row, col in three_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col] != ' ':
                    #adds a 50/50 to make it more random
                    if random.randint(1,2) == 1:
                        return 3
    elif type == "otherWater":
        one_step_checks = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for row, col in one_step_checks:
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                if grid[row][col] != ' ' and grid[row][col] != '%':
                    return 1

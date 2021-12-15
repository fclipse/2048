# 2048 게임
# 규칙
# 0. 움직인 방향으로 빈칸이 있거나 같은 숫자가 있으면 '갈 수 있음'
# 1. 가는 방향으로 같은 숫자 있으면 합쳐짐
# 2. 합쳐져서 나온 수만큼 점수 +
# 3. 더 이상 진행할 수 없으면 게임이 끝남
# 4. 2048 이상의 수를 만들고 게임을 더 진행할 수 있으면 플레이어 승리, 아니면 패배
# 5. 처음에 2가 2개 
# 선언부
import copy, random
zeroLocation = []
board = [0]
num = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
score = 0
key = {'w' : 0, 'a' : 1, 's' : 2, 'd' : 3}
move = [[0, -1], [-1, 0], [0, 1], [1, 0]]   # **y좌표는 내려갈수록 증가함
print('board status :', board )

print('Welcome to 2048 game')
size = int(input('board size input (more than 3) :'))
board *= size**2

def isEnd():
    global board
    if board.cound(0) > 0:          # 빈칸 있으면 안끝난것, 더 빠른 버전.
        return 0
    for y in range(size):
        for x in range(size):
            #if board[y][x] == 0:    # 빈칸 있으면 안끝난것
            #    return 0
            cnt = 0
            for i in range(4):  # **상하좌우 4번만 검사
                if (i % 2 == 0 and 0 < y + i - 1 < size) or (i % 2 == 1 and 0 < x + i - 2 < size) :
                    if board[y + i - 1][x + i - 2] == board[y][x]:
                        return 0 # 합칠 수 있는 칸이 있다면 안 끝난 것
    return 1    # 빈칸도 없고 합칠 수 있는 칸도 없을 때

def findZero():
    global board
    global zeroLocation
    zeroLocation = []       # 초기화
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                zeroLocation.append([i, j])
    return

def createRandomNumber():
    global board
    global zeroLocation
    global num
    findZero()
    N = num[random.randint(0, 9)]
    randindex = random.randint(0, len(zeroLocation) - 1)
    board[zeroLocation[randindex][1]][zeroLocation[randindex][0]] = N   # 첫번째인덱스가 y, 두번째 인덱스가 x
    return

def swap(y1, x1, y2, x2):   # 두 좌표를 입력받고 그 좌표에 있는 수를 바꿈
    global board
    var = board[y1][x1]
    board[y1][x1] = board[y2][x2]
    board[y2][x2] = var
    return

def merge(y1, x1, y2, x2):   # 두 좌표를 입력받고 그 좌표에 있는 수를 합해 1번좌표에 반환
    global board
    global score
    board[y1][x1] *= 2
    board[y2][x2] = 0
    return

# 입력부
q1 = input('Start game? y/n')
round = 0

if q1 == 'n':
    print('See you next time')
    round = -1    
else:
    print('Game start')
    round = 1
# 실행부
# 초기 랜덤 숫자 2개

for i in range(2):
    coordinate = [random.randint(0, size-1), random.randint(0, size-1)]
    while board[coordinate[1], coordinate[0]] != 0:             # 빈칸에 생성
        coordinate = [random.randint(0, size-1), random.randint(0, size-1)]
    board[coordinate[0], coordinate[1]] = 2
    
# 계속 반복
while round > 0:
    for i in range(4):
        for j in range(4):
            print('%4d' % board[i][j], end = ' ')
        print()
    
    direction = input('press w/a/s/d :')
    if direction not in key:
        print('wrong key input')
        continue
    else:       # 움직일 때
        ymove = move[key[direction][1]]
        xmove = move[key[direction][0]]
        if ymove != 0:
            for i in range(size):
                for j in range(size):
                    if i == 0:
                        continue
                    else:
                        if board[i + ymove][j + xmove] == 0:
                            swap(i + ymove, j + xmove, i, j)
                        if board[i + ymove][j + xmove] == board[i][j]:
                            merge(i + ymove, j + xmove, i, j)


    # 끝났는지 판단
    if isEnd() :

        break
    else:
        round += 1
        # 랜덤한 위치에 랜덤한 숫자 생성(4와 2비율은 1:9정도)
        createRandomNumber()
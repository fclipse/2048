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
board = []                                  # 만들 때 항상 형태 주의. 이차원 리스트인지 일차원 리스트인지 편한 걸로 생각할 수도 있음.
num = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]        # 그냥 if randint(0, 9) == 0 :일때만 4넣을 수도 있음
score = 0
key = {'w' : 0, 'a' : 1, 's' : 2, 'd' : 3}
move = [[0, -1], [-1, 0], [0, 1], [1, 0]]   # **y좌표는 내려갈수록 증가함
#print('board status :', board )

print('Welcome to 2048 game')
size = int(input('board size input (more than 3) :'))
board = [[0 for j in range(size)] for i in range(size)]
#print('board init :')
#print(board)
#for i in range(size):
#    for j in range(size):
#        print(board[i][j], end = ' ')
#    print()

def isEnd():
    global board
    for y in range(size):
        for x in range(size):
            if board[y][x] == 0:    # 빈칸 있으면 안끝난것
                return 0
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
                zeroLocation.append([i, j])     # ***여기서 [y, x] 형태로 생성하는데 그걸 제대로 받지 못해 생긴 문제.
    return

def createRandomNumber():
    global board
    global zeroLocation
    global num
    findZero()
    N = num[random.randint(0, 9)]
    randindex = random.randint(0, len(zeroLocation) - 1)
    #print('radom coordinate :', randindex[0], randindex[1])
    board[zeroLocation[randindex][0]][zeroLocation[randindex][1]] = N   # 첫번째인덱스가 y, 두번째 인덱스가 x
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
    score += board[y1][x1]
    board[y2][x2] = 0
    return

def rotate():       # 오른쪽(시계 방향)으로 1회 회전
    global board
    white_board = [[0 for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            white_board[j][size-i-1] = board[i][j]
    board = copy.deepcopy(white_board)
    return

def printBoard():
    global board
    for i in range(4):
        for j in range(4):
            print('%4d' % board[i][j], end = ' ')
        print()
    return

def maxNum():
    global board
    num = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] > num:
                num = copy.copy(board[i][j])
    return num


# 입력부
#q1 = input('Start game? y/n')
round = 0

#if q1 == 'n':
#    print('See you next time')
#    round = -1    
#else:
print('Game start')
round = 1
# 실행부
# 초기 랜덤 숫자 2개

for i in range(2):
    coordinate = [random.randint(0, size-1), random.randint(0, size-1)]
    
    while board[coordinate[1]][coordinate[0]] != 0:             # 빈칸에 생성
        coordinate = [random.randint(0, size-1), random.randint(0, size-1)]
    board[coordinate[0]][coordinate[1]] = 2

# 계속 반복
while round > 0:
    # 출력
    print()
    maxNumber = maxNum()
    print('round : %4d / score : %d / max Number : %d' % (round, score, maxNumber))
    printBoard()
    # 입력받음
    direction = input('press w/a/s/d :')
    if direction not in key:
        print('wrong key input')
        continue
    else:       # 움직일 때
        # 첫 번째 돌림
        for i in range(key[direction]):
            rotate()
        
        # 숫자 움직이기
        moved = 0       # 움직이지 않으면 안됨.
        for i in range(size):
            for j in range(size):
                merged = 0                  # 턴마다 한 번씩만 merge해줘야 함.
                if board[i][j] != 0:
                    for k in range(i):      # y좌표 내려온 횟수만큼 반복
                        if board[i - k - 1][j] == 0:                    # 위에 비어있으면 올려보냄
                            swap(i - k - 1, j, i - k, j)
                            moved += 1
                        elif board[i - k - 1][j] == board[i - k][j] and merged == 0:        # 같을 때 합침
                            merge(i - k - 1, j, i - k, j)                   # 올려보내기를 먼저 해서 바로 위에 숫자가 있을 경우에만 합침. 중간에 0이 있을 경우 없음.
                            merged += 1
                            moved += 1
        
        # 두 번째 돌림
        for i in range(4 - key[direction]):
            rotate()
            
        if moved == 0:
                continue        # 바뀐 게 없으면 다시 한번.
    
    # 오류 확인용
    #print('before create random number')
    #printBoard()
    # 끝났는지 판단
    if isEnd() :
        break
    else:
        round += 1
        # 랜덤한 위치에 랜덤한 숫자 생성(4와 2비율은 1:9정도)
        createRandomNumber()
        print(zeroLocation)

#일단은 2048찍고 게임 끝날 경우에도 승리로 판정
maxNumber = maxNum()
if maxNumber >= 2048:
    print('You Win!')
    print('Congratuations! your max Number is %d and Score is %d' % (maxNumber, score))
else:
    print('You Lose')
    print('Wawawa... See you next time! Your max Number is %d and score is %d' % (maxNumber, score))
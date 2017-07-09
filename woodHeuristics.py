import sys
import random
import Queue
from sets import Set

size = int(raw_input())
units_per_player = int(raw_input())
self_units_pos = [[0, 0] for i in '.'*units_per_player]
en_units_pos = [[0, 0] for i in '.'*units_per_player]
en_unknown = [True for i in '.'*units_per_player]
cmds = []
grid = [['.' for i in '.'*size] for j in '.'*size]
grid_movement = {
    'N': (-1, 0),
    'NE': (-1, 1),
    'E': (0, 1),
    'SE': (1, 1),
    'S': (1, 0),
    'SW': (1, -1),
    'W': (0, -1),
    'NW': (-1, -1)
}

directions = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']

actionTypes = ['MOVE&BUILD', 'PUSH&BUILD']

def verify(coord):
    y = coord[0]
    x = coord[1]
    if (x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid) or grid[y][x] == '.'):
        return False
    return True

def procAction(atype, dir1, dir2, o):
    m = grid_movement[dir1]
    b = grid_movement[dir2]
    if (atype == actionTypes[0]):
        endPos = (o[0]+m[0], o[1]+m[1])
        buildPos = (endPos[0]+b[0], endPos[1]+b[1])
        return (endPos, buildPos)
    elif (atype == actionTypes[1]):
        buildPos = (o[0]+m[0], o[1]+m[1])
        enPos = (buildPos[0]+b[0], buildPos[1]+b[1])
        return (enPos, buildPos)
    print >> sys.stderr, "Invalid Action Type"
    return None

def surrHeights(o):
    h = [-1 for i in '.......']
    for i, cdir in enumerate(directions):
        m = grid_movement[cdir]
        ny = o[0]+m[0]
        nx = o[1]+m[1]
        if (verify((ny, nx))):
            h[i] = grid[ny][nx]
    return h

def floodfill(o, m, b, blockedSet):
    bKey = b[0]*100+b[1]
    oKey = o[0]*100+o[1]

    visited = Set([])
    blocked = blockedSet

    for y in xrange(size):
        for x in xrange(size):
            print >> sys.stderr, grid[y][x],
        print >> sys.stderr, ''

    q = Queue.Queue()
    q.put((m,m))
    # for c in grid_movement.values():
    #     newCoord = (o[0]+c[0], o[1]+c[1])
    #     if (verify(newCoord)):
    #         q.put((o,newCoord))

    while not q.empty():
        cur = q.get()
        curO = cur[0]
        curCoord = cur[1]
        curKey = curCoord[0]*100+curCoord[1]
        if (curKey == bKey or curKey in visited or (curKey in blocked and curKey != oKey)):
            continue
        oHeight = grid[curO[0]][curO[1]]
        curHeight = grid[curCoord[0]][curCoord[1]]
        if (abs(oHeight - curHeight) < 2):
            visited.add(curKey)
            for c in grid_movement.values():
                newCoord = (curCoord[0]+c[0], curCoord[1]+c[1])
                if (verify(newCoord)):
                    q.put((curCoord,newCoord))
    print >> sys.stderr, len(visited)

    for y in xrange(size):
        for x in xrange(size):
            print >> sys.stderr, 'X' if y*100+x in visited else grid[y][x],
        print >> sys.stderr, ''

    return len(visited)

# game loop
while True:
    del cmds[:]
    for i in xrange(size):
        row = raw_input()
        for j, c in enumerate(row):
            grid[i][j] = c if c == '.' else int(c)
        print >> sys.stderr, grid[i]
    for i in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
        self_units_pos[i][0] = unit_y
        self_units_pos[i][1] = unit_x
    for i in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
        if (other_x+other_y < 0):
            en_unknown[i] = True
        else:
            en_unknown[i] = False
            en_units_pos[i][0] = other_y
            en_units_pos[i][1] = other_x
    legal_actions = int(raw_input())
    max_height = -999
    cmd_idx = 0
    curCmdLi = []
    for i in xrange(legal_actions):
        atype, index, dir_1, dir_2 = raw_input().split()
        index = int(index)
        cmds.append((index, atype, dir_1, dir_2))
        projData = procAction(atype, dir_1, dir_2, self_units_pos[index])
        ny, nx = projData[0]
        by, bx = projData[1]
        if (atype == actionTypes[0]):
            score =  # Movement score
            score += # Building score
            score += # Point-scoring score
            score -= # Blocking penalty score
            en_nearby = -1
            for c in grid_movement.values():
                cy = by + c[0]
                cx = bx + c[1]
                en_i = 0
                for en in en_units_pos:
                    if (cy == en[0] and cx == en[1]):
                        en_nearby = en_i
                    en_i += 1
            # score += 5.0 if grid[by][bx] == 3 and en_nearby > 0 and grid[en_units_pos[en_nearby][0]][en_units_pos[en_nearby][1]] > 1 else 0
            # print >> sys.stderr, "{} {} SCORE {}".format(grid[ny][nx], grid[by][bx], score)
            if (score > max_height):
                del curCmdLi[:]
                max_height = score
                cmd_idx = i
                curCmdLi.append(i)
            elif (score == max_height and grid[by][bx] == 3):
                curCmdLi.append(i)
        elif (atype == actionTypes[1]):
            score = # Movement Score
            score += # Building Score
            if (score > max_height):
                max_height = score
                cmd_idx = i

    blockedSet = Set([])
    for tmpPos in self_units_pos:
        blockedSet.add(tmpPos[0]*100+tmpPos[1])
    for tmpPos in en_units_pos:
        if (tmpPos[0]+tmpPos[1] > 0):
            blockedSet.add(tmpPos[0]*100+tmpPos[1])
    for y in xrange(size):
        for x in xrange(size):
            curGrid = grid[y][x]
            if (curGrid != '.' and curGrid > 3):
                blockedSet.add(y*100+x)

    if (len(cmds) > 0):
        curCmd = cmds[cmd_idx]
        if (len(curCmdLi) > 1):
            tmpFFScore = []
            for tmpIdx in curCmdLi:
                tmpCmd = cmds[tmpIdx]
                projData = procAction(tmpCmd[1], tmpCmd[2], tmpCmd[3], self_units_pos[tmpCmd[0]])
                m = projData[0]
                b = projData[1]
                print >> sys.stderr, tmpCmd
                curScore = sum([floodfill(self_units_pos[i], self_units_pos[i], b, blockedSet) if i != tmpCmd[0] else floodfill(self_units_pos[i], m, b, blockedSet) for i in xrange(units_per_player)])
                # curScore = floodfill(self_units_pos[tmpCmd[0]], m, b, blockedSet)
                print >> sys.stderr, "======================="
                tmpFFScore.append((curScore, tmpCmd))
            tmpFFScore = sorted(tmpFFScore, reverse=True)
            curCmd = tmpFFScore[0][1]
        print "{} {} {} {}".format(curCmd[1], curCmd[0], curCmd[2], curCmd[3])
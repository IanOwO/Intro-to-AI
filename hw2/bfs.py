import csv
import queue
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    node = [] # adjacent list 
    split = [] # to temperarily store the adjacent list
    count = 0 # check if it is the first line
    idx = [] # to store the idx (the first line)
    nodeidx = [] # to store the node index
    with open(edgeFile,'r') as file: # open file
        csvlist = csv.reader(file) # read as .csv flie
        for line in csvlist: # go through all line
            if count == 0: # if is first line, store in idx
                idx = line
                count+=1
                continue
            if split == []: # store in temp adjacent list
                split.append(line) # add line to temp adj list
                nodeidx.append(int(line[0])) # add the line index to nodeidx list
            elif split[0][0] != line[0]: # if the temp adj list has different node with current node
                node.append(split) # add temp adj list to adj list
                nodeidx.append(int(line[0])) # add current node to nodeidx list
                split = [] # reset temp adj list
                split.append(line) # add line to temp adj list
            elif line is not None: # else, add line to temp adj list
                split.append(line)
        node.append(split) # add the last temp adj list to adj list
    
    qu = queue.Queue() # create a queue
    anslist = [] # create a list to store parent, dist, visited
    for i in range(len(nodeidx)): # set all value to 0
        anslist.append([0,0,0])
    flag = 0 # check if is at the end
    num_visited = 0 # calculate the visited point
    x = nodeidx.index(start) # get the start node's index
    anslist[x][0] = -1 # parent
    anslist[x][1] = 0 # distance
    anslist[x][2] = 1 # visited
    qu.put(start) # put start in queue
    while ~qu.empty(): # loop if queue is not empty
        cur = qu.get() # get the first element of queue
        if(cur != end): # if current node is not end node
            x = nodeidx.index(cur) # get current node's index
            for j in range(len(node[x])): # go through all nodes adjacent to current node
                if int(node[x][j][1]) != end: # if the adjacent node is not end node
                    try: # try to find its index
                        y = nodeidx.index(int(node[x][j][1]))
                    except ValueError: 
                        # cannot find, then it means that the node has no adjacent node, skip it
                        continue 
                    if anslist[y][2] == 0: # if the adjacent node is not visited
                        anslist[y][0] = x # set the adj node's parent to be current node
                        anslist[y][1] = anslist[x][1] + float(node[x][j][2]) # sum up the distance
                        anslist[y][2] = 1 # set the node visited
                        num_visited += 1 # the number of visited node + 1
                        qu.put(nodeidx[y]) # push back the adjacent node
                else:
                    y = nodeidx.index(end) # get end node's index
                    num_visited += 1 # the number of visited node + 1
                    anslist[y][0] = x # set current node to be end node's parent
                    anslist[y][1] = anslist[x][1] + float(node[x][j][2]) # sum up the distance
                    anslist[y][2] = 1 # set the node visited
                    flag = 1 # set flag to 1 when end node is finded and break
                    break
            if flag == 1: # break if find end node
                break
    if(flag): # if find end node
        path = [] # create path list
        y = nodeidx.index(end) # find end node's index
        dist = anslist[y][1] # total distance walked
        cur = y # set end node's index as current index
        path.append(end) # add end to path list
        while anslist[cur][0] != -1: # loop if not find the node that its parent is -1
            cur = int(anslist[cur][0]) # current index change to current node's parent's index
            path.append(nodeidx[cur]) # add current node to path index
        path.reverse() # reverse the path and get the right path
        return path,dist,num_visited # return value
    else: return [], 0, num_visited # if did't find end, return the right value 
    # End your code (Part 1)
    # encounter problem
    # 1. read the csv and the array store string, but start and end is int
    # 2. list and numpy array can not mixed up


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')

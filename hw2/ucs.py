import csv
import queue
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
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
    
    pq = queue.PriorityQueue() # create a priority queue
    anslist = [] # create a list to store parent, dist, visited
    for i in range(len(nodeidx)): # set all value to 0
        anslist.append([0,0,0])
    flag = 0 # check if is at the end
    num_visited = 0 # calculate the visited point
    x = nodeidx.index(start) # get the start node index

    pq.put((0,start,-1)) # push start to pq (distance, current, parent)
    while ~pq.empty(): # loop if pq is not empty
        cur = pq.get() # get the first element
        x = nodeidx.index(cur[1]) # get current node's index
        if(anslist[x][2] == 0): # if current node is not visited
            num_visited += 1 # visited node + 1
            anslist[x][0] = cur[2] # set parent
            anslist[x][1] = cur[0] # set distance
            anslist[x][2] = 1 # set visited
            for j in range(len(node[x])): # go through all adjacent node
                if int(node[x][j][1]) != end: # if adj node is not end
                    try: # try to find its index
                        y = nodeidx.index(int(node[x][j][1]))
                    except ValueError:
                        # cannot find, then it means that the node has no adjacent node, skip it
                        continue
                    if anslist[y][2] == 0: # if the adj node is not visited
                        pq.put((anslist[x][1] + float(node[x][j][2]), nodeidx[y], x)) # put it in pq
                else: # if the adj node is end
                    y = nodeidx.index(end) # get end node's index
                    num_visited += 1 # visited node + 1
                    anslist[y][0] = x # set the end node's parent to be current node
                    anslist[y][1] = anslist[x][1] + float(node[x][j][2]) # sum up distance
                    anslist[y][2] = 1 # set end node visited
                    flag = 1 # set flag to 1 when end node is finded and break
                    break
            if flag == 1: # if flag is 1, find end node, break
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
    # End your code (Part 3)
    # encounter problem
    # 1. ucs use unvisited node in pq, but bfs, dfs don't mind and will get same answer


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')

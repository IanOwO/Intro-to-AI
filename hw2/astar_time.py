import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    # read edge list
    node = [] # adjacent list 
    split = [] # to temperarily store the adjacent list
    count = 0 # check if it is the first line
    nodeidx = [] # to store the node index
    with open(edgeFile,'r') as file1: # open file
        csvlist = csv.reader(file1) # read as .csv flie
        for line in csvlist: # go through all line
            if count == 0: # if is first line, count + 1
                count+=1
                continue
            else: # if is not first line, calculate the time to pass the edge
                m_to_s = float(line[2]) / (float(line[3]) * 10 / 36) # change km/h to m/s, store the time to pass the edge
                line.append(m_to_s) # add the time at the last of the line
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

    # read heuristic list
    heuristic = [] # distance to the end list 
    idx = [] # first line of heuristic
    heur_idx = [] # to store the index of each heuristic
    count = 0 # check if it is the first line
    with open(heuristicFile,'r') as file2: # open file
        csvlist = csv.reader(file2) # read as .csv flie
        for line in csvlist: # go through all line
            if count == 0: # if is first line, store in idx
                idx = line
                count+=1
                continue
            else: # if not first line
                heuristic.append(line) # add line to heuristic list
                heur_idx.append(int(line[0])) # store the line's index, search by node
    # A* algorithm
    endnode = idx.index(str(end)) # find which end node is
    pq = queue.PriorityQueue() # create a priority queue
    anslist = [] # create a list to store parent, dist, visited
    for i in range(len(nodeidx)): # set all value to 0
        anslist.append([0,0,0])
    flag = 0 # check if is at the end
    num_visited = 0 # calculate the visited point
    x = nodeidx.index(start) # get the start node's adj list's index
    h = heur_idx.index(start) # get the start node's heuristic's index

    pq.put((0 + float(heuristic[h][endnode])/1, start, -1, 0)) # push start to pq, (g(x) + h(x), current, parent, distance)
    while ~pq.empty(): # loop if pq is empty
        weight, cur, par, sec = pq.get() # get the current element
        x = nodeidx.index(cur) # get current node's index
        if(anslist[x][2] == 0): # if current node is not visited
            anslist[x][0] = par # set current node's parent
            anslist[x][1] = sec # set current node's time
            anslist[x][2] = 1 # current node visited
            num_visited += 1 # visited node + 1
            for j in range(len(node[x])): # go through all adj node
                if int(node[x][j][1]) != end: # if adj node is not visited
                    try: # try to find its index
                        y = nodeidx.index(int(node[x][j][1]))
                    except ValueError:
                        # cannot find, then it means that the node has no adjacent node, skip it 
                        continue
                    h = heur_idx.index(int(node[x][j][1])) # get adj node's heuristic
                    if anslist[y][2] == 0: # if adj node is not visited
                        next_time = float(node[x][j][3]) + float(heuristic[h][endnode]) / (float(node[x][j][3]) * 10 / 36)
                        # next time = pass edge time + next node to end node's distance / speed
                        pq.put((anslist[x][1] + next_time, nodeidx[y], x, float(node[x][j][4]) + anslist[x][1])) # push data
                else: # if adj node is end
                    y = nodeidx.index(end) # get end node's index
                    num_visited += 1 # visited number + 1
                    anslist[y][0] = x # set end node's parent
                    anslist[y][1] = anslist[x][1] + float(node[x][j][4]) # sum up time
                    anslist[y][2] = 1 # set end node visited
                    flag = 1 # set flag to 1 when end node is finded and break
                    break
            if flag == 1: # if flag is 1, find end node, break
                break
    if(flag): # if find end node
        path = [] # create path list
        y = nodeidx.index(end) # find end node's index
        time = anslist[y][1] # the total time to reach the end node
        cur = y # set end node's index as current index
        path.append(end) # add end to path list
        while anslist[cur][0] != -1: # loop if not find the node that its parent is -1
            cur = int(anslist[cur][0]) # current index change to current node's parent's index
            path.append(nodeidx[cur]) # add current node to path index
        path.reverse() # reverse the path and get the right path 
        return path,time,num_visited # return value
    else:
        return [], 0, num_visited # if did't find end, return the right value
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
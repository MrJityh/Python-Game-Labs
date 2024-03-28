# A* (star) Pathfinding
# Initialize both open and closed list
let the openList equal empty list of nodes
let the closedList equal empty list of nodes
# Add the start node
put the startNode on the openList (leave it's f at zero)
# Loop until you find the end
while the openList is not empty
    # Get the current node
    let the currentNode equal the node with the least f value
    remove the currentNode from the openList
    add the currentNode to the closedList
    # Found the goal
    if currentNode is the goal
        Congratz! You've found the end! Backtrack to get path
    # Generate children
    let the children of the currentNode equal the adjacent nodes
    
    for each child in the children
        # Child is on the closedList
        if child is in the closedList
            continue to beginning of for loop
        # Create the f, g, and h values
        child.g = currentNode.g + distance between child and current
        child.h = distance from child to end
        child.f = child.g + child.h
        # Child is already in openList
        if child.position is in the openList's nodes positions
            if the child.g is higher than the openList node's g
                continue to beginning of for loop
        # Add the child to the openList
        add the child to the openList
        




Start by Opening: Begin with only the start node in your 'open list'. This list will keep track of potential paths to explore.

Empty List for Explored Paths: Keep an 'closed list' empty at the start. This list will store nodes that have been fully explored.

Explore Until You Find the Goal:

While there are still nodes in the open list:
Choose the node that promises the shortest total path (including an estimate to the goal).
If this node is your goal, great! Trace back your steps to the start, and that's your path.
Otherwise, mark this node as explored (move it to the closed list).
Look Around Each Node:

For each neighboring node of the current node:
If it's already explored (in the closed list), ignore it.
Otherwise, calculate the path cost to reach this neighbor.
If this neighbor is new or you've found a cheaper path to it:
Update its cost and record how you got there.
Add it to the open list if it's not already there.
Repeat or End: Keep repeating this process. If the open list gets empty and you haven't found the goal, then there's no possible path.
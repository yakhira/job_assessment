from pprint import pprint

box = [["#", "#", ".", ".", ".", "#", "#"],
        [".", "#", ".", "#", ".", ".", "#"],
        [".", "#", ".", "#", "*", "#", "#"]]

box.reverse()
pprint(box)
print("")


for x in range(0, len(box)):
    obstacle = False
    for y in range(0, len(box[x])):
        if box[x][y] == "*":
            box[x][0:y] = sorted(box[x][0:y], key=lambda x: ord(x), reverse=True)
            box[x][y:] = sorted(box[x][y:], key=lambda x: ord(x), reverse=True)
            obstacle = True

    if not obstacle:
        box[x] = sorted(box[x], key=lambda x: ord(x), reverse=True)


box = [
    [row[x] for row in box]
    for x in range(0, len(box[0]))
]
pprint(box)
   


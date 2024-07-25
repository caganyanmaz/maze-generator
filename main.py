import random
from PIL import Image, ImageDraw
WIDTH, HEIGHT = 200, 200
CELL_SIZE = 20
PADDING = 20

class Node:
    def __init__(self, val):
        self.val    = val
        self.nxt    = None
        self.tail   = self
        self.head   = self
        self.length = 1

    def __eq__(self, other):
        return self.val == other.val


def shuffle(arr):
    for i in range(len(arr)):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def merge(a, b):
    if a.length < b.length:
        a, b = b, a
    a.length += b.length
    a.tail.nxt = b
    a.tail = b.tail
    while b is not None:
        b.head = a
        b = b.nxt

def main():
    edges = create_maze()
    im = draw_maze(edges)
    im.save("maze.png")
 
def draw_maze(edges):
    BOARD_WIDTH = CELL_SIZE * WIDTH 
    BOARD_HEIGHT = CELL_SIZE * HEIGHT 
    WINDOW_WIDTH  =  BOARD_WIDTH + PADDING * 2
    WINDOW_HEIGHT = BOARD_HEIGHT + PADDING * 2
    im = Image.new('RGBA', (WINDOW_WIDTH, WINDOW_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.line((PADDING, PADDING, PADDING + BOARD_WIDTH, PADDING), fill="black")
    draw.line((PADDING, PADDING + BOARD_HEIGHT, PADDING + BOARD_WIDTH, PADDING + BOARD_HEIGHT), fill="black")
    draw.line((PADDING, PADDING + CELL_SIZE, PADDING, PADDING + BOARD_HEIGHT), fill="black")
    draw.line((PADDING + BOARD_WIDTH, PADDING, PADDING + BOARD_WIDTH, PADDING + BOARD_HEIGHT - CELL_SIZE), fill="black")
    for ai, aj, bi, _ in edges:
        if ai == bi:
            draw.line((PADDING + (aj + 1) * CELL_SIZE, PADDING + ai * CELL_SIZE, PADDING + (aj + 1) * CELL_SIZE, PADDING + (ai + 1) * CELL_SIZE), fill="black")
        else:
            draw.line((PADDING + aj * CELL_SIZE, PADDING + (ai + 1) * CELL_SIZE, PADDING + (aj + 1) * CELL_SIZE, PADDING + (ai + 1) * CELL_SIZE), fill="black")
    return im

def create_maze():
    nodes = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            row.append(Node((i, j)))
        nodes.append(row)
    edges = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i != HEIGHT - 1:
                edges.append((i, j, i+1, j))
            if j != WIDTH - 1:
                edges.append((i, j, i, j+1))
    shuffle(edges)
    res_edges = []
    for ai, aj, bi, bj in edges:
        if nodes[ai][aj].head == nodes[bi][bj].head:
            res_edges.append((ai, aj, bi, bj))
            continue
        merge(nodes[ai][aj].head, nodes[bi][bj].head)
    return res_edges


           

if __name__ == "__main__":
    main()

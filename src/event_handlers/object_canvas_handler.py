class ObjectCanvasHandler:

    def __init__(self) -> None:
        pass

def movement_handler(event, c):
    x, y = event.x, event.y
    c.delete("all")
    if x - 20 > 0 and y - 20 > 0:
        c.create_rectangle(x - 20, y - 20, x + 20, y + 20, outline="#fb0", fill="#fb0")
        c.create_text(x, y, fill="darkblue", font="Times 12 italic bold", text="Router")
    else:
        c.create_rectangle(x, y, x + 40, y + 40, outline="#fb0", fill="#fb0")
        c.create_text(x + 20, y + 20, fill="darkblue", font="Times 10 italic bold", text="Router")
    print('{}, {}'.format(x, y))
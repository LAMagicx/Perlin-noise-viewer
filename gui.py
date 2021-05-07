import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import os, time, noise, random, math, pygame

random.seed(round(time.time()))
np.random.seed(int(time.time()))

background_colour = '#333333'
text_colour = '#EEEEEE'
global img

def maps(value,istart,istop,ostart,ostop):
    return ostart+(ostop-ostart)*((value-istart)/(istop-istart))


def showMontain(world, lines = 10, den = 10):

    w,h = world.shape
    screen = pygame.Surface(world.shape)

    screen.fill([255,255,255])

    for i in range(h//lines):
        points = []
        for j in range(w//den):
            points.append([j*den, int(i*lines - maps(world[i*lines][j*den], 256, 0, 0, w//8)) + h//20])

        pygame.draw.lines(screen, (0,0,0), False, points, 1)

    screen = pygame.transform.scale(screen, (500,500))

    pygame.image.save(screen, "mountain.png")


def createFile(world, name="in.txt") : 

    w,h = world.shape
    txt = ""

    for y in range(h):
        for x in range(w):
            txt += str(round(maps(world[y][x], 256, 0, 0, 1))) + " "
        txt += "\n"

    with open(name, "w+") as f:
        f.truncate()
        f.write(txt)


def Create(shape=(100,100), base=0, size=1, scale = 50.0, level_of_detail = 9, amplitude = 0.5, diff_detail = 2, color = 'L', z=0):

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            g = noise.pnoise3(i/scale, 
                                        j/scale,
                                        z/scale,
                                        octaves=int(level_of_detail*size), 
                                        persistence=amplitude, 
                                        lacunarity=diff_detail, 
                                        repeatx=shape[0], 
                                        repeaty=shape[1], 
                                        base=base)
            world[i][j] = g
    
    world_min = np.min(world)
    world_max = np.max(world)


    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = maps(world[i][j], world_min, world_max, 256, 0)


    img = Image.fromarray(world)
    img = img.resize((500, 500), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    if shape[0] <= 100:
        lines = 5

    else:
        lines = 10

    # showMontain(world, lines = lines)
    createFile(world)

    return img


def slide_shape(arg):
    select = 'Shape: ' + str(shape_var.get())
    shapeValue.config(text=select)

def slide_detail(arg):
    select = 'Detail: ' + str(detail_var.get())
    detailValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def slide_amp(arg):
    select = 'amp: ' + str(amp_var.get())
    ampValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def slide_seed(arg):
    select = 'seed: ' + str(seed_var.get())
    seedValue.config(text=select)
    if int(shape_var.get())<=100:
        update()

def slide_diff(arg):
    select = 'diff: ' + str(diff_var.get())
    diffValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def slide_scale(arg):
    select = 'scale: ' + str(scale_var.get())
    scaleValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def slide_size(arg):
    select = 'size: ' + str(size_var.get())
    sizeValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def slide_Zoff(arg):
    select = 'Zoff: ' + str(Zoff_var.get())
    ZoffValue.config(text=select)
    if int(update_var.get()) == 0 or int(shape_var.get())<=100:
        update()

def update():
    if int(update_var.get()) == 0:
        color = 'L'
    else:
        color = 'L'
    img = Create(shape=(int(shape_var.get()),int(shape_var.get())), base=int(seed_var.get()),  scale = float(scale_var.get()), level_of_detail = int(detail_var.get()), amplitude = float(amp_var.get()), diff_detail = int(diff_var.get()), color = color, size = int(size_var.get()), z=float(Zoff_var.get()))
    image.configure(image=img)
    image.image = img


# def gen2():
#     shape_slider.set(maps(random(), 0, 1, 10, 100))
#     detail_slider.set(maps(random(), 0, 1, 4, 20))
#     amp_slider.set(maps(random(), 0, 1, 0.1, 1))
#     seed_slider.set(maps(random(), 0, 1, 1, 1000))
#     diff_slider.set(maps(random(), 0, 1, 0.2, 8))
#     scale_slider.set(maps(random(), 0, 1, 2, 200))
#     size_slider.set(maps(random(), 0, 1, 1, 10))
#     Zoff_slider.set(maps(random(), 0, 1, 0, 100))

#     update()

window = tk.Tk()

window.title("APP")

img = Create(shape=(100,100))

window.configure(background=background_colour)

# sidebar
sidebar = tk.Frame(window, width=200, bg='white', height=400, borderwidth=2)
sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
sidebar.configure(background=background_colour)

# main content area
mainarea = tk.Frame(window, bg='#CCC', width=500, height=500)
mainarea.pack(expand=True, fill='both', side='right')
mainarea.configure(background=background_colour)


image = tk.Label(mainarea, image=img, bg=background_colour)
image.pack()

buttons = tk.Frame(sidebar, bg = background_colour, width = 200, height = 100, borderwidth=0)
buttons.grid(row = 20, column = 0, sticky='S')

button = tk.Button(buttons, text="Create", width=12,  command=update)
button.grid(row=20, column=0, sticky='W')

# button = tk.Button(buttons, text="Random", width=12,  command=gen2)
# button.grid(row=20, column=1, sticky='E')

shape_var = tk.IntVar()

shape_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 10, to=750, resolution=10, orient='horizontal', command=slide_shape, variable=shape_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
shape_slider.grid(row=0, column=0, sticky='S')
shape_slider.set(100)


shapeValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
shapeValue.grid(row=1, column=0, sticky='N')

detail_var = tk.DoubleVar()

detail_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 4, to=20, resolution=0.2, orient='horizontal', command=slide_detail, variable=detail_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
detail_slider.grid(row=2, column=0, sticky='S')
detail_slider.set(9)


detailValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
detailValue.grid(row=3, column=0, sticky='N')

amp_var = tk.DoubleVar()

amp_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 0.1, to=1, resolution=0.01, orient='horizontal', command=slide_amp, variable=amp_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
amp_slider.grid(row=4, column=0, sticky='S')
amp_slider.set(0.5)


ampValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
ampValue.grid(row=5, column=0, sticky='N')

seed_var = tk.IntVar()

seed_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 0, to=1000, resolution=1, orient='horizontal', command=slide_seed, variable=seed_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
seed_slider.grid(row=6, column=0, sticky='S')
seed_slider.set(0)


seedValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
seedValue.grid(row=7, column=0, sticky='N')

diff_var = tk.DoubleVar()

diff_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 0.2, to=8, resolution=0.1, orient='horizontal', command=slide_diff, variable=diff_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
diff_slider.grid(row=8, column=0, sticky='S')
diff_slider.set(2.2)


diffValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
diffValue.grid(row=9, column=0, sticky='N')


scale_var = tk.DoubleVar()

scale_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 2, to=200, resolution=2, orient='horizontal', command=slide_scale, variable=scale_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
scale_slider.grid(row=10, column=0, sticky='S')
scale_slider.set(50.0)


scaleValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
scaleValue.grid(row=11, column=0, sticky='N')

size_var = tk.IntVar()

size_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 1, to=10, resolution=1, orient='horizontal', command=slide_size, variable=size_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
size_slider.grid(row=12, column=0, sticky='S')
size_slider.set(1)


sizeValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
sizeValue.grid(row=13, column=0, sticky='N')

Zoff_var = tk.DoubleVar()

Zoff_slider = tk.Scale(sidebar, bg=background_colour, fg=text_colour, from_ = 0, to=100, resolution=0.1, orient='horizontal', command=slide_Zoff, variable=Zoff_var, showvalue=0, activebackground="#FFFFFF", highlightbackground=background_colour, highlightcolor=background_colour, sliderlength=20, length=180)
Zoff_slider.grid(row=14, column=0, sticky='S')
Zoff_slider.set(0)


ZoffValue = tk.Label(sidebar, bg=background_colour, fg=text_colour)
ZoffValue.grid(row=15, column=0, sticky='N')


update_var = tk.IntVar()

update_box = tk.Checkbutton(sidebar, text="Update", variable=update_var, bg=background_colour, fg=text_colour, activebackground='#DDDDDD',activeforeground='#444444' , selectcolor='#222222', highlightcolor = background_colour)
update_box.grid(row=16, column=0, sticky='W')
update_box.select()





window.mainloop()

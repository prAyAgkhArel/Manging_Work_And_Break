from tkinter import *
import math
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"  #hexcodes of colors
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
checkmark = ""
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global checkmark
    global reps
    window.after_cancel(timer)
    canva.itemconfig(timer_text, text = "00:00")
    label_timer.config(text= "TIMER", fg= GREEN)
    checkmark = ""
    label_checkmark.config(text=checkmark)
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

# 0. 25min work, 1.  5min break, 2. 25min work,  3. 5min break,  4. 25min work , 5. 5 min break , 6. 25min work, 7. 20 min break
def timer_mechanism():
    if reps % 2 == 0:
        label_timer.config(text="WORK", fg=GREEN)
        return WORK_MIN * 60

    else:
        label_timer.config(text="BREAK", fg= RED)
        if reps % 7 == 0:
            return LONG_BREAK_MIN * 60
        else:
           return SHORT_BREAK_MIN * 60


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps
    global checkmark
    count_sec = count % 60
    count_min = math.floor(count/60)

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canva.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count>0:
        global timer
        timer = window.after(1000, count_down, count-1)
        # this calls count_down function after every 1000ms and count-1 is received by the argument count
        # each time it is called
        # we could do this by using time.sleep(1) using time module in a loop but if we do so window.mainloop()
        # is never executed so we use the process above calling the function recursively and using window.after()
        # functionality of tkinter

    if count == 0:
        reps+=1
        # creating notification sound after each reps

        pygame.mixer.init()
        pygame.mixer.music.load("simple-notification-152054.mp3")
        pygame.mixer.music.play()

        start_count()
        if reps%2 != 0:
            checkmark += "✔"
            label_checkmark.config(text=checkmark)

def start_count():
    count = timer_mechanism()
    count_down(count)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx= 100, pady= 50, bg = YELLOW)

tomato_image = PhotoImage(file="tomato.png")
canva = Canvas(width = 200, height= 224, bg= YELLOW, highlightthickness=0)
canva.create_image(100, 112, image = tomato_image)
timer_text = canva.create_text(103, 130, text="00:00",  font=(FONT_NAME, 32, "bold"))
canva.grid(row=1, column=1)

label_timer = Label(text= "Timer", font=(FONT_NAME, 50, "bold"), fg= GREEN, bg=YELLOW)
label_timer.grid(row=0, column=1)

start_button = Button(text="Start", highlightthickness=0, command=start_count)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightthickness=0, command= reset_timer)
reset_button.grid(row=2, column=2)

label_checkmark = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 10, "bold"))
label_checkmark.grid(row=3, column =1)


window.mainloop()


### to improve: ADD alarm or notifications after each reps(work or break) #doneee

import tkinter as tk
import time
import math

# ==================== COLORS ====================

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
BLUE = "#0284C7"
BLUE_HOVER = "#0369A1"
TEXT_COLOR = "#F8FAFC"
MUTED_COLOR = "#CBD5E1"
ERROR_COLOR = "#F87171"
GREEN_COLOR = "#4ADE80"

TEST_DURATION = 60

PASSAGE = (
    "Python is a simple and powerful programming language. "
    "Practice typing every day to improve your speed and accuracy."
)

# ==================== MAIN WINDOW ====================

root = tk.Tk()
root.title("TypeSprint - Typing Speed Tester")
root.geometry("900x700")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ==================== TEST VARIABLES ====================

time_left = TEST_DURATION
start_time = None
timer_running = False
timer_job = None

# ==================== HEADER ====================

heading = tk.Label(
    root,
    text="TypeSprint",
    font=("Arial", 30, "bold"),
    bg=BG_COLOR,
    fg="#38BDF8"
)
heading.pack(pady=(20, 4))

subtitle = tk.Label(
    root,
    text="Test Your Typing Speed and Accuracy",
    font=("Arial", 13),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)
subtitle.pack(pady=(0, 20))

# ==================== STATISTICS DASHBOARD ====================

stats_frame = tk.Frame(root, bg=BG_COLOR)
stats_frame.pack(pady=5)

def create_stat_card(parent, title, value, value_color= "#38BDF8"):
    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        width=200,
        height=95
    )
    card.pack(side="left", padx=5)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        bg=CARD_COLOR,
        fg=MUTED_COLOR
    ).pack(pady=(13, 5))

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 21, "bold"),
        bg=CARD_COLOR,
        fg=value_color
    )
    value_label.pack()

    return value_label


timer_value = create_stat_card(
    stats_frame, "TIME LEFT", "60 sec"
)

wpm_value = create_stat_card(
    stats_frame, "SPEED", "0 WPM"
)

accuracy_value = create_stat_card(
    stats_frame, "ACCURACY", "100%"
)

mistakes_value = create_stat_card(
    stats_frame, "MISTAKES", "0", ERROR_COLOR
)

# ==================== PASSAGE SECTION ====================

passage_heading = tk.Label(
    root,
    text="Type the following passage:",
    font=("Arial", 13, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
passage_heading.pack(anchor="w", padx=35, pady=(20, 8))

passage_box = tk.Text(
    root,
    height=4,
    font=("Arial", 12),
    wrap="word",
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    padx=12,
    pady=12,
    spacing1=4
)
passage_box.pack(fill="x", padx=30)

passage_box.insert("1.0", PASSAGE)
passage_box.config(state="disabled")

# ==================== TYPING SECTION ====================

typing_heading = tk.Label(
    root,
    text="Your typing area:",
    font=("Arial", 13, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
typing_heading.pack(anchor="w", padx=35, pady=(17, 8))

typing_box = tk.Text(
    root,
    height=4,
    font=("Arial", 12),
    wrap="word",
    bg="#F8FAFC",
    fg="#0F172A",
    insertbackground="#0F172A",
    relief="flat",
    padx=12,
    pady=12,
    spacing1=4,
    undo=False
)
typing_box.pack(fill="x", padx=30)
typing_box.config(state="disabled")

# ==================== STATUS MESSAGE ====================

status_label = tk.Label(
    root,
    text="Click Start Test when you are ready.",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)
status_label.pack(pady=(10, 0))

# ==================== STATISTICS CALCULATION ====================

def update_statistics(event=None):
    typed_text = typing_box.get("1.0", "end-1c")

    correct_chars = 0
    mistakes = 0

    for index, character in enumerate(typed_text):
        if index < len(PASSAGE):
            if character == PASSAGE[index]:
                correct_chars += 1
            else:
                mistakes += 1
        else:
            mistakes += 1

    if len(typed_text) > 0:
        accuracy = (correct_chars / len(typed_text)) * 100
    else:
        accuracy = 100.0

    if start_time is not None:
        elapsed_time = time.time() - start_time
    else:
        elapsed_time = 0

    if elapsed_time > 0:
        # Standard net WPM calculation
        wpm = (correct_chars / 5) / (elapsed_time / 60)
    else:
        wpm = 0

    wpm_value.config(text=f"{wpm:.0f} WPM")
    accuracy_value.config(text=f"{accuracy:.0f}%")
    mistakes_value.config(text=str(mistakes))

# ==================== TIMER ====================

def update_timer():
    global time_left, timer_running, timer_job

    timer_job = None

    if not timer_running:
        return

    elapsed_time = time.time() - start_time
    time_left = max(0, TEST_DURATION - math.floor(elapsed_time))

    timer_value.config(text=f"{time_left} sec")
    update_statistics()

    if time_left <= 0:
        finish_test()
    else:
        timer_job = root.after(100, update_timer)

# ==================== FINISH TEST ====================

def finish_test():
    global timer_running, timer_job

    timer_running = False

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    typing_box.config(state="disabled")
    update_statistics()

    start_button.config(
        text="Test Finished",
        bg="#475569"
    )

    status_label.config(
        text=(
            f"Test completed! Final speed: "
            f"{wpm_value.cget('text')} | "
            f"Accuracy: {accuracy_value.cget('text')}"
        ),
        fg=GREEN_COLOR
    )

# ==================== START TEST ====================

def start_test():
    global timer_running, start_time, timer_job

    if timer_running:
        return

    if time_left <= 0:
        return

    timer_running = True
    start_time = time.time()

    typing_box.config(state="normal")
    typing_box.focus_set()

    start_button.config(
        text="Test Running...",
        bg=BLUE
    )

    status_label.config(
        text="Type the passage as accurately as possible.",
        fg=MUTED_COLOR
    )

    timer_job = root.after(100, update_timer)

# ==================== RESET TEST ====================

def reset_test():
    global time_left, start_time, timer_running, timer_job

    timer_running = False

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    time_left = TEST_DURATION
    start_time = None

    timer_value.config(text="60 sec")
    wpm_value.config(text="0 WPM")
    accuracy_value.config(text="100%")
    mistakes_value.config(text="0")

    typing_box.config(state="normal")
    typing_box.delete("1.0", "end")
    typing_box.config(state="disabled")

    start_button.config(
        text="Start Test",
        bg=BLUE
    )

    status_label.config(
        text="Click Start Test when you are ready.",
        fg=MUTED_COLOR
    )

# ==================== CUSTOM BUTTONS ====================

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=15)

def create_custom_button(parent, text, color, hover_color, command):
    button = tk.Label(
        parent,
        text=text,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="white",
        width=16,
        height=2,
        cursor="hand2"
    )
    button.pack(side="left", padx=10)

    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover_color)
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(bg=color)
    )

    button.bind(
        "<Button-1>",
        lambda event: command()
    )

    return button


start_button = create_custom_button(
    button_frame,
    "Start Test",
    BLUE,
    BLUE_HOVER,
    start_test
)

reset_button = create_custom_button(
    button_frame,
    "Reset",
    "#334155",
    "#475569",
    reset_test
)

# Update statistics whenever the user types
typing_box.bind("<KeyRelease>", update_statistics)

# ==================== START APPLICATION ====================

root.mainloop()

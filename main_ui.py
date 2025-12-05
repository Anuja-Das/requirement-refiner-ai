# python
import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import json
import os
import threading
import time
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INPUT_FILE = os.path.join(DATA_DIR, "requirement_input.txt")
ANALYSIS_FILE = os.path.join(DATA_DIR, "analysis_output.json")
FINAL_FILE = os.path.join(DATA_DIR, "final_requirement_output.json")

spinner_running = False
results_visible = False
worker_proc = None
cancel_event = threading.Event()

def run_spinner():
    spinner_chars = ["|", "/", "-", "\\"]
    idx = 0
    while spinner_running:
        spinner_label.config(text=f"Processing… {spinner_chars[idx]}")
        idx = (idx + 1) % len(spinner_chars)
        time.sleep(0.15)
    spinner_label.config(text="")

def set_readonly(widget, text):
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, text)
    widget.config(state="disabled")

def pipeline_worker(user_text):
    global worker_proc
    # long-running work runs in background thread
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        f.write(user_text)

    try:
        # start subprocess so it can be terminated if requested
        worker_proc = subprocess.Popen([sys.executable, "main.py"])
        # poll loop so we can respond to cancel_event
        while True:
            if cancel_event.is_set():
                # stop the subprocess if requested
                try:
                    if worker_proc and worker_proc.poll() is None:
                        worker_proc.terminate()
                        try:
                            worker_proc.wait(timeout=1)
                        except Exception:
                            worker_proc.kill()
                except Exception:
                    pass
                # exit without scheduling finish (stop_pipeline already handled UI)
                worker_proc = None
                return

            if worker_proc.poll() is not None:
                break
            time.sleep(0.1)

        worker_proc = None

        analysis_text = ""
        final_text = ""

        if os.path.exists(ANALYSIS_FILE):
            with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
                analysis_text = json.dumps(json.load(f), indent=4)

        if os.path.exists(FINAL_FILE):
            with open(FINAL_FILE, "r", encoding="utf-8") as f:
                final_text = json.dumps(json.load(f), indent=4)

        # schedule UI update on main thread if not cancelled
        if not cancel_event.is_set():
            root.after(0, finish_pipeline, analysis_text, final_text)

    except Exception as e:
        worker_proc = None
        # schedule an error message
        root.after(0, finish_pipeline, f"Error: {e}", "")

def run_pipeline():
    global spinner_running, cancel_event
    user_text = input_box.get("1.0", tk.END).strip()

    # reset cancel event
    cancel_event.clear()

    # show and start progress bar on main thread
    progress_bar.pack(pady=5, anchor="center")
    spinner_running = True
    progress_bar.start(10)
    threading.Thread(target=run_spinner, daemon=True).start()

    # toggle buttons
    submit_btn.config(state="disabled")
    stop_btn.config(state="normal")

    # start background worker with the user text
    threading.Thread(target=pipeline_worker, args=(user_text,), daemon=True).start()

def _show_results_once(analysis_text, final_text):
    global results_visible
    set_readonly(analysis_output_box, analysis_text)
    set_readonly(final_output_box, final_text)
    if not results_visible:
        analysis_label.pack(anchor="center")
        analysis_output_box.pack(pady=5, anchor="center")
        final_label.pack(anchor="center")
        final_output_box.pack(pady=5, anchor="center")
        results_visible = True

def finish_pipeline(analysis_text, final_text):
    global spinner_running
    # populate outputs (on main thread) and show result widgets
    _show_results_once(analysis_text, final_text)

    spinner_running = False
    progress_bar.stop()
    progress_bar.pack_forget()

    # toggle buttons
    submit_btn.config(state="normal")
    stop_btn.config(state="disabled")

def stop_pipeline():
    global spinner_running, cancel_event, worker_proc
    # signal cancellation
    cancel_event.set()

    # terminate subprocess if still running
    try:
        if worker_proc and worker_proc.poll() is None:
            worker_proc.terminate()
            try:
                worker_proc.wait(timeout=1)
            except Exception:
                worker_proc.kill()
    except Exception:
        pass
    worker_proc = None

    # stop spinner/progress UI
    spinner_running = False
    progress_bar.stop()
    progress_bar.pack_forget()
    spinner_label.config(text="")

    # show cancellation message in outputs
    _show_results_once("Operation canceled by user.", "Operation canceled by user.")

    # toggle buttons
    submit_btn.config(state="normal")
    stop_btn.config(state="disabled")

# ---------------- UI START  ----------------

root = tk.Tk()
root.title("Requirement Refiner AI")
root.geometry("1100x900")

# Canvas wrapper for total window scroll
main_canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollbar.pack(side="right", fill="y")
main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.pack(side="left", fill="both", expand=True)

container = tk.Frame(main_canvas)
window_id = main_canvas.create_window((0, 0), window=container, anchor="nw")

def configure_scroll_region(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

container.bind("<Configure>", configure_scroll_region)

# keep the container width equal to the canvas width so children can be centered
def on_canvas_config(event):
    main_canvas.itemconfig(window_id, width=event.width)

main_canvas.bind("<Configure>", on_canvas_config)

# Center inside the container
frame = tk.Frame(container)
frame.pack(anchor="center", pady=20)

# Enable mouse/touchpad scrolling for the canvas when pointer is over the container

def _on_mousewheel_windows(event):
    # event.delta is multiples of 120 on Windows
    main_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

def _on_mousewheel_linux(event):
    # Linux uses Button-4 / Button-5 events
    if event.num == 4:
        main_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        main_canvas.yview_scroll(1, "units")

def _bind_mousewheel(_event=None):
    # Bind appropriate events when pointer is over the container
    if os.name == "nt":
        root.bind_all("<MouseWheel>", _on_mousewheel_windows)
    else:
        root.bind_all("<Button-4>", _on_mousewheel_linux)
        root.bind_all("<Button-5>", _on_mousewheel_linux)

def _unbind_mousewheel(_event=None):
    # Unbind when pointer leaves the container
    if os.name == "nt":
        root.unbind_all("<MouseWheel>")
    else:
        root.unbind_all("<Button-4>")
        root.unbind_all("<Button-5>")

# attach enter/leave to the container (works when pointer is anywhere inside the canvas window)
container.bind("<Enter>", _bind_mousewheel)
container.bind("<Leave>", _unbind_mousewheel)

# ---------------- UI ELEMENTS ----------------

heading = tk.Label(frame, text="Requirement Refiner AI", font=("Arial", 18, "bold"))
heading.pack(pady=10, anchor="center")

progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=400)
# do NOT pack the progress_bar here so it is hidden at startup

spinner_label = tk.Label(frame, text="", font=("Arial", 12))
spinner_label.pack(anchor="center")

input_label = tk.Label(frame, text="Enter raw requirement:")
input_label.pack(anchor="center")

input_box = scrolledtext.ScrolledText(frame, width=120, height=5, font=("Arial", 10))
input_box.pack(pady=5, anchor="center")

# buttons frame with Refine and Stop
buttons_frame = tk.Frame(frame)
buttons_frame.pack(pady=10, anchor="center")

submit_btn = tk.Button(buttons_frame, text="Refine", command=run_pipeline, font=("Arial", 12))
submit_btn.pack(side="left", padx=6)

stop_btn = tk.Button(buttons_frame, text="Stop", command=stop_pipeline, font=("Arial", 12), state="disabled")
stop_btn.pack(side="left", padx=6)

# Create result widgets but do NOT pack them yet; they will be shown in finish_pipeline
analysis_label = tk.Label(frame, text="Analysis:")
analysis_output_box = scrolledtext.ScrolledText(frame, width=120, height=10, font=("Arial", 10))
analysis_output_box.config(state="disabled")   # start read-only

final_label = tk.Label(frame, text="Refined requirement:")
final_output_box = scrolledtext.ScrolledText(frame, width=120, height=10, font=("Arial", 10))
final_output_box.config(state="disabled")      # start read-only

root.mainloop()
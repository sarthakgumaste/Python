import threading
import time
import tempfile
import os

results = []
results_lock = threading.Lock()
START = time.perf_counter()


def record(task_name, message):
    elapsed = time.perf_counter() - START
    with results_lock:                     
        results.append(f"[{elapsed:5.2f}s] {task_name:<10} {message}")
        print(results[-1])

def compute_squares(n=5):
    record("Compute", "started")
    total = 0
    for i in range(1, n + 1):
        time.sleep(0.3)                    
        total += i * i
    record("Compute", f"finished, sum of squares 1..{n} = {total}")


def write_file(path, lines=5):
    record("FileWrite", "started")
    with open(path, "w") as f:
        for i in range(1, lines + 1):
            f.write(f"line {i}\n")
            time.sleep(0.2)
    record("FileWrite", f"finished, wrote {lines} lines")


def fake_download(name="report.pdf", seconds=1.0):
    record("Download", f"started {name}")
    time.sleep(seconds)
    record("Download", f"finished {name}")

def run_sequential(path):
    t0 = time.perf_counter()
    compute_squares()
    write_file(path)
    fake_download()
    return time.perf_counter() - t0


def run_threaded(path):
    t0 = time.perf_counter()
    threads = [
        threading.Thread(target=compute_squares, name="T-Compute"),
        threading.Thread(target=write_file, args=(path,), name="T-File"),
        threading.Thread(target=fake_download, kwargs={"name": "data.zip"},
                         name="T-Download"),
    ]
    for t in threads:
        t.start()                  
    for t in threads:
        t.join()                   
    return time.perf_counter() - t0


if __name__ == "__main__":
    out = os.path.join(tempfile.gettempdir(), "thread_demo.txt")

    print("=== A) SEQUENTIAL (one task after another) ===")
    t_seq = run_sequential(out)

    results.clear()
    START = time.perf_counter()
    print("\n=== B) THREADED (all tasks together) ===")
    t_thr = run_threaded(out)

    print(f"\nSequential time : {t_seq:.2f} s")
    print(f"Threaded time   : {t_thr:.2f} s")
    print(f"Speed-up        : {t_seq / t_thr:.1f}x faster")
    print(f"Active threads at end: {threading.active_count()} (main only)")
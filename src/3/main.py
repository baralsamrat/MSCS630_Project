#!/usr/bin/env python3
"""
Memory Management and Process Synchronization Simulation with Enhanced Visualization

This script simulates:
1. Memory Management with a paging system:
   - Each process is allocated pages in fixed-size frames.
   - Handles page faults when a page is missing.
   - Implements two page replacement algorithms: FIFO and LRU.
   - Tracks memory usage and page fault counts.
   - Generates bar charts for page fault counts and line graphs for memory usage over time using Matplotlib.
     Graphs are saved to the directory "../screenshot/3".

2. Process Synchronization:
   - Implements the Producer-Consumer problem.
   - Uses semaphores and a mutex to synchronize access to a shared buffer.
"""

import os
import time
import random
import threading
from collections import OrderedDict

# Try to import rich for enhanced terminal output.
try:
    from rich import print as rprint
    from rich.console import Console
    console = Console()
except ImportError:
    rprint = print
    console = None

# Define the output directory for graphs
OUTPUT_DIR = os.path.join("graphs", "3")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    rprint(f"[blue]Created directory for graphs:[/blue] {OUTPUT_DIR}")

# -------------------------------------
# Memory Management: Paging System
# -------------------------------------
class MemoryManager:
    def __init__(self, total_frames, algorithm='FIFO'):
        self.total_frames = total_frames  # Maximum number of frames in memory.
        self.algorithm = algorithm.upper()
        self.frames = {}            # Maps process_id -> list of pages in memory.
        self.page_faults = {}       # Tracks page faults per process.

        # For FIFO, we use a list to track insertion order.
        # For LRU, we use an OrderedDict for efficient reordering.
        if self.algorithm == 'FIFO':
            self.frame_list = []    # List of (process_id, page) tuples.
            self.lru_usage = None
        elif self.algorithm == 'LRU':
            self.lru_usage = OrderedDict()  # Keys: (process_id, page); Value is unused.
            self.frame_list = None
        else:
            raise ValueError("Unsupported algorithm. Use FIFO or LRU.")

    def load_page(self, process_id, page):
        """Simulate loading a page for a process, handling page faults as needed."""
        if process_id not in self.frames:
            self.frames[process_id] = []

        # Check if the page is already in memory.
        if page in self.frames[process_id]:
            rprint(f"[green][Process {process_id}][/green] Page {page} accessed (in memory).")
            if self.algorithm == 'LRU':
                key = (process_id, page)
                self.lru_usage.move_to_end(key)
            return False  # No page fault.

        # Page fault occurs.
        rprint(f"[red][Process {process_id}][/red] *** Page {page} fault! ***")
        self.page_faults.setdefault(process_id, 0)
        self.page_faults[process_id] += 1

        # If memory is full, replace a page.
        if self.get_total_pages() >= self.total_frames:
            self.replace_page(process_id, page)
        else:
            self._add_page(process_id, page)
        return True

    def _add_page(self, process_id, page):
        """Helper to add a page without needing replacement."""
        self.frames[process_id].append(page)
        if self.algorithm == 'FIFO':
            self.frame_list.append((process_id, page))
        elif self.algorithm == 'LRU':
            self.lru_usage[(process_id, page)] = None

    def replace_page(self, process_id, page):
        """Replace a page using the selected algorithm when memory is full."""
        if self.algorithm == 'FIFO':
            victim_pid, victim_page = self.frame_list.pop(0)
            self.frames[victim_pid].remove(victim_page)
            rprint(f"[bold yellow][FIFO][/bold yellow] Replacing: Removed page {victim_page} from process {victim_pid}")
        elif self.algorithm == 'LRU':
            (victim_pid, victim_page), _ = self.lru_usage.popitem(last=False)
            self.frames[victim_pid].remove(victim_page)
            rprint(f"[bold yellow][LRU][/bold yellow] Replacing: Removed page {victim_page} from process {victim_pid}")
        else:
            rprint("[red]Unknown algorithm. No replacement performed.[/red]")
            return

        self._add_page(process_id, page)

    def get_total_pages(self):
        """Return the total number of pages currently loaded."""
        return sum(len(pages) for pages in self.frames.values())

    def deallocate_process(self, process_id):
        """Deallocate (free) all pages for the specified process."""
        if process_id in self.frames:
            rprint(f"[blue][Process {process_id}][/blue] Deallocating all pages.")
            if self.algorithm == 'FIFO':
                self.frame_list = [item for item in self.frame_list if item[0] != process_id]
            elif self.algorithm == 'LRU':
                keys_to_remove = [key for key in self.lru_usage if key[0] == process_id]
                for key in keys_to_remove:
                    del self.lru_usage[key]
            del self.frames[process_id]

    def print_status(self):
        """Print the current memory allocation and page fault statistics."""
        rprint("\n[bold underline]--- Memory Status ---[/bold underline]")
        for pid, pages in self.frames.items():
            rprint(f"[cyan]Process {pid}:[/cyan] Pages {pages}")
        rprint(f"[magenta]Page Faults per process:[/magenta] {self.page_faults}")
        rprint("[bold underline]----------------------[/bold underline]\n")


# --------------------------------------------
# Process Synchronization: Producer-Consumer
# --------------------------------------------
class ProducerConsumer:
    def __init__(self, buffer_size=5, num_items=10):
        self.buffer = []                # Shared buffer.
        self.buffer_size = buffer_size  # Maximum number of items in the buffer.
        self.num_items = num_items      # Total items to produce/consume.
        self.empty = threading.Semaphore(buffer_size)  # Tracks empty slots.
        self.full = threading.Semaphore(0)             # Tracks filled slots.
        self.mutex = threading.Lock()                  # Ensures mutual exclusion.

    def producer(self):
        for i in range(self.num_items):
            self.empty.acquire()  # Wait for an empty slot.
            with self.mutex:
                item = f"Item-{i}"
                self.buffer.append(item)
                rprint(f"[bold green][Producer][/bold green] Produced {item}. Buffer: {self.buffer}")
            self.full.release()   # Signal that an item is available.
            time.sleep(random.uniform(0.1, 0.3))

    def consumer(self):
        for i in range(self.num_items):
            self.full.acquire()   # Wait until an item is available.
            with self.mutex:
                item = self.buffer.pop(0)
                rprint(f"[bold blue][Consumer][/bold blue] Consumed {item}. Buffer: {self.buffer}")
            self.empty.release()  # Signal that a slot is free.
            time.sleep(random.uniform(0.1, 0.3))

    def run(self):
        prod_thread = threading.Thread(target=self.producer)
        cons_thread = threading.Thread(target=self.consumer)
        prod_thread.start()
        cons_thread.start()
        prod_thread.join()
        cons_thread.join()


# --------------------------------------------
# Visualization Functions
# --------------------------------------------
def plot_memory_stats(page_faults, algorithm):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        rprint("[red]Matplotlib is not installed. Skipping visualization.[/red]")
        return

    processes = list(page_faults.keys())
    faults = [page_faults[pid] for pid in processes]

    plt.figure(figsize=(6, 4))
    plt.bar(processes, faults, color='skyblue')
    plt.title(f"Page Faults per Process ({algorithm})")
    plt.xlabel("Process ID")
    plt.ylabel("Page Fault Count")
    plt.xticks(processes)
    plt.tight_layout()
    # Save the graph in the specified output directory.
    save_path = os.path.join(OUTPUT_DIR, f"page_faults_{algorithm}.png")
    plt.savefig(save_path)
    rprint(f"[blue]Saved graph:[/blue] {save_path}")
    plt.show()

def plot_memory_usage(usage_list, algorithm):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        rprint("[red]Matplotlib is not installed. Skipping memory usage visualization.[/red]")
        return

    steps = list(range(1, len(usage_list) + 1))
    plt.figure(figsize=(6, 4))
    plt.plot(steps, usage_list, marker='o', linestyle='-', color='green')
    plt.title(f"Memory Usage Over Time ({algorithm})")
    plt.xlabel("Step")
    plt.ylabel("Total Pages Loaded")
    plt.tight_layout()
    # Save the graph in the specified output directory.
    save_path = os.path.join(OUTPUT_DIR, f"memory_usage_{algorithm}.png")
    plt.savefig(save_path)
    rprint(f"[blue]Saved graph:[/blue] {save_path}")
    plt.show()


# --------------------------------------------
# Simulation Entry Points
# --------------------------------------------
def simulate_memory_management():
    processes = [1, 2]
    page_requests = {
        1: [1, 2, 3, 1, 4],
        2: [1, 2, 1, 3, 5]
    }

    # --- FIFO Simulation with Memory Usage Recording ---
    usage_fifo = []  # Record total pages loaded after each page request.
    rprint("[bold blue]=== Memory Management Simulation: FIFO ===[/bold blue]")
    mm_fifo = MemoryManager(total_frames=5, algorithm='FIFO')
    for pid in processes:
        for page in page_requests[pid]:
            mm_fifo.load_page(pid, page)
            usage_fifo.append(mm_fifo.get_total_pages())
            time.sleep(0.15)
    mm_fifo.print_status()
    plot_memory_stats(mm_fifo.page_faults, "FIFO")
    plot_memory_usage(usage_fifo, "FIFO")

    # --- LRU Simulation with Memory Usage Recording ---
    usage_lru = []
    rprint("[bold blue]=== Memory Management Simulation: LRU ===[/bold blue]")
    mm_lru = MemoryManager(total_frames=5, algorithm='LRU')
    for pid in processes:
        for page in page_requests[pid]:
            mm_lru.load_page(pid, page)
            usage_lru.append(mm_lru.get_total_pages())
            time.sleep(0.15)
    mm_lru.print_status()
    plot_memory_stats(mm_lru.page_faults, "LRU")
    plot_memory_usage(usage_lru, "LRU")


def simulate_process_synchronization():
    rprint("[bold blue]=== Process Synchronization Simulation: Producer-Consumer ===[/bold blue]")
    pc = ProducerConsumer(buffer_size=5, num_items=10)
    pc.run()


if __name__ == "__main__":
    simulate_memory_management()
    simulate_process_synchronization()

import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
from collections import Counter

def summarize_with_keywords(text, keywords, num_sentences=2):
    # Split text into sentences properly
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    # Count word frequencies
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)

    # Score each sentence
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        # Add score based on word frequency
        for word in sentence.lower().split():
            score += word_freq.get(word, 0)
        # Add bonus points for keywords
        for kw in keywords:
            if kw.lower() in sentence.lower():
                score += 10   # made keyword weight stronger
        # Prevents duplicate sentences being chosen
        if sentence.strip():
            sentence_scores[sentence.strip()] = score

    # Sort by score (highest first) and keep top N
    best_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]

    # Join them in the order they appeared in the text of the summary 
    ordered_summary = [s for s in sentences if s.strip() in best_sentences]

    return " ".join(ordered_summary)

# --- GUI Functions ---
def run_summary():
    notes = input_text.get(1.0, tk.END).strip()
    if not notes:
        messagebox.showwarning("Warning", "No text to summarize!")
        return

    keywords_input = keyword_entry.get().strip()
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()] or ["important", "main", "key", "exam"]

    try:
        num_sentences = int(sentences_entry.get().strip() or 3)
    except ValueError:
        num_sentences = 3

    summary = summarize_with_keywords(notes, keywords, num_sentences)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, summary)

# --- Main Window ---
root = tk.Tk()
root.title("AI Notes Summarizer")
root.geometry("800x600")

# Input text area
tk.Label(root, text="Paste your notes here:").pack()
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
input_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Controls
control_frame = tk.Frame(root)
control_frame.pack(pady=5)

tk.Label(control_frame, text="Keywords:").grid(row=0, column=0, padx=5)
keyword_entry = tk.Entry(control_frame, width=30)
keyword_entry.grid(row=0, column=1, padx=5)

tk.Label(control_frame, text="Sentences:").grid(row=0, column=2, padx=5)
sentences_entry = tk.Entry(control_frame, width=5)
sentences_entry.grid(row=0, column=3, padx=5)

tk.Button(control_frame, text="Summarize", command=run_summary).grid(row=0, column=4, padx=5)

# Output text area (where summary appears)
tk.Label(root, text="Summary:").pack()
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
output_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Run app
root.mainloop()



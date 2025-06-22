import tkinter as tk
from tkinter import filedialog, messagebox
import re

class TextSummaryAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 File Reader + Summary + Readability")
        self.root.geometry("750x650")

        tk.Button(root, text="📂 Load .txt File", font=("Arial", 12), command=self.load_file).pack(pady=5)

        self.input_text = tk.Text(root, height=12, width=85, font=("Arial", 11))
        self.input_text.pack(pady=5)

        tk.Button(root, text="🧠 Generate Summary", font=("Arial", 12), command=self.summarize_text).pack(pady=5)
        self.summary_text = tk.Text(root, height=8, width=85, font=("Arial", 11))
        self.summary_text.pack(pady=5)

        tk.Button(root, text="💾 Save Summary", font=("Arial", 12), command=self.save_summary).pack(pady=5)

        tk.Button(root, text="📈 Analyze Readability", font=("Arial", 12), command=self.analyze_text).pack(pady=5)
        self.stats_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
        self.stats_label.pack(pady=5)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def summarize_text(self, n=3):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "No text to summarize.")
            return
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 20]
        sentences.sort(key=lambda s: len(s), reverse=True)
        summary = ". ".join(sentences[:n]) + "."
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def save_summary(self):
        content = self.summary_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("Info", "Nothing to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Saved", f"Summary saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def analyze_text(self):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "No text to analyze.")
            return

        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        syllables = sum(self.count_syllables(word) for word in words)

        word_count = len(words)
        sentence_count = max(1, len([s for s in sentences if s.strip()]))
        syllable_count = syllables

        # Readability scores
        flesch = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
        grade = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count / word_count) - 15.59

        self.stats_label.config(text=f"""
📊 Word Count: {word_count}
🧾 Sentence Count: {sentence_count}
🔠 Syllable Count: {syllable_count}

📈 Flesch Reading Ease: {flesch:.2f} (higher = easier)
📚 Flesch-Kincaid Grade Level: {grade:.2f}
        """, anchor="w", justify="left")

    def count_syllables(self, word):
        word = word.lower()
        word = re.sub(r'[^a-z]', '', word)
        if len(word) == 0: return 0
        vowels = "aeiouy"
        count = 0
        if word[0] in vowels: count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                count += 1
        if word.endswith("e"): count -= 1
        if count == 0: count = 1
        return count

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    TextSummaryAnalyzer(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

print("Starting the GUI...")

library = Library()
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")

# ========== Functions ==========
def toggle_ebook_field():
    if ebook_var.get():
        size_entry.config(state="normal")
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state="disabled")

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "All fields except size are required.")
        return

    if is_ebook:
        if not size or not size.isdigit():
            messagebox.showerror("Error", "Size must be a number for eBooks.")
            return
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", "Book added.")
    clear_fields()
    update_book_list()

def update_book():
    isbn = simpledialog.askstring("Update Book", "Enter ISBN of the book to update:")
    if isbn:
        book = library.find_book(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return
        new_title = simpledialog.askstring("Update Title", "Enter new title:", initialvalue=book.title)
        new_author = simpledialog.askstring("Update Author", "Enter new author:", initialvalue=book.author)
        new_size = None
        if isinstance(book, EBook):
            new_size = simpledialog.askstring("Update Size", "Enter new size (MB):", initialvalue=book.download_size)

        library.update_book(isbn, new_title, new_author, new_size)
        messagebox.showinfo("Updated", "Book updated.")
        update_book_list()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Author Search", "Enter author name:")
    if author:
        books = list(library.books_by_author(author))
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, f"Books by {author}:")
        listbox.insert(tk.END, "-"*80)
        for book in books:
            listbox.insert(tk.END, str(book))
        listbox.insert(tk.END, "")
        listbox.insert(tk.END, "Click below to return to full list")
        tk.Button(root, text="Back to Full List", command=update_book_list).pack(pady=5)

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, f"{'Title':<25} {'Author':<20} {'ISBN':<15} Type")
    listbox.insert(tk.END, "-"*80)
    for book in library:
        listbox.insert(tk.END, str(book))

def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)
    ebook_var.set(False)
    toggle_ebook_field()

# ========== UI Layout ==========
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="e")
title_entry = tk.Entry(form_frame, width=40)
title_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky="e")
author_entry = tk.Entry(form_frame, width=40)
author_entry.grid(row=1, column=1)

tk.Label(form_frame, text="ISBN:").grid(row=2, column=0, sticky="e")
isbn_entry = tk.Entry(form_frame, width=40)
isbn_entry.grid(row=2, column=1)

ebook_var = tk.BooleanVar()
ebook_check = tk.Checkbutton(form_frame, text="eBook?", variable=ebook_var, command=toggle_ebook_field)
ebook_check.grid(row=3, column=1, sticky="w")

tk.Label(form_frame, text="Size (MB):").grid(row=4, column=0, sticky="e")
size_entry = tk.Entry(form_frame, width=40, state="disabled")
size_entry.grid(row=4, column=1)

# ========== Buttons ==========
button_frame = tk.Frame(root)
button_frame.pack()

tk.Button(button_frame, text="Add Book", command=add_book, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Update Book", command=update_book, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Lend Book", command=lend_book, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Return Book", command=return_book, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Remove Book", command=remove_book, width=20).grid(row=2, column=0, padx=5, pady=5)
tk.Button(button_frame, text="View Books by Author", command=view_books_by_author, width=42).grid(row=2, column=1, pady=5)

# ========== Book List ==========
tk.Label(root, text="Library Inventory:").pack()
listbox = tk.Listbox(root, width=100)
listbox.pack(pady=10)

update_book_list()
root.mainloop()

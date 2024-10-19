import tkinter as tk
from tkinter import ttk, messagebox
from sympy import sympify, symbols, Matrix, solve, lambdify
import numpy as np
import matplotlib.pyplot as plt

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ماشین حساب پیشرفته")
        self.root.geometry("1400x1000")  # افزایش ابعاد پنجره اصلی
        self.root.configure(bg="lightblue")  # تغییر رنگ پس‌زمینه پنجره به آبی

        self.equation = tk.StringVar()

        # ایجاد نوار تب‌ها
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # ایجاد تب‌ها
        self.base_frame = ttk.Frame(self.notebook, bg="lightblue")  # تغییر رنگ پس‌زمینه تب به آبی
        self.notebook.add(self.base_frame, text="ماشین حساب")

        self.scientific_frame = ttk.Frame(self.notebook, bg="lightblue")  # تغییر رنگ پس‌زمینه تب به آبی
        self.notebook.add(self.scientific_frame, text="ماشین حساب علمی")

        self.cpp_frame = ttk.Frame(self.notebook, bg="lightblue")  # تغییر رنگ پس‌زمینه تب به آبی
        self.notebook.add(self.cpp_frame, text="کد C++")

        self.python_frame = ttk.Frame(self.notebook, bg="lightblue")  # تغییر رنگ پس‌زمینه تب به آبی
        self.notebook.add(self.python_frame, text="کد Python")

        # نمایشگر معادله
        self.display = tk.Text(self.base_frame, height=6, width=80, font=("Arial", 24), bg="white", fg="black")  # پس‌زمینه نمایشگر سفید
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # ایجاد قاب برای دکمه‌ها و اسکرول بار
        self.button_canvas = tk.Canvas(self.base_frame, bg="lightblue")  # تغییر رنگ پس‌زمینه کانواس به آبی
        self.button_canvas.grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.button_frame = ttk.Frame(self.button_canvas, bg="lightblue")  # تغییر رنگ پس‌زمینه فریم دکمه‌ها به آبی
        self.button_frame.bind(
            "<Configure>",
            lambda e: self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all"))
        )

        self.button_canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        self.vsb = tk.Scrollbar(self.base_frame, orient="vertical", command=self.button_canvas.yview)
        self.vsb.grid(row=1, column=6, sticky="ns")
        self.button_canvas.configure(yscrollcommand=self.vsb.set)

        # اتصال رویداد اسکرول با ماوس به متد جدید
        self.button_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # ایجاد دکمه‌ها
        self.create_base_buttons()
        self.create_scientific_buttons()

        # افزودن کدهای C++ و Python به صفحات مربوطه
        self.add_cpp_code()
        self.add_python_code()

        # ایجاد دکمه تغییر حالت تاریک
        self.dark_mode = False
        self.create_dark_mode_button()

    def create_base_buttons(self):
        button_texts = [
            "7", "8", "9", "/", "C",
            "4", "5", "6", "*", "(",
            "1", "2", "3", "-", ")",
            "0", ".", "=", "+", "sin",
            "cos", "tan", "cot", "log",
            "exp", "sqrt", "x", "y", "z",
            "Exit", "حل معادله", "رسم نمودار",
            "مشتق", "انتگرال", "ماتریس", "حل معادله ماتریسی",
            "دانلود داده"
        ]

        row_val = 0
        col_val = 0
        for text in button_texts:
            button = tk.Button(self.button_frame, text=text, padx=50, pady=50, font=("Arial", 20), bg="white", fg="black",  # پس‌زمینه دکمه‌ها سفید
                               command=lambda txt=text: self.button_click(txt))
            button.grid(row=row_val, column=col_val, sticky="nsew", padx=10, pady=10)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # تنظیم وزن ستون‌ها و ردیف‌ها برای پر کردن فضا
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(row_val + 1):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def create_scientific_buttons(self):
        scientific_buttons = [
            "log2", "log10", "pow", "mod",
            "سین", "آزمایش", "دلخواه1", "دلخواه2", "دلخواه3"
        ]

        row_val = 0
        col_val = 0
        for text in scientific_buttons:
            button = tk.Button(self.scientific_frame, text=text, padx=50, pady=50, font=("Arial", 20), bg="white", fg="black",  # پس‌زمینه دکمه‌ها سفید
                               command=lambda txt=text: self.button_click(txt))
            button.grid(row=row_val, column=col_val, sticky="nsew", padx=10, pady=10)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # تنظیم وزن ستون‌ها و ردیف‌ها برای پر کردن فضا
        for i in range(5):
            self.scientific_frame.grid_columnconfigure(i, weight=1)
        for i in range(row_val + 1):
            self.scientific_frame.grid_rowconfigure(i, weight=1)

    def add_cpp_code(self):
        cpp_code = """
#include <iostream>
#include <cmath>
using namespace std;

double evaluate_expression(string expression) {
    // کد محاسبه معادله
}

int main() {
    string equation;
    cout << "معادله خود را وارد کنید: ";
    getline(cin, equation);
    cout << "نتیجه: " << evaluate_expression(equation) << endl;
    return 0;
}
"""
        cpp_display = tk.Text(self.cpp_frame, height=20, width=90, font=("Courier", 12), bg="white", fg="black")  # پس‌زمینه نمایشگر کد سفید
        cpp_display.insert(tk.END, cpp_code)
        cpp_display.config(state=tk.DISABLED)
        cpp_display.pack(padx=10, pady=10)

    def add_python_code(self):
        python_code = """
import sympy as sp

def evaluate_expression(expression):
    x = sp.symbols('x')
    return sp.sympify(expression).evalf()

equation = input("معادله خود را وارد کنید: ")
result = evaluate_expression(equation)
print(f"نتیجه: {result}")
"""
        python_display = tk.Text(self.python_frame, height=20, width=90, font=("Courier", 12), bg="white", fg="black")  # پس‌زمینه نمایشگر کد سفید
        python_display.insert(tk.END, python_code)
        python_display.config(state=tk.DISABLED)
        python_display.pack(padx=10, pady=10)

    def create_dark_mode_button(self):
        dark_mode_button = tk.Button(self.base_frame, text="تغییر به حالت تاریک", command=self.toggle_dark_mode, bg="white", fg="black")  # پس‌زمینه دکمه سفید
        dark_mode_button.grid(row=0, column=5)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.configure(bg="black")
            self.display.configure(bg="black", fg="white")
            self.button_frame.configure(bg="black")
            self.vsb.configure(bg="black", troughcolor="gray", bd=2)  # تغییر رنگ اسکرول بار
        else:
            self.root.configure(bg="lightblue")
            self.display.configure(bg="white", fg="black")
            self.button_frame.configure(bg="lightblue")
            self.vsb.configure(bg="lightblue", troughcolor="gray", bd=2)

    def on_mouse_wheel(self, event):
        self.button_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def button_click(self, button_text):
        current_equation = self.display.get("1.0", tk.END).strip()

        if button_text == "=":
            self.evaluate_expression(current_equation)
        elif button_text == "C":
            self.display.delete("1.0", tk.END)
        elif button_text == "Exit":
            self.root.quit()
        elif button_text == "حل معادله":
            self.solve_equation()
        elif button_text == "رسم نمودار":
            self.plot_graph()
        elif button_text == "مشتق":
            self.differentiate_expression()
        elif button_text == "انتگرال":
            self.integrate_expression()
        elif button_text == "ماتریس":
            self.enter_matrix()
        elif button_text == "حل معادله ماتریسی":
            self.solve_matrix_equation()
        elif button_text == "دانلود داده":
            self.download_data()
        else:
            if button_text in ["sin", "cos", "tan", "cot", "log", "exp", "sqrt"]:
                button_text += "("
            self.display.insert(tk.END, button_text)

    def evaluate_expression(self, expression):
        try:
            result = str(sympify(expression))
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("خطا", f"معادله اشتباه است: {e}")
            self.display.delete("1.0", tk.END)

    def solve_equation(self):
        equation = self.display.get("1.0", tk.END).strip()
        try:
            x, y, z = symbols('x y z')
            solutions = solve(sympify(equation), (x, y, z))
            self.display_solutions(solutions)
        except Exception as e:
            messagebox.showerror("خطا", f"معادله اشتباه است یا متغیرهای x، y، z ندارد: {e}")
            self.display.delete("1.0", tk.END)

    def display_solutions(self, solutions):
        result_string = ""
        for var, sol in solutions.items():
            result_string += f"{var}: {sol}\n"
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, result_string)

    def differentiate_expression(self):
        equation = self.display.get("1.0", tk.END).strip()
        try:
            x = symbols('x')
            derivative = sympify(equation).diff(x)
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, f"مشتق: {derivative}")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در محاسبه مشتق: {e}")
            self.display.delete("1.0", tk.END)

    def integrate_expression(self):
        equation = self.display.get("1.0", tk.END).strip()
        try:
            x = symbols('x')
            integral = sympify(equation).integrate(x)
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, f"انتگرال: {integral}")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در محاسبه انتگرال: {e}")
            self.display.delete("1.0", tk.END)

    def enter_matrix(self):
        # کد برای وارد کردن ماتریس و پردازش آن
        pass

    def solve_matrix_equation(self):
        # کد برای حل معادله ماتریسی
        pass

    def plot_graph(self):
        equation = self.display.get("1.0", tk.END).strip()
        try:
            x = np.linspace(-10, 10, 100)
            y = lambdify(symbols('x'), sympify(equation), modules='numpy')(x)
            plt.plot(x, y)
            plt.title('نمودار معادله')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()
            plt.show()
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در رسم نمودار: {e}")

    def download_data(self):
        # کد برای دانلود داده‌ها
        pass

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

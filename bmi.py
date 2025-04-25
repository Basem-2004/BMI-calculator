from settings import *
import customtkinter as ctk
try:
    import ctypes
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        
        # window setup
        super().__init__(fg_color= GREEN)
        self.title("")
        self.geometry(f"400x400+{int(self.winfo_screenwidth() / 2 - 400 / 2)}+{int(self.winfo_screenheight() / 2 - 400 / 2)}")
        self.resizable(False, False)
        self.iconbitmap("empty.ico")
        self.change_title_bar_color()
        
        # layout
        self.columnconfigure(0, weight= 1)
        self.rowconfigure((0, 1, 2, 3), weight= 1, uniform= "a")
        
        # data
        self.metric_bool = ctk.BooleanVar(value= True)
        self.weight_float = ctk.DoubleVar(value= 60)
        self.height_int = ctk.IntVar(value= 170)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()
        
        # tracing
        self.weight_float.trace("w", self.update_bmi)
        self.height_int.trace("w", self.update_bmi)
        self.metric_bool.trace("w", self.change_units)
        
        # widgets
        ResultText(self, self.bmi_string)
        self.weight_input = weightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)
        self.mainloop()
   
    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()
    
    def update_bmi(self, *args):
        weight_kg = self.weight_float.get()
        height_meter = self.height_int.get() / 100
        
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)
             
    def change_title_bar_color(self):
        try:   
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_CAPTION_COLOR = 35
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(TITLE_HEX_COLOR)),
                ctypes.sizeof(ctypes.c_int)
            ) 
        except:
            pass   

class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family= FONT, size= MAIN_TEXT_SIZE, weight= "bold")
        super().__init__(master= parent, text_color= WHITE, text= "22.5", font= font,
                         textvariable = bmi_string)
        self.grid(column = 0, row= 0, rowspan = 2, sticky = "nsew")
        
class weightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master= parent, fg_color= WHITE)
        self.grid(column= 0, row= 2, sticky= "nsew", padx = 10, pady= 10)
        
        
        self.metric_bool = metric_bool
        
        # output logic
        self.weight_float = weight_float
        self.weight_text = ctk.StringVar(value= f"{self.weight_float.get()}kg")
        
        # layout
        self.rowconfigure(0, weight= 1, uniform= "b")
        self.columnconfigure(0, weight= 2, uniform= "b")
        self.columnconfigure(1, weight= 1, uniform= "b")
        self.columnconfigure(2, weight= 3, uniform= "b")
        self.columnconfigure(3, weight= 1, uniform= "b")
        self.columnconfigure(4, weight= 2, uniform= "b")
        
        # widgets
        widgets_font = ctk.CTkFont(family= FONT, size= INPUT_FONT_SIZE)
        minus_btn_s = ctk.CTkButton(self, text= "-", fg_color= LIGHT_GRAY, text_color= BLACK, font= widgets_font, hover_color= GRAY, corner_radius= BUTTON_CORNER_RADIUS,
                                    command= lambda: self.update_weight(("minus", "small")))
        minus_btn_l = ctk.CTkButton(self, text= "-", fg_color= LIGHT_GRAY, text_color= BLACK, font= widgets_font, hover_color= GRAY, corner_radius= BUTTON_CORNER_RADIUS,
                                    command= lambda: self.update_weight(("minus", "large")))
        label = ctk.CTkLabel(self, text= "50kg", font= widgets_font, text_color= BLACK, 
                             textvariable = self.weight_text)
        plus_btn_s = ctk.CTkButton(self, text= "+", fg_color= LIGHT_GRAY, text_color= BLACK, font= widgets_font, hover_color= GRAY, corner_radius= BUTTON_CORNER_RADIUS,
                                    command= lambda: self.update_weight(("plus", "small")))
        plus_btn_l = ctk.CTkButton(self, text= "+", fg_color= LIGHT_GRAY, text_color= BLACK, font= widgets_font, hover_color= GRAY, corner_radius= BUTTON_CORNER_RADIUS,
                                    command= lambda: self.update_weight(("plus", "large")))
        
        minus_btn_s.grid(column= 1, row= 0, padx = 4, pady= 4)
        minus_btn_l.grid(column= 0, row= 0, sticky= "ns", padx = 8, pady= 8)
        label.grid(column= 2, row= 0)
        plus_btn_s.grid(column= 3, row= 0, padx = 4, pady= 4)
        plus_btn_l.grid(column= 4, row= 0, sticky= "ns", padx = 8, pady= 8)
    
    def update_weight(self, info = None):
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == "large" else 0.1
            else:
                amount = 0.453592 if info[1] == "large" else 0.453592 / 16
            
            if info[0] == "plus":
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        
        if self.metric_bool.get():
            self.weight_text.set(f"{round(self.weight_float.get(), 1)}kg")
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.weight_text.set(f"{int(pounds)}lb {int(ounces)}oz")
                            
class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master= parent, fg_color= WHITE)
        self.grid(column= 0, row= 3, sticky= "nsew", padx = 10, pady= 10)
        
        self.metric_bool = metric_bool
        
        # output logic
        self.height_string = ctk.StringVar()
        self.update_text(height_int.get())
        
        # widgets
        font = ctk.CTkFont(family= FONT, size= INPUT_FONT_SIZE)
        slider = ctk.CTkSlider(self, fg_color= LIGHT_GRAY, button_color= GREEN, button_hover_color= GRAY, progress_color= GREEN,
                               variable= height_int, from_= 100, to= 250, command= self.update_text)
        label = ctk.CTkLabel(self, text= "1.2m", font= font, text_color= BLACK,
                             textvariable = self.height_string)
        
        # layout
        slider.pack(side = "left", expand = True, fill = "x", padx = 10, pady = 10)
        label.pack(side = "left", padx = 20)
    
    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(round(amount / 100, 2))
            self.height_string.set(f"{text_string}m")
        else: #imperial
            feet, inches = divmod(amount / 2.54, 12)
            self.height_string.set(f"{int(feet)}\'{int(inches)}\"")
                   
class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        font = ctk.CTkFont(family= FONT, size= SWITCH_FONT_SIZE, weight= "bold")
        super().__init__(master= parent, text= "metric", font= font, text_color= DARK_GREEN)
        self.place(relx = 0.98, rely = 0.01, anchor = "ne")
        
        self.metric_bool = metric_bool
        
        self.bind("<Button>", self.change_units)
        
    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())
        
        if self.metric_bool.get():
            self.configure(text = "metric")
        else:
            self.configure(text = "imperial")
            
        
if __name__ == "__main__":
    App()    

class SmartCalc(App):
    def build(self):
        self.expression = ""
        self.is_degree = True

        root = GridLayout(cols=1, padding=15, spacing=12)

        # DISPLAY (clean Samsung-style)
        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=48,
            background_color=(0.05,0.05,0.05,1),
            foreground_color=(1,1,1,1),
            size_hint=(1, 0.25)
        )
        root.add_widget(self.display)

        # MODE BUTTON (DEG/RAD)
        self.mode_btn = Button(
            text="DEG",
            size_hint=(1, 0.08),
            background_color=(0.2,0.6,1,1),
            color=(1,1,1,1)
        )
        self.mode_btn.bind(on_press=self.toggle_mode)
        root.add_widget(self.mode_btn)

        # BUTTON STYLE FUNCTION (Samsung feel)
        def make_btn(text, bg):
            return Button(
                text=text,
                font_size=24,
                background_normal="",
                background_color=bg,
                color=(1,1,1,1)
            )

        # BUTTONS (clean grid like phone calculator)
        buttons = [
            ["MC","MR","M+","M-","C"],
            ["7","8","9","/","sin"],
            ["4","5","6","*","cos"],
            ["1","2","3","-","tan"],
            ["0",".","π","+","√"],
            ["x²","log","⌫","(",")"],
            ["="]
        ]

        for row in buttons:
            row_layout = GridLayout(cols=len(row), spacing=6)

            for b in row:
                # COLOR SYSTEM (Samsung style)
                if b in ["+","-","*","/","="]:
                    btn = make_btn(b, (1, 0.6, 0.1, 1))   # orange operators
                elif b in ["C","⌫","MC","MR","M+","M-"]:
                    btn = make_btn(b, (0.35, 0.35, 0.35, 1))  # gray controls
                else:
                    btn = make_btn(b, (0.12, 0.12, 0.12, 1))  # dark keys

                btn.bind(on_press=self.on_press)
                row_layout.add_widget(btn)

            root.add_widget(row_layout)

        return root

    # MODE SWITCH
    def toggle_mode(self, instance):
        self.is_degree = not self.is_degree
        self.mode_btn.text = "DEG" if self.is_degree else "RAD"

    def on_press(self, instance):
        t = instance.text

        if t == "C":
            self.expression = ""

        elif t == "⌫":
            self.expression = self.expression[:-1]

        elif t == "=":
            self.calculate()
            return

        elif t == "π":
            self.expression += str(math.pi)

        elif t == "√":
            self.expression += "math.sqrt("

        elif t == "x²":
            self.expression += "**2"

        elif t == "sin":
            self.expression += "self.sin_fix("

        elif t == "cos":
            self.expression += "self.cos_fix("

        elif t == "tan":
            self.expression += "self.tan_fix("

        else:
            self.expression += t

        self.display.text = self.expression

    def sin_fix(self, x):
        if self.is_degree:
            x = math.radians(x)
        return math.sin(x)

    def cos_fix(self, x):
        if self.is_degree:
            x = math.radians(x)
        return math.cos(x)

    def tan_fix(self, x):
        if self.is_degree:
            x = math.radians(x)
        return math.tan(x)

    def calculate(self):
        try:
            result = eval(
                self.expression,
                {"__builtins__": None},
                {"math": math, "self": self}
            )
            self.display.text = str(result)
            self.expression = str(result)
        except:
            self.display.text = "Error"
            self.expression = ""

SmartCalc().run()

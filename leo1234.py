import tkinter as tk

# =========================
# AI ENGINE
# =========================
class ClimateAI:
    def __init__(self):
        self.w = {
            "co2": 0.6,
            "temp": 0.5,
            "pollution": 0.7,
            "energy": 0.6,
            "gdp": -0.4
        }

        self.actions = ["Renewable", "Reforestation", "Regulation", "GreenTech"]

    # ---------- SCORING ----------
    def score(self, co2, temp, pollution, energy, gdp, action):
        base = (
            co2*self.w["co2"] +
            temp*self.w["temp"] +
            pollution*self.w["pollution"] +
            energy*self.w["energy"] +
            gdp*self.w["gdp"]
        )

        if action == "Renewable":
            base *= 0.92
        elif action == "Reforestation":
            base *= 0.90
        elif action == "Regulation":
            base *= 0.88
        elif action == "GreenTech":
            base *= 0.89

        return base

    # ---------- DECISION ----------
    def decide(self, inputs):
        results = {}
        for a in self.actions:
            results[a] = self.score(*inputs, a)

        best = min(results, key=results.get)
        return best, results

    # ---------- LEARNING ----------
    def learn(self):
        # small adaptive improvement
        self.w["co2"] *= 0.999
        self.w["pollution"] *= 0.999
        self.w["energy"] *= 1.001

    # ---------- SIMULATION ----------
    def simulate(self, inputs, action):
        co2, temp, pollution, energy, gdp = inputs
        trend = []

        for _ in range(10):
            val = self.score(co2, temp, pollution, energy, gdp, action)
            trend.append(val)

            co2 *= 0.97
            pollution *= 0.96
            temp *= 0.995

        return trend

    # ---------- EXPLANATION ----------
    def explain(self, best):
        return f"{best} selected because it minimizes environmental impact under current conditions."


# =========================
# UI APP
# =========================
class App:
    def __init__(self, root):
        self.ai = ClimateAI()

        root.title("🌍 Climate Mission AI FINAL")
        root.geometry("1100x650")
        root.configure(bg="#0f172a")

        # ================= LEFT PANEL =================
        self.left = tk.Frame(root, bg="#1e293b", width=320)
        self.left.pack(side="left", fill="y")

        tk.Label(self.left, text="CLIMATE INPUTS",
                 bg="#1e293b", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)

        self.sliders = {}
        labels = ["CO2", "Temp", "Pollution", "Energy", "GDP"]

        for l in labels:
            tk.Label(self.left, text=l, bg="#1e293b", fg="white").pack()

            s = tk.Scale(self.left, from_=0, to=1000,
                         orient="horizontal", bg="#1e293b",
                         fg="white")
            s.pack()
            self.sliders[l] = s

        # -------- Presets (Upgrade #2) --------
        tk.Button(self.left, text="🇪🇹 Ethiopia Mode",
                  command=self.ethiopia).pack(pady=5)

        tk.Button(self.left, text="🌍 Global Mode",
                  command=self.global_mode).pack(pady=5)

        tk.Button(self.left, text="🏭 Industrial Mode",
                  command=self.industrial).pack(pady=5)

        # Run button
        tk.Button(self.left, text="RUN AI",
                  command=self.run,
                  bg="#22c55e", fg="white").pack(pady=10)

        self.result = tk.Label(self.left, text="",
                               bg="#1e293b", fg="#22c55e")
        self.result.pack()

        self.explain = tk.Label(self.left, text="",
                                bg="#1e293b", fg="white",
                                wraplength=280)
        self.explain.pack()

        # ================= RIGHT CANVAS =================
        self.canvas = tk.Canvas(root, bg="#0f172a")
        self.canvas.pack(side="right", fill="both", expand=True)

    # ================= PRESETS =================
    def ethiopia(self):
        self.set_values(400, 25, 200, 300, 150)

    def global_mode(self):
        self.set_values(500, 30, 300, 500, 400)

    def industrial(self):
        self.set_values(800, 35, 700, 900, 600)

    def set_values(self, co2, temp, pol, energy, gdp):
        vals = [co2, temp, pol, energy, gdp]
        for i, k in enumerate(self.sliders):
            self.sliders[k].set(vals[i])

    # ================= RUN =================
    def run(self):
        vals = [self.sliders[k].get() for k in self.sliders]

        best, results = self.ai.decide(vals)
        self.ai.learn()

        self.canvas.delete("all")

        self.draw_bars(results, best)
        self.draw_line(self.ai.simulate(vals, best))

        self.result.config(text=f"Best: {best}")
        self.explain.config(text=self.ai.explain(best))

    # ================= BAR GRAPH =================
    def draw_bars(self, results, best):
        x = 50
        base = 550
        w = 70

        m = max(results.values()) or 1

        for a, v in results.items():
            h = (v/m)*250

            color = "#22c55e" if a == best else "#475569"

            self.canvas.create_rectangle(x, base-h, x+w, base, fill=color)
            self.canvas.create_text(x+35, base+15, text=a, fill="white")

            x += 100

    # ================= LINE GRAPH =================
    def draw_line(self, data):
        x0, y0 = 400, 120
        w, h = 600, 300

        mn, mx = min(data), max(data)
        if mx == mn:
            mx += 1

        prev = None

        for i, v in enumerate(data):
            x = x0 + (i/len(data))*w
            y = y0 + h - ((v-mn)/(mx-mn))*h

            if prev:
                self.canvas.create_line(prev[0], prev[1], x, y,
                                        fill="#22c55e", width=2)
            prev = (x, y)

        self.canvas.create_text(700, 80,
                                text="10-Year Future Simulation",
                                fill="white")


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
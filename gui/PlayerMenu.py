import tkinter as tk
from tkinter import ttk
from data.constante import colors

def get_players_from_menu():
    players = []

    def on_create():

        nonlocal players
        players = []

        from core.Player import Player
        from core.AiPlayer import AiPlayer

        for p in entries:
            name = p["name"].get() or "Player"
            primary = p["primary"].get() or colors[0]
            secondary = p["secondary"].get() or (colors[1] if len(colors) > 1 else colors[0])
            p_type = p["type"].get()

            if p_type == "AI":
                player = AiPlayer()
            else:
                player = Player(name, primary, secondary, False)

            players.append(player)

        root.destroy()

    root = tk.Tk()
    root.title("Player Setup")
    entries = []

    for i in range(4):
        frame = ttk.LabelFrame(root, text=f"Player {i+1}")
        frame.pack(padx=10, pady=5, fill="x")

        tk.Label(frame, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=0, column=1)


        tk.Label(frame, text="Primary Color:").grid(row=1, column=0)
        primary_color = ttk.Combobox(frame, values=colors, state="readonly")
        primary_color.current(0)
        primary_color.grid(row=1, column=1)

        tk.Label(frame, text="Secondary Color:").grid(row=2, column=0)
        secondary_color = ttk.Combobox(frame, values=colors, state="readonly")
        secondary_color.current(1 if len(colors) > 1 else 0)
        secondary_color.grid(row=2, column=1)

        type_var = tk.StringVar(value="Player")
        ttk.Radiobutton(frame, text="Human", variable=type_var, value="Player").grid(row=3, column=0)
        ttk.Radiobutton(frame, text="AI", variable=type_var, value="AI").grid(row=3, column=1)

        entries.append({
            "name": name_entry,
            "primary": primary_color,
            "secondary": secondary_color,
            "type": type_var
        })
    tk.Button(root, text="Create Players", command=on_create).pack(pady=10)

    root.mainloop()

    return players

if __name__ == "__main__":
    game_players = get_players_from_menu()
    print("Players returned from menu:", [getattr(p, 'playerName', str(p)) for p in game_players])

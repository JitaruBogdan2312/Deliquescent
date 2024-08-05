import random
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk


class Trait:
    def __init__(self, name, description, modifier):
        self.name = name
        self.description = description
        self.modifier = modifier  # Modifier is a dictionary with check type as key and value as the bonus


class Check:
    def __init__(self, check_type, difficulty, modifier):
        self.check_type = check_type
        self.difficulty = difficulty
        self.modifier = modifier


class PlayerStats:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.psyche_current = 5
        self.psyche_max = 5
        self.health_current = 5
        self.health_max = 5
        self.aura_current = 5
        self.aura_max = 5
        self.magic_unlocked = False
        self.magic_current = 0
        self.magic_max = 0
        self.traits = [
            Trait("To Be a Hero...", "+1 Modifier to all checks when actively attempting to save someone!", {"all": 1}),
            Trait("Silver Eyes...", "???/More to be added later!", {}),
            Trait("Not Weird! Just...Quirky!", "+3 to all Engineering Checks, -1 to all Social Checks!",
                  {"Engineering Check": 3, "Social Check": -1})
        ]
        self.skills = {}  # Dictionary to hold trained skills and their levels
        self.inventory = []
        self.equipment = {
            "Primary Weapon": None,
            "Side Arm": None,
            "Outfit": None,
            "Accessories": []
        }
        self.death_door_check = 15
        self.san_break_count = 0

        # Equip starting items
        self.add_to_inventory(
            "One Cloak, dear to the heart… [+1 to all Psyche Checks Whilst Wearing this!] [Accessory!]")
        self.equip_item("One Cloak, dear to the heart… [+1 to all Psyche Checks Whilst Wearing this!] [Accessory!]")
        self.add_to_inventory("Crescent Rose [Can Be equipped as a primary weapon!] [+3 to all Combat Checks!]")
        self.equip_item("Crescent Rose [Can Be equipped as a primary weapon!] [+3 to all Combat Checks!]")

    def display_text(self, text, color=None, tag=None):
        if color:
            self.text_widget.insert(tk.END, text + '\n', color)
        elif tag:
            self.text_widget.insert(tk.END, text + '\n', tag)
        else:
            self.text_widget.insert(tk.END, text + '\n', 'white')
        self.text_widget.tag_add("center", "end-2l linestart", "end-1c lineend")
        self.text_widget.see(tk.END)

    def display_stats(self):
        self.display_text(f"Psyche: {self.psyche_current}/{self.psyche_max}", 'purple')
        self.display_text(f"Health: {self.health_current}/{self.health_max}", 'red')
        self.display_text(f"Aura: {self.aura_current}/{self.aura_max}", 'blue')
        if self.magic_unlocked:
            self.display_text(f"Magic: {self.magic_current}/{self.magic_max}", 'cream')
        else:
            self.display_text(f"Magic: Not Unlocked", 'cream')

    def display_traits(self):
        self.display_text("That Which Defines Us...", 'gold')
        for trait in self.traits:
            self.display_text(f"- {trait.name}: {trait.description}", 'gold')

    def display_skills(self):
        self.display_text("Skills Picked up on a Perilous Journey", 'green')
        for skill, level in self.skills.items():
            self.display_text(f"- {skill}: Level {level}", 'green')

    def display_inventory(self):
        self.display_text("Inventory", 'orange')
        for item in self.inventory:
            self.display_text(f"- {item}", 'orange')

    def display_equipment(self):
        self.display_text("Equipment", 'orange')
        self.display_text(f"Primary Weapon: {self.equipment['Primary Weapon']}", 'orange')
        self.display_text(f"Side Arm: {self.equipment['Side Arm']}", 'orange')
        self.display_text(f"Outfit: {self.equipment['Outfit']}", 'orange')
        self.display_text("Accessories:", 'orange')
        for accessory in self.equipment["Accessories"]:
            self.display_text(f"- {accessory}", 'orange')

    def unlock_magic(self):
        self.magic_unlocked = True
        self.magic_current = 5  # Set initial magic current value when unlocked
        self.magic_max = 5  # Set initial magic max value when unlocked

    def add_trait(self, trait):
        self.traits.append(trait)

    def train_skill(self, skill, level):
        self.skills[skill] = level

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def equip_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        if "Primary Weapon" in item:
            if self.equipment["Primary Weapon"]:
                self.inventory.append(self.equipment["Primary Weapon"])
            self.equipment["Primary Weapon"] = item
        elif "Side Arm" in item:
            if self.equipment["Side Arm"]:
                self.inventory.append(self.equipment["Side Arm"])
            self.equipment["Side Arm"] = item
        elif "Outfit" in item:
            if self.equipment["Outfit"]:
                self.inventory.append(self.equipment["Outfit"])
            self.equipment["Outfit"] = item
        elif "Accessory" in item and len(self.equipment["Accessories"]) < 4:
            self.equipment["Accessories"].append(item)
        else:
            self.display_text(f"Cannot equip {item}.", 'red')
            return

        self.display_text(f"Equipped {item}.", 'green')
        self.update_stats()

    def unequip_item(self, slot, item):
        if slot == "Accessories":
            self.equipment[slot].remove(item)
        else:
            self.equipment[slot] = None
        self.inventory.append(item)
        self.display_text(f"Unequipped {item}.", 'green')
        self.update_stats()

    def roll_dice(self):
        return [random.randint(1, 20) for _ in range(3)]

    def perform_check(self, check):
        rolls = self.roll_dice()
        self.display_text(f"Dice rolls: {rolls}")

        # Check for special outcomes
        total = sum(rolls)
        unique_rolls = set(rolls)
        result = "Regular Roll"
        result_color = 'white'

        if total == 21:
            result = "BlackJack! Critical Success."
            result_color = 'gold'
        elif total == 12:
            result = "WhiteJack! Critical Failure."
            result_color = 'dark red'
        elif len(unique_rolls) == 1:
            if rolls[0] == 7:
                result = "Jackpot! Critical Success and Greater Critical Success."
                result_color = 'gold'
                self.apply_jackpot()
            elif rolls[0] == 4:
                result = "Whiteout! Critical Failure and severe penalties."
                result_color = 'gray'
                self.apply_whiteout()
            else:
                result = "Triples! Greater Critical Success."
                result_color = 'gold'
        else:
            highest_roll = max(rolls) + check.modifier + self.calculate_equipment_bonus(check.check_type)
            if highest_roll >= check.difficulty:
                result = "Pass"
                result_color = 'white'
            else:
                result = "Fail"
                result_color = 'red'

        return rolls, result, result_color

    def calculate_equipment_bonus(self, check_type):
        bonus = 0
        if self.equipment["Primary Weapon"] and "Combat" in check_type:
            bonus += 3
        for accessory in self.equipment["Accessories"]:
            if "Psyche" in check_type:
                bonus += 1
        return bonus

    def apply_jackpot(self):
        # Placeholder method to apply a random Jackpot trait
        self.display_text("Applying a random Jackpot trait...", 'gold')
        # Implement the logic to apply a random Jackpot trait

    def apply_whiteout(self):
        # Placeholder method to apply a random Whiteout trait and reduce stats
        self.display_text("Applying a random Whiteout trait and reducing stats...", 'gray')
        self.health_current = 1
        self.psyche_current = 1
        self.aura_current = 1
        self.magic_current = 1 if self.magic_unlocked else 0
        # Implement the logic to apply a random Whiteout trait

    def combat_clash(self, enemy_roll, enemy_damage):
        # Ruby rolls
        ruby_rolls = self.roll_dice()
        ruby_highest_roll = max(ruby_rolls) + 3  # Assuming a +3 combat check modifier
        self.display_text(f"Ruby's dice rolls: {ruby_rolls} (Highest Roll + Modifier: {ruby_highest_roll})", 'white')

        # Determine the outcome
        if ruby_highest_roll >= enemy_roll:
            damage_dealt = max(3, ruby_highest_roll - enemy_roll)
            self.display_text(f"Ruby wins the clash and deals {damage_dealt} damage!", 'gold')
            return damage_dealt, 0
        else:
            self.display_text(f"Enemy wins the clash and deals {enemy_damage} damage!", 'red')
            return 0, enemy_damage

    def receive_damage(self, damage):
        if self.aura_current > 0:
            if damage <= self.aura_current:
                self.aura_current -= damage
                damage = 0
            else:
                damage -= self.aura_current
                self.aura_current = 0

        self.health_current -= damage
        if self.health_current < 1:
            self.health_current = 1
            self.enter_deaths_door()

    def enter_deaths_door(self):
        self.display_text("Ruby has entered Death's Door!", 'dark red')
        self.root.configure(bg='dark red')
        self.deaths_door_check()

    def deaths_door_check(self):
        check = Check("Death's Door", self.death_door_check, 0)
        if not self.perform_check(check):
            self.display_text("Ruby failed the Death's Door check and dies...", 'dark red')
            self.health_current = 0
        else:
            self.display_text("Ruby succeeded the Death's Door check!", 'white')
            self.death_door_check += 3

    def san_break(self):
        self.san_break_count += 1
        self.display_text("Ruby has entered San Break!", 'dark purple')
        self.root.configure(bg='dark purple')
        self.psyche_current = 3
        self.add_negative_traits(self.san_break_count)

    def add_negative_traits(self, count):
        for _ in range(count):
            # Placeholder logic for adding a random negative trait
            self.display_text(f"Added a negative trait to Ruby.", 'gold')
            # Add the actual logic for adding negative traits here

    def update_stats(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', tk.END)
        self.display_character_sheet()
        self.text_widget.configure(state='disabled')

    def display_character_sheet(self):
        self.display_text("\nRuby Rose\n", 'cyan')  # Updated color
        self.display_text("---------------------------------", 'red')
        self.display_stats()
        self.display_text("---------------------------------", 'red')
        self.display_traits()
        self.display_text("---------------------------------", 'red')
        self.display_inventory()
        self.display_text("---------------------------------", 'red')
        self.display_equipment()
        self.display_text("---------------------------------", 'red')
        self.display_skills()
        self.display_text("\n", 'white')
        self.text_widget.see(tk.END)

    def equip_item_from_inventory(self, item):
        self.equip_item(item)
        self.update_stats()

    def unequip_item_from_slot(self, slot, item):
        self.unequip_item(slot, item)
        self.update_stats()


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deliquescent")
        self.root.configure(bg='black')
        self.root.geometry("1024x768")  # Set the window size
        self.root.attributes('-fullscreen', True)  # Set full screen

        # Create main screen frame
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill='both', expand=True)

        # Load and display the background image
        self.background_image = Image.open(r"C:\Users\spach\Desktop\Concept Art\Deli_Cover.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.main_frame, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Create buttons on the main screen
        self.play_button = tk.Button(self.main_frame, text="Play Deliquescent-Text-Only", command=self.start_game,
                                     bg='blue', fg='white', font=("Helvetica", 20))
        self.play_button.place(relx=0.5, rely=0.4, anchor='center')

        self.options_button = tk.Button(self.main_frame, text="Options", bg='blue', fg='white', font=("Helvetica", 20))
        self.options_button.place(relx=0.5, rely=0.5, anchor='center')

        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.root.quit, bg='blue', fg='white',
                                     font=("Helvetica", 20))
        self.quit_button.place(relx=0.5, rely=0.6, anchor='center')

        # Create tabs
        self.notebook = ttk.Notebook(root)

        # Welcome tab
        self.welcome_frame = tk.Frame(self.notebook, bg='black')
        self.notebook.add(self.welcome_frame, text='Welcome')
        self.display_welcome_message()

        # Character tab
        self.character_frame = tk.Frame(self.notebook, bg='black')
        self.notebook.add(self.character_frame, text='Character')
        self.character_text = scrolledtext.ScrolledText(self.character_frame, wrap=tk.WORD, width=60, height=20,
                                                        font=("Helvetica", 12), bg='black', fg='white')
        self.character_text.pack()
        self.character_text.tag_config('purple', foreground='#800080')
        self.character_text.tag_config('red', foreground='#FF0000')
        self.character_text.tag_config('blue', foreground='#0000FF')
        self.character_text.tag_config('cream', foreground='#FFFDD0')
        self.character_text.tag_config('white', foreground='#FFFFFF')
        self.character_text.tag_config('gold', foreground='#FFD700')
        self.character_text.tag_config('orange', foreground='#FFA500')
        self.character_text.tag_config('green', foreground='#00FF00')
        self.character_text.tag_config('italic', font=("Helvetica", 12, "italic"))
        self.character_text.tag_config('teal', foreground='#008080', font=("Helvetica", 10, "italic"))
        self.character_text.tag_configure("center", justify='center')

        self.player_stats = PlayerStats(self.character_text)
        self.player_stats.root = self.root
        self.display_character_sheet()

        # Listbox for inventory
        self.inventory_listbox = tk.Listbox(self.character_frame, selectmode=tk.SINGLE, font=("Helvetica", 12),
                                            bg='black', fg='orange', width=60, height=10)
        self.inventory_listbox.pack(pady=10)
        self.update_inventory_listbox()

        # Equip and unequip buttons
        self.equip_buttons_frame = tk.Frame(self.character_frame, bg='black')
        self.equip_buttons_frame.pack(pady=10)

        self.equip_inventory_button = tk.Button(self.equip_buttons_frame, text="Equip Selected Item",
                                                command=self.equip_selected_item, bg='blue', fg='white',
                                                font=("Helvetica", 12))
        self.equip_inventory_button.pack(side=tk.LEFT, padx=5)

        self.unequip_item_buttons = {
            "Primary Weapon": tk.Button(self.equip_buttons_frame, text="Unequip Primary Weapon",
                                        command=lambda: self.unequip_item("Primary Weapon"), bg='blue', fg='white',
                                        font=("Helvetica", 12)),
            "Side Arm": tk.Button(self.equip_buttons_frame, text="Unequip Side Arm",
                                  command=lambda: self.unequip_item("Side Arm"), bg='blue', fg='white',
                                  font=("Helvetica", 12)),
            "Outfit": tk.Button(self.equip_buttons_frame, text="Unequip Outfit",
                                command=lambda: self.unequip_item("Outfit"), bg='blue', fg='white',
                                font=("Helvetica", 12)),
            "Accessories": tk.Button(self.equip_buttons_frame, text="Unequip Accessory", command=self.unequip_accessory,
                                     bg='blue', fg='white', font=("Helvetica", 12))
        }

        for slot, button in self.unequip_item_buttons.items():
            button.pack(side=tk.LEFT, padx=5)

        # Play tab
        self.play_frame = tk.Frame(self.notebook, bg='black')
        self.notebook.add(self.play_frame, text='Play')

        self.play_text = scrolledtext.ScrolledText(self.play_frame, wrap=tk.WORD, width=80, height=20,
                                                   font=("Helvetica", 12), bg='black', fg='white')
        self.play_text.pack()
        self.play_text.tag_config('purple', foreground='#800080')
        self.play_text.tag_config('red', foreground='#FF0000')
        self.play_text.tag_config('blue', foreground='#0000FF')
        self.play_text.tag_config('cream', foreground='#FFFDD0')
        self.play_text.tag_config('white', foreground='#FFFFFF')
        self.play_text.tag_config('gold', foreground='#FFD700')
        self.play_text.tag_config('orange', foreground='#FFA500')
        self.play_text.tag_config('green', foreground='#00FF00')
        self.play_text.tag_config('magenta', foreground='#FF00FF')
        self.play_text.tag_config('italic', font=("Helvetica", 12, "italic"))
        self.play_text.tag_config('teal', foreground='#008080', font=("Helvetica", 10, "italic"))
        self.play_text.tag_configure("center", justify='center')

        self.check_label = tk.Label(self.play_frame, text="", bg='black', fg='white', font=("Helvetica", 12))
        self.check_label.pack(pady=10)

        self.roll_button = tk.Button(self.play_frame, text="Roll Dice", command=self.show_dice_roll, bg='blue',
                                     fg='white', font=("Helvetica", 12))
        self.roll_button.pack(pady=10)
        self.roll_button.config(state=tk.DISABLED)

        self.result_text = tk.Label(self.play_frame, text="", bg='black', font=("Helvetica", 16))
        self.result_text.pack(pady=20)

        # Choice buttons arranged horizontally
        self.choice_frame = tk.Frame(self.play_frame, bg='black')
        self.choice_frame.pack(pady=10)

        self.choice_buttons = {
            "purple": tk.Button(self.choice_frame, text="Psyche Choice", bg='purple', fg='white',
                                font=("Helvetica", 12), command=lambda: self.handle_choice("purple")),
            "red": tk.Button(self.choice_frame, text="Health Choice", bg='red', fg='white', font=("Helvetica", 12),
                             command=lambda: self.handle_choice("red")),
            "blue": tk.Button(self.choice_frame, text="Aura Choice", bg='blue', fg='white', font=("Helvetica", 12),
                              command=lambda: self.handle_choice("blue")),
            "cream": tk.Button(self.choice_frame, text="Magic Choice", bg='#FFFDD0', fg='black', font=("Helvetica", 12),
                               command=lambda: self.handle_choice("cream")),
            "white": tk.Button(self.choice_frame, text="Neutral Choice", bg='white', fg='black', font=("Helvetica", 12),
                               command=lambda: self.handle_choice("white"))
        }

        for button in self.choice_buttons.values():
            button.pack(side=tk.LEFT, padx=5)
            button.config(state=tk.DISABLED)

        self.current_step = 0
        self.play_initialized = False
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def start_game(self):
        self.main_frame.pack_forget()  # Hide the main frame
        self.notebook.pack(pady=10, expand=True)
        self.notebook.select(self.play_frame)  # Open the play tab

    def display_check(self, check):
        self.check_label.config(text=f"{check.check_type} Check: BO3 1d20+{check.modifier}")
        self.roll_button.config(state=tk.NORMAL)
        self.current_check = check
        self.display_narrator_blurb()

    def display_narrator_blurb(self):
        blurbs = [
            "Hello?\n- Kranith",
            "Maybe this is working?\n- Kranith"
        ]
        blurb = random.choice(blurbs)
        self.check_label.config(text=self.check_label.cget("text") + "\n" + blurb)
        self.check_label.config(font=("Helvetica", 10, "italic"), fg='teal')

    def display_choicebox(self):
        self.play_text.insert(tk.END, "\n---------------------------------\n", 'white')
        self.play_text.insert(tk.END, "\nA Crossroad Emerges…", 'gold')
        self.play_text.tag_add("center", "end-2l linestart", "end-1c lineend")
        self.play_text.insert(tk.END, "\n---------------------------------\n", 'white')

        choice_text = (
            "\n\"This I say to you, all of you, any of you, who lay hands onto this burden and seek to carry it.\n"
            "Eyes open will never close again.\n"
            "And just as you see, the light and darkness both…\n"
            "So does it see you.\n"
            "Leave what you love and cherish well-alone. Leave it behind you, for what you will bring upon them will be worse than any curse could be…\n"
            "There are enough pouches of gold buried in the filth and muck across this world to last you a life time. Enough favors. Enough oaths. All within these pages.\n"
            "They are yours now.\n"
            "Such is our duty. Our silent, lonely vigil.\""
        )
        self.play_text.insert(tk.END, choice_text, 'magenta')
        self.play_text.tag_add("center", "end-10l linestart", "end-1c lineend")
        self.play_text.insert(tk.END, "\n\"Abandon all hope, ye who enter!\"", 'italic lightblue')
        self.play_text.tag_add("center", "end-1l linestart", "end-1c lineend")
        self.play_text.insert(tk.END, "\n---------------------------------\n", 'white')

        # Adding choices under the text
        self.play_text.insert(tk.END, "\nLeave them well alone. You will only bring ruin upon them.", 'purple')
        self.play_text.tag_add("center", "end-3l linestart", "end-3l lineend")
        self.play_text.insert(tk.END,
                              "\nYou will handle anything that dares to touch that which you love. You don't know how. But you will.",
                              'red')
        self.play_text.tag_add("center", "end-2l linestart", "end-2l lineend")
        self.play_text.insert(tk.END, "\nPerhaps a balance can be struck? Neither gone, nor here, at once.", 'blue')
        self.play_text.tag_add("center", "end-1l linestart", "end-1c lineend")
        self.play_text.insert(tk.END, "\n---------------------------------\n", 'white')

        self.choice_buttons["purple"].config(state=tk.NORMAL)
        self.choice_buttons["red"].config(state=tk.NORMAL)
        self.choice_buttons["blue"].config(state=tk.NORMAL)
        if self.player_stats.magic_unlocked:
            self.choice_buttons["cream"].config(state=tk.NORMAL)
        self.choice_buttons["white"].config(state=tk.NORMAL)

    def handle_choice(self, choice):
        for button in self.choice_buttons.values():
            button.config(state=tk.DISABLED)
        self.play_text.insert(tk.END, "\n", 'white')  # Add an empty line
        if choice == "purple":
            self.play_text.insert(tk.END,
                                  "\n\nHello! You've stumbled onto a major divergence from the normal storyline! This will be implemented at a later time! Thank you for playing, and apologies for the inconvenience!",
                                  'white')
        elif choice == "red":
            self.play_text.insert(tk.END,
                                  "\nShe sniffled lightly and wiped her eyes as she remembered the child, and then, she stood up resolutely, donning her precious, precious cape onto her shoulders.",
                                  'white')
            self.play_text.insert(tk.END, "\nNow then, what was her course of action?", 'white')
            self.play_text.insert(tk.END,
                                  "\nHer father would be home by tomorrow morning at the earliest, and it was noon now. She had already processed what had happened, already found her resolution…so what was her next step?",
                                  'white')
        elif choice == "blue":
            self.play_text.insert(tk.END,
                                  "\n\nHello! You've stumbled onto a major divergence from the normal storyline! This will be implemented at a later time! Thank you for playing, and apologies for the inconvenience!",
                                  'white')
        elif choice == "cream":
            self.play_text.insert(tk.END, "\n[Magic Choice text goes here]", 'cream')
        elif choice == "white":
            self.play_text.insert(tk.END, "\n[Neutral Choice text goes here]", 'white')
        self.current_step += 1
        self.advance_story()

    def display_welcome_message(self):
        welcome_message = (
            "\n\n\nWelcome To Deliquescent Version 0.1!\n"
            "Input Character to display the Character Sheet!\n"
            "Input Play to start up the game!"
        )
        welcome_label = tk.Label(self.welcome_frame, text=welcome_message, bg='black', fg='white',
                                 font=("Helvetica", 12, "italic"), justify='center')
        welcome_label.pack(expand=True)

    def display_character_sheet(self):
        self.character_text.configure(state='normal')
        self.character_text.delete('1.0', tk.END)
        self.player_stats.display_character_sheet()
        self.character_text.configure(state='disabled')

    def update_inventory_listbox(self):
        self.inventory_listbox.delete(0, tk.END)
        for item in self.player_stats.inventory:
            self.inventory_listbox.insert(tk.END, item)

    def equip_selected_item(self):
        try:
            selected_index = self.inventory_listbox.curselection()[0]
            selected_text = self.inventory_listbox.get(selected_index)
            if selected_text in self.player_stats.inventory:
                self.player_stats.equip_item_from_inventory(selected_text)
                self.update_inventory_listbox()
            else:
                self.player_stats.display_text("Please select a valid item from the inventory.", 'red')
        except IndexError:
            self.player_stats.display_text("No item selected. Please select an item from the inventory.", 'red')

    def unequip_item(self, slot):
        item = self.player_stats.equipment[slot]
        if item:
            self.player_stats.unequip_item_from_slot(slot, item)
            self.update_inventory_listbox()

    def unequip_accessory(self):
        if self.player_stats.equipment["Accessories"]:
            accessory = self.player_stats.equipment["Accessories"][-1]  # Unequip the last accessory
            self.player_stats.unequip_item("Accessories", accessory)
            self.update_inventory_listbox()

    def start_play(self):
        if not self.play_initialized:
            self.current_step = 0
            self.advance_story()
            self.play_initialized = True

    def advance_story(self):
        if self.current_step == 0:
            self.play_text.insert(tk.END,
                                  'Azul smiled lightly at her, waving one hand in front of him. He took another sip of his hot chocolate, before turning his eyes to hers.\n',
                                  'white')
            self.play_text.insert(tk.END,
                                  '"Alright Ruby, could you please tell us if you heard anything...strange last night by any chance?"\n',
                                  'white')
            self.display_check(Check("Memory", 15, 0))  # Memory check with DC 15
        elif self.current_step == 1:
            self.play_text.insert(tk.END, '\n---------------------------------\n', 'white')
            self.play_text.insert(tk.END, '\nRuby stopped, rooted in place, glancing down a corridor of trees.\n',
                                  'white')
            self.play_text.insert(tk.END,
                                  'There were no branches on those trees on the lower half of their trunks. They were present higher than that, but not a single one lower.\n',
                                  'white')
            self.play_text.insert(tk.END, 'Her head hurt.\n', 'white')
            self.display_check(Check("Psyche", 12, 0))  # Psyche check with DC 12 and 18
        elif self.current_step == 2:
            self.play_text.insert(tk.END, '\n---------------------------------\n', 'white')
            self.play_text.insert(tk.END, 'With shaky legs, she moved back, but the stench clung to her still.\n',
                                  'white')
            self.play_text.insert(tk.END,
                                  'Holding her scarf up to her mouth, she pulled out her scroll and called Azul again, only for there to be no signal.\n',
                                  'white')
            self.play_text.insert(tk.END,
                                  'Releasing a shuddering breath, she moved forward, but before she could as much as take another step, her head throbbed.\n',
                                  'white')
            self.display_check(Check("Psyche", 15, 0))  # Psyche check
        elif self.current_step == 3:
            self.play_text.insert(tk.END, '\n---------------------------------\n', 'white')
            self.play_text.insert(tk.END,
                                  'The cave was a straight tunnel at the very least, as she couldn\'t spot any other paths through the shine of her flashlight.\n',
                                  'white')
            self.play_text.insert(tk.END, 'All of a sudden, however, Ruby stopped dead in her tracks.\n', 'white')
            self.display_check(Check("Caution", 15, 0))  # Caution check
        elif self.current_step == 4:
            self.play_text.insert(tk.END, '\n---------------------------------\n', 'white')
            self.play_text.insert(tk.END,
                                  'The voice stopped, and one eye nearly consumed by fire, yet still as black as death, turned to stare into her soul.\n',
                                  'white')
            self.play_text.insert(tk.END, 'And the forest walker, in its death throes, started laughing.\n', 'white')
            self.play_text.insert(tk.END, 'Ruby screamed.\n', 'white')
            self.play_text.insert(tk.END,
                                  'At least her father would be here tomorrow…so she could sob into his chest, and weep wholeheartedly.\n',
                                  'white')
            self.play_text.insert(tk.END, 'Weep from so many things. From the corpses. From the monster.\n', 'white')
            self.play_text.insert(tk.END,
                                  'And from everything else she\'d recalled from the book stuck inside her head.\n',
                                  'white')
            self.display_check(Check("Memory", 15, 0))  # Memory check
        elif self.current_step == 5:
            self.play_text.insert(tk.END, '\n---------------------------------\n', 'white')
            self.play_text.insert(tk.END,
                                  'Until finally, she reached out to her dear, dear cloak, which she hadn\'t worn that fateful day. The red cloak that was still pristine. That had yet to see fire and bone, hatred and agony. She clutched it to her chest, and breathed out a sigh of relief at the comfort it brought to her empty husk.\n',
                                  'white')
            self.play_text.insert(tk.END, 'It would work out, somehow.\n', 'white')
            self.play_text.insert(tk.END, 'All she needed to do…was pick.\n', 'white')
            self.display_choicebox()

    def show_dice_roll(self):
        if self.current_check:
            rolls, result, result_color = self.player_stats.perform_check(self.current_check)
            self.result_text.config(text=f"Dice rolls: {rolls}\n{result}", fg=result_color)
            self.roll_button.config(state=tk.DISABLED)

            if self.current_step == 0:  # Memory check
                if result == "Fail":
                    self.player_stats.psyche_current -= 1
                    self.result_text.config(
                        text=f"Dice rolls: {rolls}\n{result}\nPsyche: {self.player_stats.psyche_current}/{self.player_stats.psyche_max}",
                        fg='purple')
            elif self.current_step == 1:  # Psyche check with DC 12 and 18
                highest_roll = max(rolls) + self.current_check.modifier
                if highest_roll < 12:
                    self.player_stats.psyche_current -= 2
                elif highest_roll < 18:
                    self.player_stats.psyche_current -= 1
                self.result_text.config(
                    text=f"Dice rolls: {rolls}\n{result}\nPsyche: {self.player_stats.psyche_current}/{self.player_stats.psyche_max}",
                    fg='purple')
            elif self.current_step == 2:  # Psyche check
                if result == "Fail":
                    self.player_stats.psyche_current -= 1
                    self.result_text.config(
                        text=f"Dice rolls: {rolls}\n{result}\nPsyche: {self.player_stats.psyche_current}/{self.player_stats.psyche_max}",
                        fg='purple')
            elif self.current_step == 3:  # Caution check
                # Placeholder logic for caution check results
                pass
            elif self.current_step == 4:  # Memory check
                if result == "Fail":
                    self.player_stats.psyche_current -= 1
                    self.result_text.config(
                        text=f"Dice rolls: {rolls}\n{result}\nPsyche: {self.player_stats.psyche_current}/{self.player_stats.psyche_max}",
                        fg='purple')

            self.player_stats.update_stats()
            self.current_step += 1
            self.advance_story()

    def on_tab_changed(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Play":
            self.start_play()
        elif selected_tab == "Character":
            self.display_character_sheet()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()

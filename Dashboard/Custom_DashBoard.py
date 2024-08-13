import customtkinter
from DT import DigitalTwin

class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("512x552")
        self.minsize(512, 562)
        self.maxsize(512, 562)
        self.title("Dashboard Battery Digital Twin")

        # Add the digital twin
        self.digital_twin = DigitalTwin("localhost", 1883, "battery.prediction:hivelab")

        self.update_active = True

        # Frame DT State
        state = customtkinter.CTkFrame(self, width=211, height=168, fg_color="gray", corner_radius=15, border_width=2)
        state.place(x=30, y=30)
        
        title_state = customtkinter.CTkLabel(state, text="State of the battery:", bg_color="black", font=("Helvetica", 14, "underline"), width=191)
        title_state.place(x=10, y=10)
        
        voltage_label = customtkinter.CTkLabel(state, text="Voltage:", anchor="w")
        voltage_label.place(x=10, y=40)
        self.voltage_entry = customtkinter.CTkEntry(state, placeholder_text="Voltage", width=100)
        self.voltage_entry.place(x=80, y=40)
        self.voltage_entry.bind("<FocusIn>", self.pause_update)
        self.voltage_entry.bind("<FocusOut>", self.resume_update)
        
        current_label = customtkinter.CTkLabel(state, text="Current:", anchor="w")
        current_label.place(x=10, y=70)
        self.current_entry = customtkinter.CTkEntry(state, placeholder_text="Current", width=100)
        self.current_entry.place(x=80, y=70)
        self.current_entry.bind("<FocusIn>", self.pause_update)
        self.current_entry.bind("<FocusOut>", self.resume_update)
        
        capacity_label = customtkinter.CTkLabel(state, text="Capacity:", anchor="w")
        capacity_label.place(x=10, y=100)
        self.capacity_entry = customtkinter.CTkEntry(state, placeholder_text="Capacity", width=100)
        self.capacity_entry.place(x=80, y=100)
        self.capacity_entry.bind("<FocusIn>", self.pause_update)
        self.capacity_entry.bind("<FocusOut>", self.resume_update)

        new_value = customtkinter.CTkButton(state, text="Set random value", command=self.set_random_value, width=90)
        new_value.place(x=10, y=140)

        update_button = customtkinter.CTkButton(state, text="Update Values", command=self.update_digital_twin, width=90)
        update_button.place(x=110, y=140)

        # Frame DT Connection
        connection = customtkinter.CTkFrame(self, width=211, height=168, fg_color="gray", corner_radius=15, border_width=2)
        connection.place(x=271, y=30)
        
        title_connection = customtkinter.CTkLabel(connection, text="Connection:", bg_color="black", font=("Helvetica", 14, "underline"), width=191)
        title_connection.place(x=10, y=10)
        
        connect = customtkinter.CTkButton(connection, text="Connect", command=self.digital_twin.connect)
        connect.place(relx=0.5, rely=0.45, anchor="center")
        
        disconnect = customtkinter.CTkButton(connection, text="Disconnect", command=self.digital_twin.disconnect)
        disconnect.place(relx=0.5, rely=0.75, anchor="center")

        # Model
        model = customtkinter.CTkFrame(self, width=452, height=294, fg_color="gray", corner_radius=15, border_width=2)
        model.place(x=30, y=228)
        
        title_model = customtkinter.CTkLabel(model, text="Model:", bg_color="black", font=("Helvetica", 14, "underline"), width=432)
        title_model.place(x=10, y=10)
        
        path = customtkinter.CTkLabel(model, text="Path to the model to load:")
        path.place(x=10, y=40)
        
        text = customtkinter.StringVar(value="Enter your path")
        text_path = customtkinter.CTkEntry(model, textvariable=text, width=432)
        text_path.place(x=10, y=70)
        
        load = customtkinter.CTkButton(model, text="Load Model", command=None)
        load.place(relx=0.5, rely=0.45, anchor="center")

        predict = customtkinter.CTkButton(model, text="Make a prediction", command=None)
        predict.place(relx=0.5, rely=0.6, anchor="center")

        prediction = customtkinter.CTkLabel(model, text="Remaining battery usage time:")
        prediction.place(x=10, y=200)

        # Start the update loop
        self.update_values()

    def set_random_value(self):
        import random
        voltage = random.uniform(3.0, 4.2)
        current = random.uniform(0.0, 2.0)
        capacity = random.uniform(0.0, 100.0)
        self.digital_twin.update_features(voltage=voltage, current=current, capacity=capacity)

    def update_digital_twin(self):
        try:
            voltage = float(self.voltage_entry.get())
            current = float(self.current_entry.get())
            capacity = float(self.capacity_entry.get())
            self.digital_twin.update_features(voltage=voltage, current=current, capacity=capacity)
        except ValueError:
            print("Please enter valid numerical values.")

    def update_values(self):
        if self.update_active:
            # Update the entry fields with the latest values
            self.voltage_entry.delete(0, 'end')
            self.voltage_entry.insert(0, str(self.digital_twin.voltage))
            self.current_entry.delete(0, 'end')
            self.current_entry.insert(0, str(self.digital_twin.current))
            self.capacity_entry.delete(0, 'end')
            self.capacity_entry.insert(0, str(self.digital_twin.capacity))

        # Schedule the next update
        self.after(1000, self.update_values)  # Update every second

    def pause_update(self, event):
        self.update_active = False

    def resume_update(self, event):
        self.update_active = True

main_window = Window()
main_window.mainloop()

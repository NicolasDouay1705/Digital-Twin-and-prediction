from tkinter import *
import tkinter.font as tkFont

main_window = Tk()
main_window.title("DashBoard Battery Digital Twin")
main_window.geometry("512x512")
main_window.minsize(512,512)
main_window.maxsize(512,512)

#Frame DT State:
state = Frame(main_window, bg="white", borderwidth=2, relief=GROOVE, width=128, height=128)
state.pack_propagate(False)
state.place(x=30, y=30)
title_state = Label(state, text="State of the battery:", bg="yellow", font=tkFont.Font(family="Helvetica", size=11, underline=True))
title_state.pack(fill='x')
voltage = Label(state, text="Voltage:", anchor="w")
voltage.pack(fill='x')
current = Label(state, text="Current:", anchor="w")
current.pack(fill='x')
capacity = Label(state, text="Capacity:", anchor="w")
capacity.pack(fill='x')

#Frame DT Connection
connection = Frame(main_window, bg="white", borderwidth=2, relief=GROOVE, width=128, height=128)
connection.pack_propagate(False)
connection.place(x=354 ,y=30)
title_connection = Label(connection, text="Connection:", bg="yellow", font=tkFont.Font(family="Helvetica", size=11, underline=True))
title_connection.pack(fill='x')
connect = Button(connection, text="Connect", command=None)
connect.pack()
disconnect = Button(connection, text="Disconnect", command=None)
disconnect.pack()

#Model
model = Frame(main_window, bg="white", borderwidth=2, width=452 ,height=294)
model.place(x=30, y=188)
title_model = Label(model, text="Model:", bg="yellow", font=tkFont.Font(family="Helvetica", size=11, underline=True))
title_model.place(x=10, y=10)
path = Label(model, text="Path to the model to load:")
path.place (x=10, y=40)
text = StringVar()
text.set("Enter your path")
text_path = Entry(model, textvariable=text, width=70)
text_path.place(x=10, y=70)
load = Button(model, text="Load Model", command=None)
load.place(x=10, y=100)

# #Prediction
# prediction = Frame(main_window, bg="white", borderwidth=2, width=, height=)
# # predict = Button(model, text="Make a prediction", command=None)
# # predict.place(x=10, y=130)

main_window.mainloop()
import Tkinter as tk
import ttk
from Tkinter import StringVar
import tkFileDialog
from ttk import Frame, Style
import nep

    
        
class MainGUI:
    def __init__(self, master):
        #Definition of the main GUI

        node = nep.node("enviroment_node") # Create a new node
        conf = node.conf_pub() # Select the configuration of the subscriber
        self.pub_emotion = node.new_pub("/enviroment", conf)  # Set the topic and the configuration of the subscriber
    
        self.master = master
        self.master.title("Enviroment simulation")
        
        # Create scale for each parameter
        self.w = tk.Scale(master, from_=0, to=50, orient=tk.HORIZONTAL, length=500, command = self.update_temp, label = 'Temperature')
        self.w.set(20)
        self.w.grid(row=0,column=0)

        self.w1 = tk.Scale(master, from_=0, to= 100, orient=tk.HORIZONTAL, length=500, command = self.update_hum, label = 'Humidity')
        self.w1.set(50)
        self.w1.grid(row=1,column=0)

        self.w2 = tk.Scale(master, from_=0, to= 100, orient=tk.HORIZONTAL, length=500, command = self.update_bri, label = 'Brightness')
        self.w2.set(50)
        self.w2.grid(row=2,column=0)

        self.w3 = tk.Scale(master, from_=20, to= 80, orient=tk.HORIZONTAL, length=500, command = self.update_tr, label = 'Temp robot')
        self.w2.set(50)
        self.w2.grid(row=4,column=0)

        self.T = 20
        self.H = 50
        self.B = 50
        self.RT = 0
        msg = {"T": self.T, "H": self.H, "B": self.B, "RT": self.RT, }
        self.pub_emotion.send_info(msg)


    # Help function for the interface, for the second order
    def nothing (self,val):
        i = int(val)
        
    # ------- Events, change parameters of the system, graph and save the data -------
    def update_temp(self,val):
        print "Temperature: ", int(val)
        self.T = int(val)
        self.send_enviroment_data()

    def update_hum(self,val):
        print "Humidity: ", int(val)
        self.H = int(val)
        self.send_enviroment_data()

    def update_bri(self,val):
        print "Brightness: ", int(val)
        self.B = int(val)
        self.send_enviroment_data()

    def update_tr(self,val):
        print "Robot temp: ", int(val)
        self.RT = int(val)
        self.send_enviroment_data()

    def send_enviroment_data(self):
        msg = {"T": self.T, "H": self.H, "B": self.B, "RT": self.RT }
        self.pub_emotion.send_info(msg)


def main():
        
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

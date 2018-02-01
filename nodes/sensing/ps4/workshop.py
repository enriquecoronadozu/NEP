from tkinter import *
from tkinter import ttk
root = Tk()
import threading
import time
from nep import*




LY = 0
LX = 0
triangle = [False,False]
circle = [False,False]
square = [False,False]
L1 = [False,False]
R1 = [False,False]
X = [False,False]
up = [False,False]
down = [False,False]
left = [False,False]
right = [False,False]

r = interaction()
max_values = 0
idx = 0



def onTest():
    global selection_number, idx

    while True:

        
        if triangle[0] == False and triangle[1] == True:
            print "change triangle"
            triangle[0] =  triangle[1]
            r.do_parallel_actions(["wake_up","none"], { },["nao"])
            
        if circle[0] == False and circle[1] == True:
            print "change circle"
            circle[0] =  circle[1]
            msg = ""
            
        if square[0] == False and square[1] == True:
            msg = countrynames[idx]
            r.do_parallel_actions(["say_contextual",msg], {"language":"English"},["nao"])
            
            
            print "change square"
            square[0] =  square[1]
            
        if X[0] == False and X[1] == True:
            print "change X"
            X[0] =  X[1]
            msg = ""
            r.do_parallel_actions(["rest","none"], { },["nao"])
            
        if up[0] == False and up[1] == True:
            print "change down"
            up[0] =  up[1]
            lbox.selection_clear(selection_number)

            if selection_number > 0:
                selection_number =  selection_number - 1

            else:
                selection_number = max_value-1
                
            lbox.selection_set(selection_number)
            print selection_number

            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                name = countrynames[idx]
                statusmsg.set("Student %s n: %s" % (name, idx))

        
        if down[0] == False and down[1] == True:
            print "change up"
            down[0] =  down[1]
      
            lbox.selection_clear(selection_number)

            if selection_number < len(countrynames)-1:
                
                selection_number =  selection_number + 1

            else:

                selection_number = 0
            print selection_number
                
            lbox.selection_set(selection_number)

            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                name = countrynames[idx]
                statusmsg.set("Student %s n: %s" % (name, idx))
                

def onUpdateData():
    global LY, triangle, LX, circle, square, X, R1, L1
    print ("Waiting data...")
    msg = {'action':'remote', 'input': "velocity", 'params':{'x':0, 'y':0, 'theta':0 }}
    while True :
        s, data = sub.listen_info()
        if s == True:

            triangle[0] = triangle[1]
            circle[0] = circle[1]
            square[0] = square[1]
            X[0] = X[1]
            L1[0] =  L1[1]
            R1[0] = R1[1]
            down[0] = down[1]
            left[0] = left[1]
            right[0] = right[1]
            up[0] = up[1]
            
            triangle[1] = data["button"]["triangle"]
            circle[1] = data["button"]["circle"]
            square[1] = data["button"]["square"]
            X[1] = data["button"]["x"]
            L1[1] = data["button"]["L1"]
            R1[1] = data["button"]["R1"]
            up[1] = data["hat"]["up"]
            down[1] = data["hat"]["down"]
            left[1] = data["hat"]["left"]
            right[1] = data["hat"]["right"]
            
            
            

node = nep.node("animation_maker")
c = node.conf_sub()
sub = node.new_sub("ps4", c)
c = node.conf_pub(mode = "many2many")
pub = node.new_pub("/action_request", c)

sense = threading.Thread(target = onUpdateData)
# Used to finish the background thread when the main thread finish
sense.daemon = True
# Start new thread 
sense.start()
print ("Thread launched")


selection_number = 0

# Initialize our country "databases":
#  - the list of country codes (a subset anyway)
#  - a parallel list of country names, in the same order as the country codes
#  - a hash table mapping country code to population<

countrynames = (
"Any other question? as the last question",
"Professor Shibata",
"I´have no idea about these difficult questions",
"here are some very good materials for the discussion!", 
"May be we could hear what the others panelists think?",
"Should we try to conclude now",
"Thank you very much to the four panelists. I think it is time for everyone to take  some energy for the afternoon session. Fodd is served in the back, while Paro and I will go and charge our batteries.",

)

max_value = len(countrynames)
print max_value
cnames = StringVar(value=countrynames)

sentmsg = StringVar()
statusmsg = StringVar()


# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

# Create the different widgets; note the variables that many
# of them are bound to, as well as the button callback.
# Note we're using the StringVar() 'cnames', constructed from 'countrynames'
lbox = Listbox(c, listvariable=cnames, height=len(countrynames))
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=6, columnspan=2, sticky=(W,E))
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)


# Colorize alternating lines of the listbox
for i in range(0,len(countrynames),2):
    lbox.itemconfigure(i, background='#f0f0ff')

# Set the starting state of the interface, including selecting the
# default gift to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> event is only
# generated when the user makes a change, we explicitly call showPopulation.

sentmsg.set('')
statusmsg.set('')
lbox.selection_clear(0)
selection_number = 0
lbox.selection_set(selection_number)
idxs = lbox.curselection()
if len(idxs)==1:
    idx = int(idxs[0])

time.sleep(.1)
select = threading.Thread(target = onTest)
# Used to finish the background thread when the main thread finish
select.daemon = True
# Start new thread 
select.start()

   


root.mainloop()

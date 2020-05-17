import tkinter as tk
from tkinter import ttk # for the Combobox
root = tk.Tk()
root.title('Unit Converter')

controls = []
cboxindices = []
   
def onkeypress(event):
    # Event handler for entry key pressed 
    st = event.widget.get()
    ch = event.char
    deletechar = chr(127) # hex 7F
    endflag = 0 # non-zero if key is return
    returnchar = '\r' # the return or enter key
    ic = event.widget.index(tk.INSERT)
    if ord(ch) > 255: return # Ignore arrow keys
    if ch == deletechar:
      st = st[:ic-1] + st[ic:]
    else:
      if ch == returnchar: endflag = 1 # signal return key pressed
      else:
        st = st[:ic] + ch + st[ic:]
    process(icoldvalue, st, endflag)

def onselection(event):
    # Event handler for Combobox selected
    for controlindex in range(len(controls)):
      if event.widget == controls[controlindex]: break
    unittypeindex = icunittype
    if controlindex == unittypeindex:
      setupcomboboxes(1)
    process(controlindex)
    
def setupcomboboxes(mode):
    # Fill combobox lists 
    unittypeindex = icunittype
    if mode == 0:
      # set up unittype list.
      units = []
      for item in conversiondata:
        units.append(item[0])
      controls[unittypeindex]['values'] = units
      controls[unittypeindex].current(0) # set the current item selection
    unittype = controls[unittypeindex].current()
    convs = conversiondata[unittype][1].conversions
    units = []
    for u in convs:
      units.append(u[0])
    cur = 0
    for cindex in (icoldunit, icnewunit):
      controls[cindex]['values'] = units
      controls[cindex].current(cur)
      cur += 1

oldvalue = 1.0 
def convert(unittype=0, oldvalue=1.0, oldunit=0, newunit=0):
    # convert the current entry value from old to the new units
    conv = conversiondata[unittype][1].conversions
    newvalue = (float(oldvalue) * conv[oldunit][1] + conv[oldunit][2] \
    - conv[newunit][2])/ conv[newunit][1]
    newvaluetext = '{:.5}'.format(newvalue)
    if newvalue <= 0.001 or newvalue >= 1000.:
      newvaluetext = '{:.5e}'.format(newvalue) 
    controls[icnewvalue].configure(text=newvaluetext)
    return newvalue

def entrytype(st='', endflag=0):
    noend = '+-Ee' 
    noreps = '.Ee' 
    global oldvalue
    pm = '+-'
    validchars = '0123456789' + noreps + pm # all valid alphanumeric characters
    type = 0
    stl = len(st) 
    if stl == 0: type = -1 # a blank entry will fail attempted conversion
    if type == 0:
      ic = 0
      for c in st:
        valid = c in validchars # valid = True if character c is present in validchars
        if not valid:
          type = -1
          break
        if type == 0 and ic > 0:
          norep = c in noreps and c in st[:ic] # True if c is in both Lists    
          if norep:
            type = -1
            break
        ic = ic + 1 
      if type == 0:
        if st.count('e') + st.count('E')> 1: type = -1 # No repeats of e or E
        # test for more then one + or -; note e or E restarts the count
        ieE = max (st.find('e'), st.find('E')) + 1
        ch = st[-1]
        if ch == '+' or ch == '-':
          if st[ieE:].count('+') + st[ieE:].count('-') > 1: type = -1
        # No '.' allowed in exponent
        if ch == '.' and ieE > 1 and st[ieE:].count('.') > 0: type = -1
        if type == 0:
          if st[-1] not in noend:
            # st[-1] is the last element, [-2] the one preceding it, ...
            type = 1
          else:
            # if ch == returnchar: type = -1 # NO! return chr never gets into string.
            if endflag != 0: type = -1
    if type >= 0: oldvalue = st
    return type
    
def process(controlindex=0, entrystring='', endflag = 0):
    global oldvalue
    oldvalue = controls[icoldvalue].get()   
    if controlindex == icoldvalue:
      col = 'light blue'
      flag = entrytype(entrystring, endflag) # also resets oldvalue
      if flag < 0:
        col = 'red'
      controls[icoldvalue].configure(bg=col)
      
      if flag <= 0:
        return
    # Get current settings of the controls
    unittype =controls[icunittype].current()
    oldunit = controls[icoldunit].current()
    newunit = controls[icnewunit].current()
    # Do the conversion
    newvalue = convert(unittype, oldvalue, oldunit, newunit) 
    
class Force: # these subclasses do not need initializers
    conversions = (('Newtons', 1.0, 0.), ('pounds-force', 4.448222, 0.),
    ('dynes', 1.0e-5, 0.), ('kilogram-force', 9.80665, 0.))

class Length:
    conversions = (('cms', 1.0, 0.), ('meters', 1.0e2, 0.), ('kilometers', 1.0e5, 0.),
    ('inches', 2.54, 0.), ('feet', 30.48, 0.), ('yards', 91.44, 0.),
    ('miles', 1.609344e5, 0.))

class Mass:
    conversions = (('grams', 1.0, 0.), ('kilograms', 1.0e3, 0.),
    ('ounces', 28.34952, 0.), ('pounds', 453.59237, 0.), ('tons', 9.07185e5, 0.))

class Temperature:
    conversions = (('Celsius', 1.0, 0.), ('Fahrenheit', 100./180, -160./9),
    ('Kelvin', 1.0, -273.15))


conversiondata = (('Mass', Mass()), ('Length', Length()),
      ('Weight', Force()), ('Force', Force()),
      ('Temperature', Temperature()))
controldata = (('unit type', 'Combobox'), ('old value', 'Entry'),
      ('old unit', 'Combobox'), (' = ', 'Label'), ('new value', 'Label'), 
      ('new unit', 'Combobox'))
for ic in range(len(controldata)):
      if controldata[ic][0] == 'unit type': icunittype = ic
      if controldata[ic][0] == 'old value': icoldvalue = ic
      if controldata[ic][0] == 'old unit': icoldunit = ic
      if controldata[ic][0] == 'new value': icnewvalue = ic
      if controldata[ic][0] == 'new unit': icnewunit = ic

for c in controldata:
  if c[1] == 'Combobox':
    control = ttk.Combobox(root, height = 60, width = 30)
    control.bind ('<<ComboboxSelected>>', onselection)
  if c[1] == 'Entry':
      control = tk.Entry(root, width=40, bd=10, bg='lightgreen')
      control.insert (0, '1.0')
      control.bind('<Key>', onkeypress)
  if c[1] == 'Label':
      w = 40
      col = 'lightgreen'
      t = '        '
      if c[0] != 'new value':
        w = 20
        col = 'red'
        t = '=' 
      control = tk.Label(root, width=40, bd=10, text=t, bg=col)
  controls.append(control)
  control.pack(side = 'left') # Add the control to the layout
setupcomboboxes(0) # 0 sets up unit type

process()
root.mainloop()

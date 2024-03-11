import tkinter as tk
from ColorRangeSelector import ColorRangeSelector

def getResults():
  label['text']= "FROM BUTTON:\ns1= {}\ns2={}\ns3={}".format(selector.result,selector2.result,selector3.result)

def getEventResults(self):
  label['text'] = "FROM EVENT ON ROOT:\ns1= {}\ns2={}\ns3={}".format(selector.result,selector2.result,selector3.result)

root = tk.Tk()
root.geometry("1000x500")

selector = ColorRangeSelector(root,10,70,900,30, bg='#ccc', lineColor='white', textColor='#222')
selector2 = ColorRangeSelector(root,50,150)
selector3 = ColorRangeSelector(root,400,150,510,100, initial=[70.5,203])

button = tk.Button(root, text ="Print Results", command = getResults)
label = tk.Label( root, text="")
button.place(x=0,y=0)
label.place(x=500,y=0)

root.bind( '<B1-Motion>', getEventResults)

root.mainloop()
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# plotting the PPF graphs 
def graph(x1, x2, x3, x4, y1, y2, y3, y4, name1, name2, slide1, slide2):
    # converting the user input into arrays of floats
    x = np.array([float(x1), float(x2), float(x3), float(x4)])
    y = np.array([float(y1), float(y2), float(y3), float(y4)])

    # creating the basic graph with the 4 points
    # the user has not altered the sliders from their default position
    if (slide1 == 0 and slide2 == 0):

      # creating an outward bowed graph from the 4 points
      # the function generates 200 equally spaced points between the smallest and largest x-value
      # to smooth the graph
      xnew = np.linspace(x.min(), x.max(), 200) 

      # smoothing over the line on the graph 
      spline = make_interp_spline(x, y, k=3)
      y_smooth = spline(xnew)

      # labelling and plotting the graph
      plt.xlabel(name1)
      plt.ylabel(name2)
      plt.xlim([0, 2 * x.max()])
      plt.ylim([0, 2 * y.max()])
      plt.plot(xnew, y_smooth, label=createLabel(x, y, name1, name2))
      plt.legend()
      plt.show(block=False)
    else:
      # creating a graph of the altered points
      # the user has altered the sliders from their default postion

      # creating a new array with each of the points scaled by the slider position
      scaled_x = scaleArray(x, slide1)
      scaled_y = scaleArray(y, slide2)

      # creating an outward bowed graph from the 4 points
      # the function generates 200 equally spaced points between the smallest and largest x-value
      # to smooth the graph
      scaled_xnew = np.linspace(scaled_x.min(), scaled_x.max(), 200) 

      # smoothing over the line on the graph
      scaled_spline = make_interp_spline(scaled_x, scaled_y, k=3)
      scaled_y_smooth = scaled_spline(scaled_xnew)

      # labelling and plotting the graph
      plt.xlabel(name1)
      plt.ylabel(name2)
      plt.xlim([0, 2 * x.max()])
      plt.ylim([0, 2 * y.max()])
      plt.plot(scaled_xnew, scaled_y_smooth, linestyle="dotted", label=createLabel(scaled_x, scaled_y, name1, name2))
      plt.legend()
      plt.show(block=False)

# creating the gui
def create_gui():
  
  # creating the layout of the interface using PySimpleGUI
  layout = [[sg.Text("Name of first production line: "), sg.Input(key="name_production_1", size=(10))],
            [sg.Text("Name of second production line: "), sg.Input(key="name_production_2", size=(10))],
           [sg.Text("Input 4 points (the two end ones and the two middle ones), x must start from 0:")],
           [sg.Text("x1"), sg.Input(key="x1", size=(3)), sg.Text("y1"), sg.Input(key="y1", size=(3))],
           [sg.Text("x2"), sg.Input(key="x2", size=(3)), sg.Text("y2"), sg.Input(key="y2", size=(3))],
           [sg.Text("x3"), sg.Input(key="x3", size=(3)), sg.Text("y3"), sg.Input(key="y3", size=(3))],
           [sg.Text("x4"), sg.Input(key="x4", size=(3)), sg.Text("y4"), sg.Input(key="y4", size=(3))],
           [sg.Text("Percent change in the first production line: "), 
             sg.Slider(range=(-100, 100), orientation="horizontal", default_value=0, key="slider1")],
           [sg.Text("Percent change in the second prodcution line: "),
             sg.Slider(range=(-100, 100), orientation="horizontal", default_value=0, key="slider2")],
           [sg.Button("Create Graph")]]

  window = sg.Window("Test", layout)

  # running the gui and collecting the user inputs to create the graphs
  while(True):
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == "Create Graph":
        graph(values["x1"], values["x2"], values["x3"], values["x4"], 
              values["y1"], values["y2"], values["y3"], values["y4"],
              values["name_production_1"], values["name_production_2"],
              values["slider1"], values["slider2"])

# helper method to scale array
def scaleArray(arr, scale):
    return arr + (arr * (scale / 100))

# helper method to create a name for the legend 
def createLabel(x, y, name1, name2):
  return str(round((x.max() / y.max()), 2)) + " " + name1 + " per " + name2

def main():
  create_gui()

# entry point for the script
if __name__ == "__main__":
  main()

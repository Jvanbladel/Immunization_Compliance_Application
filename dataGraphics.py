
# import SQL_Engine
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px




def pieChart(data, labels, color):
    plt.pie(data, labels=labels, colors=color, autopct='%1.1f%%')
    plt.show()

'''
    displaying three lines on line graph
    using matplotlib'''
def performanceMeasurement():
    df = pd.DataFrame({'x': range(1, 11), 'RANDOM1': np.random.randn(10),
                   'RANDOM2': np.random.randn(10) + range(1, 11),
                   'RANDOM3': np.random.randn(10) + range(11, 21)})

    # multiple line plot
    plt.plot('x', 'RANDOM1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4,
             label='male')
    plt.plot('x', 'RANDOM2', data=df, marker='', color='olive', linewidth=2, label='female')
    plt.plot('x', 'RANDOM3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    plt.legend()
    plt.show()

    # df = pd.read_csv(data)

    # Indicated your x values and y values.




# pieChart([len(num_male),len(genderFrame)-len(num_male)], ['male', 'female'], ['#6e93cd', '#fbb7e0'])
# performanceMeasurement(0,0,0)'''

'''
    graphs using tkinter
'''
def tkinter():
    import tkinter as tk
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np

    app = tk.Tk()
    app.wm_title("Graphs")

    fig = Figure(figsize=(6, 4), dpi=96)
    a = np.array([1,2,3])
    ax = fig.add_subplot(111)

    line, = ax.plot(a,np.array([0,0.5,2]))
    line2, = ax.plot(a,0.55*a)

    graph = FigureCanvasTkAgg(fig, master=app)
    canvas = graph.get_tk_widget()
    canvas.grid(row=0, column=0, rowspan = 11, padx =10, pady =5)

    def updateScale(value):
       # print("scale is now %s" % (value))
       b = float(value)*a
       # set new data to the line
       line2.set_data(a,b)
       # rescale the axes
       ax.relim()
       ax.autoscale()
       #draw canvas
       fig.canvas.draw_idle()


    value = tk.DoubleVar()
    scale = tk.Scale(app, variable=value, orient="horizontal",length = 100,
                     from_=0.55, to=2.75, resolution = 0.01,command=updateScale)
    scale.grid(row=0, column=1)
    app.mainloop()

#matplotlib
#performanceMeasurement()


#tkinter
#tkinter()
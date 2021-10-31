import doxyplot_core as dp

plot = dp.Doxyplot()

x=[1,2,3,4]
y=[4,5,4.5,2]
y2=[5,7,2,1]
y3=[10,9,5,4]
y4=[5,4,2,2]

plot.append_data(
    x, y, 'r', 'Line1', linewidth=2.0)
plot.append_data(x, y2, 'k', 'Line2', linewidth=2.0)
plot.append_data(x,y3, c='g', label='Line3')
plot.append_data(x,y4, c='b', label='Line4')
plot.construct_plot("Doxyplot", "Time", "Velocity",save="export.png")


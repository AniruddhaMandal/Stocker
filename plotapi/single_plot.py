from bokeh.plotting import figure, show
from Stocker.stocks import Stock

def _plot(st: Stock):
    """
        `st` is the stock instance of the `stock` class
    """
    st.config()
    p = figure(
        title=f"Graph for {st.name}",
        x_axis_label= "Dates",
        x_axis_type = "datetime",
        y_axis_label= "Price")
    p.line(
        st.dates, 
        st.value, 
        legend_label=f"{st.id}",
        line_width=2)
    show(p)
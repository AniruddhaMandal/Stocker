from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
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
        y_axis_label= "Price",
        height=645,
        width=1340)
    p.line(
        st.dates, 
        st.value, 
        legend_label=f"{st.id}",
        line_width=2,
        )
    return file_html(p,CDN, "my_plot")
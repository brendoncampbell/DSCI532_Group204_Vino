import altair as alt
import pandas as pd
from vega_datasets import data

def wrangle_varieties(df):
    """
    Wrangle the data to group by state.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns the data grouped by variety
    """

    # Group and aggregate data by wine varieties
    variety_df = df.groupby(['variety']).size().reset_index(name='counts')
    variety_df = variety_df.sort_values(by='counts')
    popular_varieties = variety_df.query('counts > 500')['variety']

    # Filter the data set to include only popular grape varieties
    varieties_plot_data = df[df['variety'].isin(popular_varieties.tolist())]

    return varieties_plot_data


def plot_heatmap(df, x_name='price'):
    """
    Plot a heatmap of showing the average value of wines from popular grape varieties at a range of price points.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns altiar plot objects.
    """

    def vino_special_heatmap():
        font = "Helvetica"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 500
                },
                "axisX": {
                    "domain": True,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0,  #no angle required for this plot
                    "tickColor": axisColor,
                    "tickSize": 5, 
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10,
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10,
                    "title": "Y Axis Title (units)",
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('vino_special_heatmap', vino_special_heatmap)

    # enable the newly registered theme
    alt.themes.enable('vino_special_heatmap')

    varieties_chart_data = wrangle_varieties(df)

    if x_name == 'price': 
        varieties_heatmap_plot = alt.Chart(varieties_chart_data.query('price < 50')).mark_rect().encode(
            x=alt.X(x_name + ':Q',
                    bin=alt.Bin(maxbins=10),
                    title="Price ($)"),
            y=alt.Y('variety:O', 
                    title="Grape Variety"),
            color=alt.Color('average(value_scaled):Q',
                            scale=alt.Scale(scheme="bluepurple"),
            legend=alt.Legend(
                            orient='right', title="Average Value")
                        ),
            tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                     alt.Tooltip('average(price)', format='$.2f'),
                     alt.Tooltip('average(value_scaled)', format='.2f'),
                     alt.Tooltip('count(title)')]
        ).properties(
            title="Average Value Scores for Popular Grape Varieties, by Price"
        ).configure_axis(
            grid=False,
            labelAngle=0
        )
    
    if x_name == 'points':
        varieties_heatmap_plot = alt.Chart(varieties_chart_data).mark_rect().encode(
            x=alt.X('points:Q',
                        bin=alt.Bin(maxbins=10),
                        title="Rating"),
            y=alt.Y('variety:O', 
                    title="Grape Variety"),
            color=alt.Color('average(value_scaled):Q',
                            scale=alt.Scale(scheme="bluepurple"),
            legend=alt.Legend(
                            orient='right', title="Average Value")
                        ),
            tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                     alt.Tooltip('average(price)', format='$.2f'),
                     alt.Tooltip('average(value_scaled)', format='.2f'),
                     alt.Tooltip('count(title)')]
        ).properties(
            title="Average Value Scores for Popular Grape Varieties, by Rating"
        ).configure_axis(
            grid=False,
            labelAngle=0
        )
    
    return varieties_heatmap_plot


if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_data.csv', index_col=0)
    plot_heatmap(df)
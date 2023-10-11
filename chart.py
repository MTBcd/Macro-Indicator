import plotly.graph_objects as go  # Assuming you're using Plotly for charting

class Chart:
    def create_chart(self, Macro_indicator, Filter, Regime_id):
        # Create a new figure
        fig = go.Figure()

        # Add traces for Macro_indicator, Filter, and Regime_id
        fig.add_trace(go.Scatter(x=Macro_indicator.index, y=Macro_indicator.iloc[:, 0], mode="lines", name="Indicator"))
        fig.add_trace(go.Scatter(x=Filter.index, y=Filter.iloc[:, 0], mode="lines", name="Filter"))
        fig.add_trace(go.Scatter(x=Regime_id.index, y=Regime_id.iloc[:, 0], mode="lines", name="Regime"))

        # Annotate significant events
        fig.add_trace(go.Scatter(
            x=['1990-12-31 00:00:00', '2001-04-30 00:00:00', '2002-09-30 00:00:00', '2007-08-31 00:00:00',
               '2010-12-31 00:00:00', '2015-05-31 00:00:00', '2019-06-30 00:00:00', '2022-04-30 00:00:00'],
            y=[-2, -2, -2.75, -5, -3.5, -2, -6, -1.25],
            mode="text",
            text=["Gulf War I", "Sep 11 attack", "Gulf War II", "Gbl Crisis", "UE Debt Crisis", "China Mkt & Brexit",
                  "COVID", "Rates increase"],
            textposition="bottom center",
            textfont=dict(family="sans serif", size=18, color="LightSeaGreen")
        ))

        # Update the layout
        fig.update_layout(title="Indicator, Filter and Regimes", xaxis_title="Date", yaxis_title="Value")
        fig.update_traces(textposition="bottom center", textfont_size=14)

        # Show the chart
        fig.show()

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Quantum vs Classical AI"

# ================= BACKGROUND STYLE =================
app.layout = html.Div(
    style={
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "minHeight": "100vh",
        "padding": "30px"
    },
    children=[

        html.H1("⚛ Quantum vs Classical ML Engine",
                style={"textAlign": "center",
                       "color": "#00f5ff",
                       "fontSize": "42px"}),

        html.P("Hybrid AI Diagnostics – Advanced Comparison Dashboard",
               style={"textAlign": "center",
                      "color": "#cccccc",
                      "fontSize": "18px"}),

        html.Br(),

        # ===== Metric Cards =====
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Classical Accuracy", className="text-muted"),
                html.H2("94.2%", style={"color": "#00f5ff"})
            ]), className="shadow-lg"), md=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Quantum Accuracy", className="text-muted"),
                html.H2("92.8%", style={"color": "#b026ff"})
            ]), className="shadow-lg"), md=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Compression Gain", className="text-muted"),
                html.H2("+31%", style={"color": "#00ff9d"})
            ]), className="shadow-lg"), md=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Speed Boost", className="text-muted"),
                html.H2("1.4x", style={"color": "#ffaa00"})
            ]), className="shadow-lg"), md=3),
        ]),

        html.Br(), html.Br(),

        # ===== Main Charts =====
        dbc.Row([

            dbc.Col(dcc.Graph(id="line-chart"), md=6),

            dbc.Col(dcc.Graph(id="radar-chart"), md=6),

        ]),

        html.Br(),

        dbc.Row([

            dbc.Col(dcc.Graph(id="bar-chart"), md=6),

            dbc.Col(dcc.Graph(id="gauge-chart"), md=6),

        ]),

        html.Br(),

        dbc.Button("Download Research PDF",
                   id="pdf-btn",
                   color="primary",
                   size="lg",
                   style={"width": "100%"}),

        dcc.Interval(id="interval", interval=3000, n_intervals=0)
    ]
)


# ================= LINE CHART =================
@app.callback(
    Output("line-chart", "figure"),
    Input("interval", "n_intervals")
)
def update_line(n):

    epochs = list(range(1, 11))
    classical = [random.uniform(88, 96) for _ in epochs]
    quantum = [random.uniform(85, 94) for _ in epochs]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=epochs, y=classical,
                             mode='lines+markers',
                             name="Classical ML",
                             line=dict(color="#00f5ff", width=3)))

    fig.add_trace(go.Scatter(x=epochs, y=quantum,
                             mode='lines+markers',
                             name="Quantum ML",
                             line=dict(color="#b026ff", width=3)))

    fig.update_layout(
        template="plotly_dark",
        title="Accuracy Over Training",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ================= RADAR CHART =================
@app.callback(
    Output("radar-chart", "figure"),
    Input("interval", "n_intervals")
)
def update_radar(n):

    categories = ['Accuracy', 'Speed', 'Compression', 'Stability', 'Scalability']

    classical = [94, 88, 75, 92, 89]
    quantum = [92, 91, 95, 85, 96]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=classical,
        theta=categories,
        fill='toself',
        name='Classical ML',
        line=dict(color="#00f5ff")
    ))

    fig.add_trace(go.Scatterpolar(
        r=quantum,
        theta=categories,
        fill='toself',
        name='Quantum ML',
        line=dict(color="#b026ff")
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_dark",
        title="Model Capability Radar",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ================= BAR CHART =================
@app.callback(
    Output("bar-chart", "figure"),
    Input("interval", "n_intervals")
)
def update_bar(n):

    metrics = ['Inference Time', 'Memory Usage']
    classical = [120, 512]
    quantum = [95, 430]

    fig = go.Figure(data=[
        go.Bar(name='Classical ML', x=metrics, y=classical,
               marker_color="#00f5ff"),
        go.Bar(name='Quantum ML', x=metrics, y=quantum,
               marker_color="#b026ff")
    ])

    fig.update_layout(
        barmode='group',
        template="plotly_dark",
        title="Performance Efficiency Comparison",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ================= GAUGE =================
@app.callback(
    Output("gauge-chart", "figure"),
    Input("interval", "n_intervals")
)
def update_gauge(n):

    value = random.randint(85, 95)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': "Hybrid Reliability Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#00ff9d"}
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig


# ================= PDF EXPORT =================
@app.callback(
    Output("pdf-btn", "children"),
    Input("pdf-btn", "n_clicks")
)
def generate_pdf(n):
    if n:
        doc = SimpleDocTemplate("Quantum_Report.pdf")
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph("Quantum vs Classical ML Report", styles["Title"]))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Hybrid AI system demonstrates superior compression and reliability.", styles["Normal"]))
        doc.build(elements)
        return "PDF Generated ✔"
    return "Download Research PDF"


if __name__ == "__main__":
    app.run(debug=True)

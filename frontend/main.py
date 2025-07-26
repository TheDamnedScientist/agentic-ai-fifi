import streamlit as st
"""
This Streamlit application, "FIFI: Financial Intelligence powered by Fi", provides a visually rich dashboard for personal financial insights, including authentication, financial summaries, behavioral classification, and a chat interface.
Main Features:
---------------
- **Custom Theming & SVG Background:** Uses inline SVG and CSS for a stylized, banknote-themed background and modern UI elements.
- **Authentication:** Simple username/password login system using Streamlit session state.
- **Settings Panel:** Allows users to manage accounts, export data, connect tools, manage privacy, and log out.
- **Financial Insights:**
    - Net worth display.
    - Monthly spending breakdown by category (pie chart).
    - Behavioral spending classification (radar chart).
    - Monthly spending trends (line chart).
    - Credit usage over time (bar chart).
    - Top 3 best and worst investments (horizontal bar charts).
- **Chat Interface:** Users can interact with a mock chatbot ("FiFi") for financial queries, with prompt buttons and chat history display.
Mock Data:
-----------
- Financial data, investment returns, and credit usage are generated with placeholder/mock values for demonstration.
Session State:
---------------
- Manages login state, chat history, and user input for a seamless interactive experience.
Dependencies:
--------------
- streamlit
- pandas
- numpy
- plotly
- datetime
- urllib
Usage:
-------
Run the script with Streamlit to launch the dashboard. Authenticate with the hardcoded credentials ("alok" / "chutya") to access the main features.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import urllib.parse


# --- SVG Banknote as page background, fixed under all content ---
banknote_svg = """
<svg width="700" height="265" viewBox="0 0 700 265" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="680" height="245" rx="30" fill="#284968" fill-opacity="0.1"/>
  <rect x="11" y="11" width="678" height="243" rx="30" stroke="#ade1ff" stroke-width="3" stroke-opacity="0.1"/>
  <rect x="30" y="36" width="640" height="190" rx="58" fill="#181c24" fill-opacity="0.52"/>
  <ellipse cx="195" cy="132" rx="60" ry="60" fill="#47e8d4" fill-opacity="0.02"/>
  <ellipse cx="500" cy="132" rx="62" ry="62" fill="#b0ffc4" fill-opacity="0.02"/>
  <circle cx="350" cy="132" r="44" fill="#fffa90" fill-opacity="0.02"/>
  <text x="52" y="175" fill="#7cf7e6" fill-opacity="0.03" font-size="120" font-family="monospace" font-weight="bold">₹</text>
  <text x="582" y="175" fill="#7cf7e6" fill-opacity="0.03" font-size="120" font-family="monospace" font-weight="bold">₹</text>
</svg>
"""
svg_url = f"data:image/svg+xml;utf8,{urllib.parse.quote(banknote_svg)}"
st.markdown(f"""
<style>
body, .stApp {{
    background-color: #14210d !important;
    background-image: url('{svg_url}');
    background-repeat: no-repeat;
    background-position: 50% 40%;
    background-size: 90vw auto;
    background-attachment: fixed;
}}
section.main, .block-container {{
    background: transparent !important;
    padding-top: 3rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}
.settings-column {{
    font-family: monospace;
    font-size: 14px;
    color: #bfbfbf;
    background: rgba(30,35,45,0.96) !important;
    text-align: center;
    box-sizing: border-box;
    padding-left: 0 !important;
    padding-right: 0 !important;
}}
.settings-header {{
    font-weight: bold;
    margin-bottom: 1rem;
    color: #c8e6fa;
}}
</style>
<style>
/* Preserve original page background by NOT overriding body or .stApp background here */

/* Input Text Box */
div[data-testid="stTextInput"] input, 
div[data-testid="stPassword"] input,
textarea {{
    background: #232539 !important;              /* Rich dark background */
    color: #e5ecf4 !important;                   /* High-contrast text */
    border: 1.5px solid #434752 !important;      /* Subtle border */
    border-radius: 8px !important;
    font-family: 'Fira Mono', monospace;         /* Modern readable font */
    font-size: 16px !important;
    box-shadow: 0 1px 7px 0 #070d1e33;           /* Soft shadow */
}}

div[data-testid="stTextInput"] input:focus, 
div[data-testid="stPassword"] input:focus,
textarea:focus {{
    border: 1.5px solid #7ab8ff !important;      /* Brighter border on focus */
    outline: none !important;
    background: #272b4b !important;
    color: #eef7fa !important;
}}

/* Placeholder text for visibility */
div[data-testid="stTextInput"] input::placeholder,
textarea::placeholder {{
    color: #9db3c2 !important;
    opacity: 0.92 !important;
}}

/* Button styling */
button[kind="secondary"], button[kind="primary"] {{
    background: #000000 !important;
    color: #d8e6ff !important;
    border: 1.5px solid #435086 !important;
    border-radius: 8px !important;
    font-weight: 600;
}}
button[kind="secondary"]:hover, button[kind="primary"]:hover {{
    background: #3856a6 !important;
    color: #eef7fa !important;
    border-color: #7ab8ff !important;
}}

</style>

""", unsafe_allow_html=True)



# --------- HEADER AND STYLES ---------
header_text = "FIFI: Financial Intelligence powered by Fi"
padding = 20
st.markdown(f"""
<style>
div.fifi-header {{
    font-family: monospace;
    font-size: 30px;
    white-space: nowrap;
    overflow: hidden;
    text-align: center;
    user-select: text;
    margin-bottom: 1rem;
    color: #bfbfff;
}}
.my-user {{
    background: #1976d2;
    color: white;
    border-radius: 12px;
    padding: 5px 10px;
    margin: 4px 0 6px auto;
    align-self: flex-end;
    max-width: 80%;
    width: fit-content;
    min-width: 20px;
    word-break: break-word;
    word-wrap: break-word;
    display: block;
    box-sizing: border-box;
}}
.my-bot {{
    background: #363947;
    color: #e0e0e3;
    border-radius: 12px;
    padding: 5px 10px;
    margin: 4px auto 6px 0;
    align-self: flex-start;
    max-width: 80%;
    width: fit-content;
    min-width: 20px;
    word-break: break-word;
    word-wrap: break-word;
    display: block;
    box-sizing: border-box;
}}
.scrollbox, .settings-column {{
    background: transparent !important;
}}
.settings-column {{
    font-family: monospace;
    font-size: 14px;
    color: #bfbfbf;
}}
.settings-header {{
    font-weight: bold; margin-bottom: 1rem;
    color: #c8e6fa;
}}
</style>
<div class="fifi-header">
    {'-' * padding} {header_text} {'-' * padding}
</div>
""", unsafe_allow_html=True)


st.set_page_config(layout="wide")


# ------------- LOGIN PAGE CONTROL -------------


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_failed" not in st.session_state:
    st.session_state.login_failed = False
if "login_attempted" not in st.session_state:
    st.session_state.login_attempted = False


def set_login_attempted():
    st.session_state.login_attempted = True


# --- Check for login attempt and handle authentication ---
if st.session_state.login_attempted:
    username = st.session_state.get("fifi_username", "")
    password = st.session_state.get("fifi_password", "")
    # Replace with your authentication logic!
    if username.strip() == "alok" and password.strip() == "chutya":
        st.session_state.logged_in = True
        st.session_state.login_failed = False
    else:
        st.session_state.logged_in = False
        st.session_state.login_failed = True
    st.session_state.login_attempted = False  # Reset after processing


if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align: center; margin-top: 7rem; margin-bottom: 2.5rem;'>
        <span style='font-size: 2.5rem; color: #bfbfff; font-family: monospace; font-weight: bold;'>Sign in 🔫</span>
    </div>
    <style>
    div[data-testid="stTextInput"], div[data-testid="stPassword"] {
        max-width:300px !important;
        margin-left:auto !important;
        margin-right:auto !important;
    }
    div[data-testid="stTextInput"] input, div[data-testid="stPassword"] input {
        max-width:300px !important;
    }
    div.login-btn-holder {
        text-align:center;
        margin-top:1rem;
    }
    button[kind="secondary"] {
        width:110px !important;
        margin-left:auto !important;
        margin-right:auto !important;
        display:block !important;
        font-weight:600;
    }
    </style>
    """, unsafe_allow_html=True)


    if st.session_state.login_failed:
        st.markdown(
            "<div style='color:#ff5959; background:rgba(40,0,0,0.2); "
            "border-radius:8px; padding:7px 0; text-align:center; "
            "font-weight:600;'>Incorrect username or password</div>",
            unsafe_allow_html=True
        )


    st.text_input("Username", key="fifi_username")
    st.text_input(
        "Password",
        type="password",
        key="fifi_password",
        on_change=set_login_attempted
    )


    st.markdown('<div class="login-btn-holder">', unsafe_allow_html=True)
    if st.button("Sign In", key="fifi_signin_btn"):
        set_login_attempted()
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()


# ---------- Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""
if "immersive_chart" in st.session_state:
    del st.session_state["immersive_chart"]


# ---------- Mock Data ----------
def get_financial_data():
    return {
        "net_worth": 45320,
        "monthly_spends": {
            "Jan": {"Shopping": 4500, "Food": 3000, "Bills": 2000, "Entertainment": 1200},
            "Feb": {"Shopping": 4000, "Food": 2800, "Bills": 2100, "Entertainment": 1300},
            "Mar": {"Shopping": 4800, "Food": 2900, "Bills": 1900, "Entertainment": 1500},
            "Apr": {"Shopping": 5000, "Food": 3100, "Bills": 1800, "Entertainment": 1350},
            "May": {"Shopping": 4700, "Food": 3000, "Bills": 2200, "Entertainment": 1600},
            "Jun": {"Shopping": 5200, "Food": 3200, "Bills": 2100, "Entertainment": 1400},
        }
    }
def classify_behavior(last_month_spends):
    total = sum(last_month_spends.values()) if last_month_spends else 1
    shopping_pct = last_month_spends.get("Shopping", 0) / total
    food_pct = last_month_spends.get("Food", 0) / total
    if shopping_pct > 0.4: return "Shopaholic"
    elif food_pct > 0.35: return "Foodie"
    elif total < 9000: return "Saver"
    else: return "Balanced"
def get_investment_data():
    best = [("S&P 500 ETF", 17.5), ("Gold", 12.2), ("Corporate Bonds", 8.9)]
    worst = [("Crypto Fund", -11.0), ("Emerging Markets", -4.5), ("Startups Fund", -1.2)]
    return best, worst
def get_credit_usage():
    return [("Jan", 8200), ("Feb", 7300), ("Mar", 9500), ("Apr", 9100), ("May", 8650), ("Jun", 9900)]


col_settings, col_insights, col_chat = st.columns([0.5, 6, 3], gap="large")


with col_settings:
    st.markdown('<div class="settings-column column-gap-right">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">Settings</div>', unsafe_allow_html=True)
    st.button("✅", help="Add/Remove connected banks/accounts")
    st.button("📤", help="Export Data")
    st.button("🔗", help="Connect budgeting or investment tools")
    st.button("🛡️", help="Manage data sharing and anonymization")
    st.markdown("---")
    if st.button("👋", help="Log out of your FiFi account"):
        st.session_state.logged_in = False
        st.session_state.chat_history.clear()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


data = get_financial_data()
net_worth = data["net_worth"]
monthly_spends = data["monthly_spends"]
df_spends = pd.DataFrame(monthly_spends).T
df_spends.index.name = "Month"
df_spends.fillna(0, inplace=True)
last_month = df_spends.index[-1]
behavior = classify_behavior(df_spends.loc[last_month].to_dict())


pie_colors = px.colors.sequential.Blues_r[:-2]
line_palette = px.colors.sequential.Blues_r + px.colors.sequential.Greens_r


with col_insights:
    st.markdown(f"<h2>💰 Net Worth: ₹{net_worth:,}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #82b1ff;'>📝 Your Behavior Summary: <em>{behavior}</em></h4>", unsafe_allow_html=True)
    st.markdown("---")


    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📊 Monthly Spend by Category")
        pie_data = df_spends.loc[last_month]
        fig_pie = px.pie(
            values=pie_data.values,
            names=pie_data.index,
            color_discrete_sequence=pie_colors,
            height=270,
            width=350,
            template="plotly_dark"
        )
        fig_pie.update_traces(textinfo="label+percent", pull=[0.07]*len(pie_data), textfont_size=14)
        fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Behavioral spending categories and hover descriptions
        categories = [
            "Essentials",
            "Upskill/Education",
            "Impulse",
            "Savings",
            "Lifestyle & Leisure",
            "Debt Repayment"
        ]

        hover_texts = [
            "Everyday necessities like rent, groceries, utilities, transport, healthcare",
            "Expenses for self-improvement, courses, books, certifications, workshops",
            "Unplanned, spur-of-the-moment purchases influenced by emotions or promotions",
            "Money set aside for future needs, emergencies, or financial growth",
            "Entertainment, hobbies, travel, dining out, streaming services",
            "Payments towards loans, credit cards, mortgages, or borrowed funds"
        ]

        # Generate mock values for demonstration (replace with real data as needed)
        np.random.seed(42)
        spend_values = np.random.randint(1_000, 10_000, size=len(categories))

        # Radar charts require closed loops, so repeat first value/category for closure.
        categories_closed = categories + [categories[0]]
        values_closed = np.append(spend_values, spend_values[0])
        hover_texts_closed = hover_texts + [hover_texts[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            hoverinfo='text',
            text=hover_texts_closed,
            name='Spending Behavior'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values_closed) * 1.2]
                )
            ),
            showlegend=False,
            template="plotly_dark",
            height=270,
            width=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        st.markdown("##### 🕸️ Spending Behavior Classification")
        st.plotly_chart(fig, use_container_width=True)


    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### 📈 Monthly Spending Trends")
        fig_line = go.Figure()
        for i, col in enumerate(df_spends.columns):
            fig_line.add_trace(go.Scatter(
                x=df_spends.index, y=df_spends[col], mode='lines+markers',
                name=col,
                line=dict(color=line_palette[i % len(line_palette)], width=3),
                marker=dict(color=line_palette[i % len(line_palette)], size=9)
            ))
        fig_line.update_layout(
            template="plotly_dark",
            height=220, width=350, xaxis_title="Month", yaxis_title="Spend (₹)",
            legend_title_text='Category',
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_line, use_container_width=True)


    with col4:
        st.markdown("##### 💳 Credit Usage Till Date")
        months, usage = zip(*get_credit_usage())
        df_credit = pd.DataFrame({"Month": months, "Credit Usage (₹)": usage})
        fig_credit = px.bar(
            df_credit, x="Month", y="Credit Usage (₹)",
            height=220, width=350,
            color="Credit Usage (₹)", color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig_credit.update_traces(marker_line_color='#eef6fa', marker_line_width=1.2)
        fig_credit.update_layout(
            margin=dict(l=30, r=10, t=10, b=0), showlegend=False
        )
        st.plotly_chart(fig_credit, use_container_width=True)


    col5, col6 = st.columns(2)
    best, worst = get_investment_data()
    with col5:
        st.markdown("##### 📉 Top 3 Worst Investments")
        df_worst = pd.DataFrame(worst, columns=["Investment", "Return (%)"]).sort_values("Return (%)")
        fig_worst = px.bar(
            df_worst, x="Return (%)", y="Investment", orientation='h',
            color="Return (%)", color_continuous_scale="reds",
            height=130, width=220, range_x=[min(df_worst["Return (%)"]) * 1.15, 0],
            template="plotly_dark"
        )
        fig_worst.update_layout(
            margin=dict(l=10, r=10, t=20, b=20), coloraxis_showscale=False
        )
        st.plotly_chart(fig_worst, use_container_width=True)
    with col6:
        st.markdown("##### 📈 Top 3 Best Investments")
        df_best = pd.DataFrame(best, columns=["Investment", "Return (%)"]).sort_values("Return (%)")
        fig_best = px.bar(
            df_best, x="Return (%)", y="Investment", orientation='h',
            color="Return (%)", color_continuous_scale="greens",
            height=130, width=220, range_x=[0, max(df_best["Return (%)"]) * 1.15],
            template="plotly_dark"
        )
        fig_best.update_layout(
            margin=dict(l=10, r=10, t=20, b=20), coloraxis_showscale=False
        )
        st.plotly_chart(fig_best, use_container_width=True)


with col_chat:
    st.markdown('<div class="column-gap-left">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><h2>💬 Chat with FiFi</h2></div>', unsafe_allow_html=True)

    prompts = ["How did I spend this weekend?", "Show me top expenses", "Suggest a saving goal"]
    prompt_cols = st.columns(len(prompts))
    for i, prompt in enumerate(prompts):
        with prompt_cols[i]:
            if st.button(prompt, key=f"prompt_{i}"):
                st.session_state.chat_history.append({"role": "user", "message": prompt})
                st.session_state.chat_history.append({"role": "bot", "message": f"Placeholder response to: '{prompt}'"})
    chat_html = '<div class="scrollbox">'
    for msg in st.session_state.chat_history[-7:]:
        if msg["role"] == "user":
            chat_html += f'<div class="my-user">{msg["message"]}</div>'
        else:
            chat_html += f'<div class="my-bot">{msg["message"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    def handle_enter():
        text = st.session_state.chat_input.strip()
        if text:
            st.session_state.chat_history.append({"role": "user", "message": text})
            st.session_state.chat_history.append({"role": "bot", "message": f"FiFi says: Placeholder response to: '{text}'"})
        st.session_state.chat_input = ""
    st.text_input(
        "Type your message:",
        key="chat_input",
        placeholder="Ask something...",
        label_visibility="collapsed",
        on_change=handle_enter
    )
    st.markdown('</div>', unsafe_allow_html=True)

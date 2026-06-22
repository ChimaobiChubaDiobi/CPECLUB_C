import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3

# Database setup
DB_PATH = "virtual_matches.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            league TEXT,
            home_team TEXT,
            away_team TEXT,
            home_goals INTEGER,
            away_goals INTEGER,
            result TEXT,
            over_15 BOOLEAN,
            over_25 BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

init_db()

# Load data
def load_data():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM matches ORDER BY timestamp DESC", conn)
    conn.close()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Save match
def save_match(data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO matches 
        (timestamp, league, home_team, away_team, home_goals, away_goals, result, over_15, over_25)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        data['league'],
        data['home_team'],
        data['away_team'],
        data['home_goals'],
        data['away_goals'],
        data['result'],
        data['over_15'],
        data['over_25']
    ))
    conn.commit()
    conn.close()

# ====================== STREAMLIT APP ======================
st.set_page_config(page_title="SportyBet Virtuals Analyzer", layout="wide")
st.title("🏆 SportyBet Virtuals Analyzer")
st.markdown("Track • Analyze • Apply Strategies for SportyBet Virtual Matches")

df = load_data()

# Sidebar - Match Entry Form
with st.sidebar:
    st.header("📝 Log New Match")
    league = st.text_input("League", value="Virtual Premier League")
    home_team = st.text_input("Home Team")
    away_team = st.text_input("Away Team")
    
    col1, col2 = st.columns(2)
    with col1:
        home_goals = st.number_input("Home Goals", min_value=0, value=1, step=1)
    with col2:
        away_goals = st.number_input("Away Goals", min_value=0, value=1, step=1)
    
    if st.button("💾 Save Match", type="primary"):
        if home_team.strip() and away_team.strip():
            result = "Home" if home_goals > away_goals else "Away" if away_goals > home_goals else "Draw"
            over_15 = (home_goals + away_goals) > 1
            over_25 = (home_goals + away_goals) > 2
            
            match_data = {
                "league": league,
                "home_team": home_team.strip(),
                "away_team": away_team.strip(),
                "home_goals": int(home_goals),
                "away_goals": int(away_goals),
                "result": result,
                "over_15": over_15,
                "over_25": over_25
            }
            save_match(match_data)
            st.success("✅ Match saved successfully!")
            st.rerun()
        else:
            st.error("Please enter both team names")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Match History", "🎯 Strategies"])

with tab1:
    st.header("Overall Statistics")
    if not df.empty:
        total = len(df)
        draw_rate = (df['result'] == 'Draw').mean() * 100
        over15_rate = df['over_15'].mean() * 100
        over25_rate = df['over_25'].mean() * 100
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Matches", total)
        col2.metric("Draw Rate", f"{draw_rate:.1f}%")
        col3.metric("Over 1.5 Rate", f"{over15_rate:.1f}%")
        col4.metric("Over 2.5 Rate", f"{over25_rate:.1f}%")
        st.subheader("Results Distribution")
        fig1 = px.pie(df, names='result', title="Match Outcomes", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig1, use_container_width=True)
        
        st.subheader("Goals Distribution")
        goals_df = pd.melt(df, value_vars=['home_goals', 'away_goals'], var_name='Side', value_name='Goals')
        fig2 = px.histogram(goals_df, x='Goals', color='Side', barmode='group', title="Home vs Away Goals")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No matches logged yet. Use the sidebar to start tracking!")

with tab2:
    st.header("Match History")
    if not df.empty:
        display_df = df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "virtual_matches_history.csv", "text/csv")
    else:
        st.info("No matches recorded yet.")

with tab3:
    st.header("🎯 Strategy Recommendations")
    if not df.empty and len(df) >= 5:
        st.subheader("Draw After Non-Draw Streak")
        streak = 0
        recs = []
        for _, row in df.iterrows():
            if row['result'] != 'Draw':
                streak += 1
            else:
                if streak >= 4:
                    recs.append(f"Strong Draw Signal after {streak} non-draws → {row['home_team']} vs {row['away_team']}")
                streak = 0
        if recs:
            for r in recs[-3:]:
                st.success(r)
        else:
            st.info("No strong draw streaks detected yet.")
        
        st.subheader("Over 1.5 Goals Strategy")
        low_streak = 0
        for _, row in df.iterrows():
            if not row['over_15']:
                low_streak += 1
            else:
                if low_streak >= 3:
                    st.info(f"Over 1.5 recommended after {low_streak} low-scoring games")
                low_streak = 0
    else:
        st.info("Log at least 5 matches to see intelligent strategy suggestions.")

st.caption("⚠️ Disclaimer: Virtual matches are RNG-based. This tool helps with statistical tracking and common community strategies only. No guarantee of wins. Gamble responsibly.")
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3
import math

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

# Prediction Engine
def calculate_xg(df, home_team, away_team):
    overall_avg_scored = (df['home_goals'].mean() + df['away_goals'].mean()) / 2 if not df.empty else 1.5
    
    teamA_home = df[df['home_team'] == home_team]
    teamB_away = df[df['away_team'] == away_team]
    
    home_scored = teamA_home['home_goals'].mean() if not teamA_home.empty else overall_avg_scored
    home_conceded = teamA_home['away_goals'].mean() if not teamA_home.empty else overall_avg_scored
    
    away_scored = teamB_away['away_goals'].mean() if not teamB_away.empty else overall_avg_scored
    away_conceded = teamB_away['home_goals'].mean() if not teamB_away.empty else overall_avg_scored
    
    home_xg = (home_scored + away_conceded) / 2
    away_xg = (away_scored + home_conceded) / 2
    
    if pd.isna(home_xg): home_xg = 1.5
    if pd.isna(away_xg): away_xg = 1.5
        
    return home_xg, away_xg

def poisson_probability(k, lmbda):
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

def predict_match(home_xg, away_xg):
    max_goals = 5
    probs = {'Home': 0, 'Draw': 0, 'Away': 0, 'Over 1.5': 0, 'Under 1.5': 0, 'Over 2.5': 0, 'Under 2.5': 0}
    cs_probs = {}
    
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            prob = poisson_probability(h, home_xg) * poisson_probability(a, away_xg)
            cs_probs[f"{h}-{a}"] = prob
            
            if h > a: probs['Home'] += prob
            elif h == a: probs['Draw'] += prob
            else: probs['Away'] += prob
                
            total_goals = h + a
            if total_goals > 1.5: probs['Over 1.5'] += prob
            else: probs['Under 1.5'] += prob
                
            if total_goals > 2.5: probs['Over 2.5'] += prob
            else: probs['Under 2.5'] += prob
                
    total_1x2 = probs['Home'] + probs['Draw'] + probs['Away']
    if total_1x2 > 0:
        probs['Home'] /= total_1x2
        probs['Draw'] /= total_1x2
        probs['Away'] /= total_1x2
        
    total_15 = probs['Over 1.5'] + probs['Under 1.5']
    if total_15 > 0:
        probs['Over 1.5'] /= total_15
        probs['Under 1.5'] /= total_15
        
    total_25 = probs['Over 2.5'] + probs['Under 2.5']
    if total_25 > 0:
        probs['Over 2.5'] /= total_25
        probs['Under 2.5'] /= total_25
        
    total_cs = sum(cs_probs.values())
    if total_cs > 0:
        for k in cs_probs:
            cs_probs[k] /= total_cs
            
    # Get top 5 correct scores
    top_cs = dict(sorted(cs_probs.items(), key=lambda item: item[1], reverse=True)[:5])
        
    return probs, top_cs

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
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔮 Predictor", "📋 Match History", "🎯 Strategies"])

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
    st.header("🔮 Match Predictor")
    st.markdown("Select two teams to predict the statistical outcome based on historical data.")
    
    all_teams = []
    if not df.empty:
        all_teams = sorted(list(set(df['home_team'].tolist() + df['away_team'].tolist())))
    
    col1, col2 = st.columns(2)
    with col1:
        pred_home = st.selectbox("Home Team", options=all_teams, key="phome_sel") if all_teams else st.text_input("Home Team", key="phome")
    with col2:
        pred_away = st.selectbox("Away Team", options=all_teams, index=min(1, len(all_teams)-1), key="paway_sel") if all_teams else st.text_input("Away Team", key="paway")
        
    st.markdown("---")
    st.subheader("💰 Bookmaker Odds (Optional for Value Bets)")
    col_o1, col_o2, col_o3 = st.columns(3)
    odds_home = col_o1.number_input("Home Win Odds", min_value=1.0, value=1.0, step=0.1)
    odds_draw = col_o2.number_input("Draw Odds", min_value=1.0, value=1.0, step=0.1)
    odds_away = col_o3.number_input("Away Win Odds", min_value=1.0, value=1.0, step=0.1)

    col_o4, col_o5 = st.columns(2)
    odds_over15 = col_o4.number_input("Over 1.5 Odds", min_value=1.0, value=1.0, step=0.1)
    odds_over25 = col_o5.number_input("Over 2.5 Odds", min_value=1.0, value=1.0, step=0.1)

    if st.button("Calculate Predictions", type="primary", use_container_width=True):
        if pred_home and pred_away:
            if pred_home == pred_away:
                st.warning("Please select two different teams.")
            else:
                home_xg, away_xg = calculate_xg(df, pred_home, pred_away)
                probs, top_cs = predict_match(home_xg, away_xg)
                
                st.subheader("📈 Statistical Prediction Models")
                
                st.markdown("#### Match Winner (1X2)")
                col_w1, col_w2, col_w3 = st.columns(3)
                col_w1.metric("Home Win", f"{probs['Home']*100:.1f}%")
                col_w2.metric("Draw", f"{probs['Draw']*100:.1f}%")
                col_w3.metric("Away Win", f"{probs['Away']*100:.1f}%")
                
                st.markdown("#### Goals Market")
                col_g1, col_g2, col_g3, col_g4 = st.columns(4)
                col_g1.metric("Over 1.5", f"{probs['Over 1.5']*100:.1f}%")
                col_g2.metric("Under 1.5", f"{probs['Under 1.5']*100:.1f}%")
                col_g3.metric("Over 2.5", f"{probs['Over 2.5']*100:.1f}%")
                col_g4.metric("Under 2.5", f"{probs['Under 2.5']*100:.1f}%")
                
                st.markdown("#### Top 3 Most Likely Correct Scores")
                cs_cols = st.columns(3)
                cs_keys = list(top_cs.keys())
                for i in range(min(3, len(cs_keys))):
                    cs_cols[i].metric(f"Score: {cs_keys[i]}", f"{top_cs[cs_keys[i]]*100:.1f}%")
                
                st.markdown("---")
                st.subheader("🎯 Recommended Betting Options")
                
                options = []
                
                # Check for value bets if odds were provided
                provided_odds = {
                    'Home': odds_home, 'Draw': odds_draw, 'Away': odds_away,
                    'Over 1.5': odds_over15, 'Over 2.5': odds_over25
                }
                
                has_custom_odds = any(o > 1.0 for o in provided_odds.values())
                
                if has_custom_odds:
                    st.markdown("**Value Bets found based on your Odds Input (Expected Value > 0):**")
                    for market, odd in provided_odds.items():
                        if odd > 1.0:
                            ev = (probs[market] * odd) - 1
                            if ev > 0.05: # more than 5% edge
                                options.append(f"✅ **{market}** @ {odd} (Edge: +{ev*100:.1f}%) - *Strong Value*")
                            elif ev > 0:
                                options.append(f"☑️ **{market}** @ {odd} (Edge: +{ev*100:.1f}%) - *Slight Value*")
                
                if not options:
                    if has_custom_odds:
                        st.info("No value bets found based on the provided odds.")
                    
                    st.markdown("**Safe Options based on Statistical Probability:**")
                    
                    for market, prob in probs.items():
                        if 'Under' not in market and prob > 0.55:
                            options.append(f"📊 **{market}** (Probability: {prob*100:.1f}%)")
                            
                    # Always show top correct score as an option
                    top_score = cs_keys[0]
                    top_score_prob = top_cs[top_score]
                    options.append(f"🎯 **Correct Score {top_score}** (Probability: {top_score_prob*100:.1f}%)")

                for opt in options:
                    st.success(opt)
        else:
            st.error("Please provide both teams.")

with tab3:
    st.header("Match History")
    if not df.empty:
        display_df = df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "virtual_matches_history.csv", "text/csv")
    else:
        st.info("No matches recorded yet.")

with tab4:
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
import random
import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import model modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.q_learning import BattingRL
from model.game_theory import get_nash_equilibrium

# Load IPL data
df = pd.read_csv('../data/ipl_ball_by_ball.csv')

st.set_page_config(page_title="Cricket Strategy Optimiser", layout="wide")
st.title("🏏 Cricket Strategy Optimiser")

# Player selection (standard panel)
players = df['Batter'].unique()
bowlers = df['Bowler'].unique()

player = st.selectbox("Select Batsman", players)
opponent = st.selectbox("Select Bowler", bowlers)

# Q-learning model
rl_model = BattingRL()
state = (hash(player) + hash(opponent)) % 100
strategy = rl_model.recommend(state)

st.markdown(f"###  Recommended Batting Strategy: **{strategy}**")

# Game Theory Payoff Matrix
bowler_labels, batsman_labels, payoff_matrix, equilibria = get_nash_equilibrium(player, opponent)
st.markdown("###  Game Theory Payoff Matrix (Bowler's Perspective)")
payoff_df = pd.DataFrame(payoff_matrix, index=bowler_labels, columns=batsman_labels)
st.dataframe(payoff_df.style.background_gradient(cmap='Blues'), use_container_width=True)

# Game Theory Result
st.markdown("###  Nash Equilibrium Strategy Mixes")
if equilibria:
    for eq in equilibria:
        st.write("**Bowler Strategy Mix:**")
        for i, prob in enumerate(eq[0]):
            st.write(f"- {bowler_labels[i]}: {round(prob, 2)}")
        st.write("**Batsman Strategy Mix:**")
        for j, prob in enumerate(eq[1]):
            st.write(f"- {batsman_labels[j]}: {round(prob, 2)}")
else:
    st.warning("No Nash Equilibrium found.")

# ------------------------------------------
# 🎮 Real Match Simulation Mode (Ball-by-Ball)
# ------------------------------------------
st.markdown("---")
st.subheader("🏏 Full Match Simulation (Ball-by-Ball AI Strategies)")

# Filter to one match (first match in dataset)
match_id = df['Match ID'].unique()[0]
match_data = df[df['Match ID'] == match_id].reset_index(drop=True)

# Setup session state to track match
if "ball_index" not in st.session_state:
    st.session_state.ball_index = 0
if "runs" not in st.session_state:
    st.session_state.runs = 0
if "wickets" not in st.session_state:
    st.session_state.wickets = 0

# Simulate one delivery at a time
if st.button("▶️ Simulate Next Ball"):
    if st.session_state.ball_index < len(match_data):
        ball = match_data.iloc[st.session_state.ball_index]

        # Show match details
        st.markdown(f"**Over:** {ball['Over']}.{ball['Ball']}")
        st.markdown(f"**Batsman:** {ball['Batter']}  |  **Bowler:** {ball['Bowler']}")
        st.markdown(f"**Runs Scored:** {ball['Batter Runs']}")

        # Update match state
        st.session_state.runs += ball['Batter Runs']
        if pd.notna(ball.get('dismissal_kind')) and ball['dismissal_kind'] != 'retired hurt':
            st.session_state.wickets += 1
        st.markdown(f"**Live Score:** {st.session_state.runs}/{st.session_state.wickets}")

        # AI Batting Strategy (Q-Learning)
        state = (int(ball['Over']) + hash(ball['Batter']) + hash(ball['Bowler'])) % 100
        ai_strategy = rl_model.recommend(state)
        st.markdown(f"🧠 **Recommended Batting Strategy:** {ai_strategy}")

        # Game Theory Strategy (Nash Equilibrium)
        b_labels, bt_labels, p_matrix, eqs = get_nash_equilibrium(ball['Batter'], ball['Bowler'])
        sim_df = pd.DataFrame(p_matrix, index=b_labels, columns=bt_labels)
        st.markdown(" **Payoff Matrix (This Ball):**")
        st.dataframe(sim_df.style.background_gradient(cmap='YlOrBr'))

        if eqs:
            st.markdown(" **Nash Equilibrium for This Ball:**")
            for eq in eqs:
                st.write("**Bowler Strategy Mix:**")
                for i, prob in enumerate(eq[0]):
                    st.write(f"- {b_labels[i]}: {round(prob, 2)}")
                st.write("**Batsman Strategy Mix:**")
                for j, prob in enumerate(eq[1]):
                    st.write(f"- {bt_labels[j]}: {round(prob, 2)}")
        else:
            st.warning("No equilibrium found for this ball.")

        # Move to next ball
        st.session_state.ball_index += 1
    else:
        st.success(" Match Simulation Complete!")

import streamlit as st
import mysql.connector

st.set_page_config(page_title="Spiderman Info", layout="centered")
st.title("🕷️ Spidey Database")

# ------ SAME CONNECTION INFO YOU'LL USE IN BOTH FILES ------
HOST = "127.0.0.1"   # local MySQL, you could also type “localhost”
PORT = 3306          # use 3307 if you installed a second instance
DB   = "spiderman_multiverse_db"     # <- puppy sample database
USER = "root"        # or 'class_admin'
PWD  = "Cachito2002"  # or change to your local password

def run_query(sql, params=()):
    conn = mysql.connector.connect(host=HOST, port=PORT, user=USER, password=PWD, database=DB)
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

# ------ 1.(Spiderman Function (Info))
SQL = """
SELECT UPPER(name) AS Full_Name, UPPER(s_identity) AS Secret_Identity
FROM Spiderman
WHERE name LIKE %s OR s_identity LIKE %s;
;
"""
name = st.text_input("Spiderman Name Contains (e.g., Peter)", value="", key="input_spiderman")
if st.button("Search Spidey", key="btn_spiderman"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,search_term))

        st.dataframe(rows if rows else [{"Spiderman": "Spidey Not Found"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query



# ------ 2.(INNER JOIN QUERY -> Epic Battle/Spiderman/Villains)
SQL = """
SELECT 
	s.name AS Civilian_Name,
    s.s_identity AS Spiderman,
    v.name AS Villain,
    epic.date AS Date
FROM
	Spiderman s
INNER JOIN EpicBattles epic
ON epic.spiderman_id = s.spiderman_id
INNER JOIN Villains v
ON epic.villain_id = v.villain_id
WHERE v.name LIKE %s OR s.name LIKE %s OR epic.outcome LIKE %s
ORDER BY epic.date;
"""

name = st.text_input("Battle Contains (e.g., goblin)", value="")
if st.button("Battle Info"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,search_term,search_term))

        st.dataframe(rows if rows else [{"info": "No Battle Info found"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query


# ------ 3.(Subquery Deathy Battles)
SQL = """
WITH FilteredBattles AS (
	SELECT
		epic.villain_id,
		epic.spiderman_id,
        epic.outcome,
        epic.details AS Event,
        v.name AS Villain
	FROM EpicBattles epic
    INNER JOIN Villains v
    ON epic.villain_id = v.villain_id
    WHERE epic.outcome LIKE %s
)
SELECT 
	s.name AS Civilian_Name,
    s.s_identity AS Spiderman,
    fb.Villain,
    fb.outcome,
    fb.Event
FROM
	Spiderman s
INNER JOIN FilteredBattles fb
ON fb.spiderman_id = s.spiderman_id;
"""
name = st.text_input("Battle Outcome (e.g., Death)", value="")
if st.button("Search Battle Outcome", key="btn_cte_search"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,))

        st.dataframe(rows if rows else [{"Battle Info": "No battle with death found"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query

# ------ 4.(Suit Case/When Query)
SQL = """
SELECT 
	su.name AS Suit, 
    su.abilities_granted AS Abilities,
    su.price AS Suit_Value,
    su.power_level AS Power,
    CASE
		WHEN su.power_level < 3 THEN 'Weak Suit'
        WHEN su.power_level >= 5 THEN 'Powerful Suit'
        ELSE 'Regular Suit'
	END AS Suits_Power
FROM Suits su
WHERE su.name LIKE %s
ORDER BY su.power_level DESC;
"""
name = st.text_input("Spiderman Suits (e.g., Superior Suit)", value="")
if st.button("Search Battle Suits", key="btn_suit_search"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,))

        st.dataframe(rows if rows else [{"Suit Info": "No Suit Found"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query

# ----> 5. Universes LEFT join (OUTER JOIN)
SQL_ALL_UNIVERSES = """
SELECT m.name AS Multiverse, s.name AS Spiderman
FROM Multiverse m
LEFT JOIN Spiderman s
ON s.universe_id = m.universe_id;
"""
SQL_ALL_NULL_UNIVERSES = """
SELECT m.name AS Multiverse, s.name AS Spiderman
FROM Multiverse m
LEFT JOIN Spiderman s
ON s.universe_id = m.universe_id
WHERE s.spiderman_id IS NULL;
"""
# name = st.text_input("The Multiverses (e.g., Earth 616)", value="")

filter_choice = st.selectbox(
    "Select Universe View:",
    options=['Show All Universes', 'Show Only Empty Universes'],
    key="filter_multiverse"
)
if st.button("Multiverse Option", key="btn_universe_search"):
    try:
        if filter_choice == 'Show Only Empty Universes':
            selected_sql = SQL_ALL_NULL_UNIVERSES
        else:
            selected_sql = SQL_ALL_UNIVERSES

        search_term = f"%{name.strip()}%"

        rows = run_query(selected_sql, ())

        st.dataframe(rows if rows else [{"Universe": "Universe is not found"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query


# --- 6.Aggregate Function
SQL_VILLAIN_TEAM = """
SELECT org.team_name, COUNT(v.name) AS Villain_in_team
FROM organization org
INNER JOIN Villains v
ON v.organization_id = org.organization_id
GROUP BY org.team_name;
"""

SQL_SPIDEY_TEAM = """
SELECT org.team_name, COUNT(s.name) AS Spidey_in_team
FROM organization org
INNER JOIN Spiderman s
ON s.organization_id = org.organization_id
GROUP BY org.team_name;
"""
# name = st.text_input("Organization - Teams (e.g., Sinister Six)", value="")

filter_choice = st.selectbox(
    "Select Spidey or Villain Teams:",
    options=['Show Villain Teams', 'Show Spidey Teams'],
    key="filter_teams"
)
if st.button("Team Option", key="btn_team_search"):
    try:
        if filter_choice == 'Show Villain Teams':
            sql_selected = SQL_VILLAIN_TEAM
        else:
            sql_selected = SQL_SPIDEY_TEAM


        search_term = f"%{name.strip()}%"

        rows = run_query(sql_selected, ())

        st.dataframe(rows if rows else [{"Team": "Nobody is associated to that team"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query


# --- 7.Aggregate Function
SQL = """
SELECT 
	s.name AS Spidey,
    v.name AS Villain,
    ROW_NUMBER () OVER (
    PARTITION BY v.villain_id
    ORDER BY s.spiderman_id
    ) AS spidey_to_villain
FROM EpicBattles epic
JOIN Villains v
ON epic.villain_id = v.villain_id
JOIN Spiderman s
ON epic.spiderman_id = s.spiderman_id
WHERE s.name LIKE %s OR v.name LIKE %s;
"""

name = st.text_input("Villain to Spidey Ratio (e.g., spidey...villain)", value="")
if st.button("Comparison"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,search_term))

        st.dataframe(rows if rows else [{"Ratio": "At his moment that is not available"}])
    except Exception as e:
        st.error(str(e))
# ------End of Query

# --- 8.Other Tables that I have
SQL = """
SELECT  
    po.origin AS Origin_of_Power, 
    po.details AS Origin_Details, 
    ct.creature AS Creature, 
    a.name AS Ability, 
    a.strength AS Power, 
    a.details AS Details
FROM CreatureTypes ct
RIGHT JOIN PowerOrigins po
ON ct.power_source_id = po.power_source_id
LEFT JOIN Abilities a
ON ct.ability_id = a.ability_id
WHERE po.origin LIKE %s OR po.details LIKE %s OR ct.creature LIKE %s;
"""

name = st.text_input("Ability/Details (e.g., spider)", value="")
if st.button("Origin"):
    try:
        search_term = f"%{name.strip()}%"

        rows = run_query(SQL, (search_term,search_term,search_term))

        st.dataframe(rows if rows else [{"Creature/Event": "At his moment that is not available"}])
    except Exception as e:
        st.error(str(e))


# ------End of Query



# streamlit run spidey_app.py 
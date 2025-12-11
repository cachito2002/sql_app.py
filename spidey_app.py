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

# ------(Spiderman Function (Info))
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



# ------(INNER JOIN QUERY -> Epic Battle/Spiderman/Villains)
SQL = """
SELECT 
	s.name AS Civilian_Name,
    s.s_identity AS Spiderman,
    v.name AS Villain,
    epic.date AS Date,
    epic.outcome AS Result,
    epic.details AS Details
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





# streamlit run spidey_app.py 
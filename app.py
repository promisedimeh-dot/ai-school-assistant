import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI School Assistant", page_icon="🎓")
st.title("🎓 AI School Assistant")
st.caption("Ask me anything about your class timetable, schedule, or lecturers!")

# ── Groq client ───────────────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ── Timetable data ────────────────────────────────────────────────────────────
TIMETABLE = """
CLASS TIMETABLE – HND I Computer Science (AI Option), Auchi Polytechnic
All classes hold in Room 3.4 unless stated otherwise.

MONDAY
  8:00 – 9:30    | Natural Language Processing          | Mr Ahmed        | Room 3.4
  9:30 – 11:00   | Computer Vision                      | Mr Ford         | Room 3.4
  11:00 – 12:30  | Neural Computation & Bioinformation  | Mr Jimoh        | Room 3.4
  12:30 – 2:00   | FREE PERIOD

TUESDAY
  8:00 – 9:30    | Research Methodology in A.I          | Mr Yeremiah     | Room 3.4
  9:30 – 11:00   | Machine Learning                     | Mr Abdulazeeh   | Room 3.4
  11:00 – 12:30  | Computer Vision (Practical)          | Mrs Edhonghon   | Room 3.4
  12:30 – 2:00   | FREE PERIOD

WEDNESDAY
  8:00 – 9:30    | A.I Framework and Development        | Mr Momodu       | Room 3.4
  9:30 – 11:00   | Neural Computation & Bioinformation  | Mr Ukolo        | Room 3.4
  11:00 – 12:30  | A.I Framework and Development (Practical) | Mr Umoru   | Room 3.4
  12:30 – 2:00   | Data Science for A.I (Practical)     | Mr Okudowa      | Room 3.4

THURSDAY
  8:00 – 9:30    | Data Science for A.I                 | Mr Musa         | Room 3.4
  9:30 – 11:00   | Machine Learning (Practical)         | Mr Sado         | Room 3.4
  11:00 – 12:30  | Use of English                       | Mrs Imode       | Lecture Theater
  12:30 – 2:00   | FREE PERIOD

FRIDAY
  8:00 – 12:00   | MSQ                                  | Mr Michael      | Room 3.4
"""

SYSTEM_PROMPT = f"""
You are a helpful and friendly school assistant chatbot for HND I Computer Science (AI Option) students at Auchi Polytechnic, Auchi.

Your main job is to answer questions about the class timetable and schedule. You can tell students:
- What class is happening at a specific time and day
- Who the lecturer is for a particular course
- What venue a class holds
- What courses are on a particular day
- When a student has free periods

Here is the full timetable:

{TIMETABLE}

Be friendly, clear, and concise. Always respond in a warm, student-friendly tone.
"""

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display chat history ──────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Handle input ──────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about your timetable or schedule..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

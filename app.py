import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from datetime import datetime
import PyPDF2
from docx import Document

from openai import OpenAI
import os


client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)


# Load embedding model

def load_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )
model = load_model()

st.set_page_config(
    page_title="PolyU Academic Advising Assistant",
    page_icon="🎓",
    layout="wide"
)





st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F3F4F6;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E5E7EB;
    }

    /* Buttons */
    .stButton > button {
        background-color: #A6192E;
        color: white;
        border: none;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #8A1526;
        color: white;
    }

    /* Text input */
    .stTextInput input {
        background-color: white;
    }

    /* Upload boxes */
    [data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stApp {
        background-color: #F3F4F6;
        background-repeat: no-repeat;
        background-position: center;
        background-size: 500px
        }

    </style>
    """,
    unsafe_allow_html=True
)



col1, col2 = st.columns([1.2, 8.2])

with col1:
    st.markdown("<div style='margin-top:40px'></div>",
                unsafe_allow_html=True)

    st.image(
        "logo.png",
        width=140
    )

with col2:
    st.markdown("""
    <div style="padding-top: 25px;">
        <h1 style="margin-bottom:0;">
            PolyU Academic Advising Assistant
        </h1>
        <p style="color:gray;">
            Helping you navigate your academic journey at PolyU.
        </p>
    </div>
    """, unsafe_allow_html=True)

    

st.markdown("""
<div style="
background-color:white;
padding:20px;
border-left:6px solid #A6192E;
border-radius:8px;
margin-bottom:25px;
box-shadow:0 2px 4px rgba(0,0,0,0.08);
">

<h4 style="margin-top:0;">
👋 Welcome to Polly
</h4>

<p>
I'm your virtual academic advisor for PolyU students.
</p>

<p><b>I can help with:</b></p>

<ul>
<li>Subject Registration</li>
<li>GPA and Academic Performance</li>
<li>Work-Integrated Education (WIE)</li>
<li>Exchange Programmes</li>
<li>Graduation Requirements</li>
<li>Academic Regulations</li>
</ul>

</div>
""", unsafe_allow_html=True)





if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []


st.sidebar.title("Conversation History")
if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []
    st.session_state.messages = []
    if "selected_chat" in st.session_state:
        del st.session_state["selected_chat"]












st.markdown("### 📄 Supporting Documents")




uploaded_file = st.file_uploader(
    "Upload PDF, DOCX or TXT",
    type=["pdf", "docx", "txt"]
)


uploaded_text = ""

if uploaded_file is not None:
    

    # TXT
    if uploaded_file.type == "text/plain":

        uploaded_text = uploaded_file.read().decode("utf-8")

    # PDF
    elif uploaded_file.type == "application/pdf":

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                uploaded_text += page_text + "\n"
            if len(uploaded_text) > 2000:
                break

    # DOCX
    elif "wordprocessingml.document" in uploaded_file.type:

        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            uploaded_text += para.text + "\n"

    st.success(
        f"📄 Uploaded: {uploaded_file.name}"
    )




with st.form("question_form"):

    question = st.text_input(
        "Ask Polly anything...",
        placeholder="e.g. What is academic integrity?"
    )

    submit = st.form_submit_button(
        "Send"
    )






# process the question

if submit and question.strip():
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    # Load Knowledge Base
    with open(
        "output/polyu_kb.txt",
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()

    # Create chunks
    chunk_size = 2000

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

        

    # Load FAISS index
    index = faiss.read_index(
        "vector_db/polyu.index"
    )
    

    # Create query embedding
    query_embedding = model.encode(
        [question]
    )

    # Search top 3 chunks
    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        k=3
    )
    top_distance = float(distances[0][0])



    confidence = max(
        60,
        min(
            95,
            int(100 - top_distance * 20)
        )
    )
    # Build context

    context = ""

    # PolyU knowledge base
    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            context += chunks[idx]
            context += "\n\n"

    # Uploaded document
    if uploaded_text:
        context += "\n\n=== Uploaded Document ===\n\n"
        context += uploaded_text[:1000]




    
    # Create prompt
    prompt = f"""
    You are Polly, a friendly and helpful PolyU Academic Advisor for PolyU students.

    Your role is to assist students by answering their questions clearly, politely and professionally.

    Guidelines:
    -Use a warm and encouraging tone.
    -Explain information in a student-friendly way.
    -Use ONLY the information provided in the context.
    -Do not make up information.
    -If the answer is not available in the context, politely tell the student that the information could not be found and suggest contacting the relevant PolyU office.
    -When appropriate, provide practical next steps.


    Context:
    {context}



    Instructions:
    If an uploaded document is provided,
    use information from both the PolyU
    knowledge base and the uploaded
    document when answering.

    Question:
    {question}
    """

    # Ask Phi-4
        
    with st.spinner("📖 Polly is thinking..."):
        try:
            response = client.chat.completions.create(
                model="nvidia/nemotron-3-ultra-550b-a55b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            answer = response.choices[0].message.content
        except Exception as e:
            
            if "429" in str(e):
                answer = (
                     "Polly is temporarily unavailable because the AI service "
                     "has reached its daily usage limit. Please try again later."
                )
            else:
                answer = f"Error: {str(e)}"

        

    answer = answer.replace("</div>", "")
    answer = answer.replace("<div>", "")



    st.metric(
        label="Confidence",
        value=f"{confidence}%"
    )

    

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    

    st.session_state.history.append(
        {
            "question": question,
            "answer": answer,
            "time": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
    )
    # st.rerun()
            
    with st.expander("Sources Used"):
        for idx in indices[0]: 
            st.write(f"Chunk {idx}")
            st.write(chunks[idx][:200] + "...")
            st.markdown("---")
    
    
    
    


st.markdown("### 💬 Conversation")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div style="
                background-color:#DCF8C6;
                padding:10px;
                border-radius:15px;
                margin:10px 0;
                max-width:70%;
                margin-left:auto;
                text-align:right;
            ">
                <b>You</b><br>
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="
                background-color:white;
                padding:12px;
                border-radius:15px;
                margin:10px 0;
                max-width:80%;
                border-left:4px solid #A6192E;
            ">
                <b>Polly</b><br>
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )   







                
        



st.sidebar.markdown("### Recent Chats")


for i, item in enumerate(reversed(st.session_state.history)):

    chat_title = item["question"][:25] + "..." if len(item["question"]) > 25 else item["question"]

    if st.sidebar.button(
        chat_title,
        key=f"chat_{i}"
    ):

    
        st.session_state.selected_chat = item

    st.sidebar.caption(item["time"])
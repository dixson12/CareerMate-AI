import streamlit as st
import requests
import os
# just an random comment
# --- Config ---
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="CareerMate AI", page_icon="💼", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.05rem;
        margin-top: 0.25rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: left;
        height: 100%;
    }
    .feature-card h4 {
        margin-bottom: 0.3rem;
    }
    .sidebar-logo {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1F2937;
    }
    .sidebar-logo span {
        background: linear-gradient(90deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sidebar-subtitle {
        color: #9CA3AF;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    .secure-box {
        background: #F5F3FF;
        border: 1px solid #E0E7FF;
        border-radius: 10px;
        padding: 0.8rem;
        font-size: 0.85rem;
        color: #4B5563;
        margin-top: 1rem;
    }
    div[data-testid="stChatInput"] {
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">💼 CareerMate <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Your AI Career Mentor</div>', unsafe_allow_html=True)

    st.markdown("**📤 Upload Document**")
    st.caption("Upload a document and chat with it.")

    uploaded_file = st.file_uploader(
        "Drag & drop your file here",
        type=["pdf", "docx", "txt"],
        help="PDF, DOCX, TXT — Max size 10MB"
    )

    if uploaded_file is not None:
        st.success(f"Selected: {uploaded_file.name}")
        if st.button("Upload", use_container_width=True):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                with st.spinner("Uploading..."):
                    response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Uploaded! {result['chunks_stored']} chunks stored.")
                else:
                    st.error(f"Upload failed: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend.")

    st.markdown(
        '<div class="secure-box">🛡️ <b>Your documents are secure</b><br>'
        'Files are encrypted and only used for your conversations.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("**🖥️ Backend Status**")
    st.caption("Check if your backend is connected and ready to help.")
    if st.button("Check Connection", use_container_width=True):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Ready to connect")
            else:
                st.error(f"❌ Backend returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot reach backend.")

# --- Main Area ---
st.markdown('<div class="main-title">Chat with your document ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a document and start asking questions.</div>', unsafe_allow_html=True)

# Feature cards (only show if no chat yet, like the mockup's empty state)
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="feature-card">💬<h4>Ask Anything</h4>'
            'Ask questions about your document in natural language.</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="feature-card">📄<h4>Smart Answers</h4>'
            'Get accurate answers based on your document content.</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div class="feature-card">🛡️<h4>Secure & Private</h4>'
            'Your data is safe and never shared with anyone.</div>',
            unsafe_allow_html=True
        )
    st.write("")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"query": prompt},
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result["answer"]
                    sources = result.get("sources", [])

                    st.markdown(answer)
                    if sources:
                        st.caption(f"📄 Sources: {', '.join(sources)}")

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend.")
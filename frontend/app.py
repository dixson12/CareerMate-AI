import streamlit as st
import requests

# --- Config ---
API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="CareerMate AI", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("📄 CareerMate AI")
    st.markdown("Upload a document and chat with it.")

    st.subheader("Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "txt"],
        help="Upload a resume or document to analyze"
    )

    if uploaded_file is not None:
        st.success(f"Selected: {uploaded_file.name}")
        if st.button("Upload"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Uploaded! Extracted {result['text_length']} characters.")
                    st.text_area("Preview", result["text_preview"], height=150)
                else:
                    st.error(f"Upload failed: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend.")

    st.divider()

    # Backend connection check
    st.subheader("Backend Status")
    if st.button("Check Connection"):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success(f"✅ Connected: {response.json()}")
            else:
                st.error(f"❌ Backend returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot reach backend. Is it running on port 8000?")

# --- Main Chat Area ---
st.header("Chat with your document")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something about your document..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the real /chat endpoint
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
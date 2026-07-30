import streamlit as st
import requests
import os

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

# =========================================================
# --- Sidebar: Uploads + Backend Status ONLY ---
# =========================================================
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

    st.divider()
    st.markdown("**📋 Upload Resume**")
    st.caption("Upload your CV for AI analysis.")

    resume_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx", "txt"],
        key="resume_uploader"
    )

    if resume_file is not None:
        st.success(f"Selected: {resume_file.name}")
        if st.button("Upload Resume", use_container_width=True):
            files = {"file": (resume_file.name, resume_file.getvalue())}
            try:
                with st.spinner("Uploading resume..."):
                    response = requests.post(f"{API_BASE_URL}/upload-resume", files=files, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    st.success(result["message"])
                    st.session_state.resume_filename = result["filename"]
                else:
                    st.error(f"Upload failed: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend.")

    if "resume_filename" in st.session_state:
        st.caption(f"✅ Active resume: {st.session_state.resume_filename}")

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

# =========================================================
# --- Main Area: Tabs for each workflow ---
# =========================================================
st.markdown('<div class="main-title">CareerMate AI ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered career mentor</div>', unsafe_allow_html=True)

tab_chat, tab_resume, tab_match, tab_interview, tab_visa = st.tabs(
    ["💬 Chat", "📄 Resume Tools", "🎯 Job Match & Roadmap", "🎤 Interview Prep", "🛂 Visa Q&A"]
)

# --- Tab 1: Chat with document (Sprint 1) ---
with tab_chat:
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

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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

# --- Tab 2: Resume Tools (Parse, Extract Skills, Analyze) ---
with tab_resume:
    if "resume_filename" not in st.session_state:
        st.info("Upload a resume from the sidebar first.")
    else:
        st.caption(f"Active resume: {st.session_state.resume_filename}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Parse Resume", use_container_width=True):
                try:
                    with st.spinner("Parsing..."):
                        response = requests.post(
                            f"{API_BASE_URL}/parse-resume/{st.session_state.resume_filename}",
                            timeout=60
                        )
                    if response.status_code == 200:
                        st.session_state.parsed_resume = response.json()["parsed_data"]
                    else:
                        st.error(f"Parsing failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

        with col2:
            if st.button("Extract Skills", use_container_width=True):
                try:
                    with st.spinner("Extracting..."):
                        response = requests.post(
                            f"{API_BASE_URL}/extract-skills/{st.session_state.resume_filename}",
                            timeout=60
                        )
                    if response.status_code == 200:
                        st.session_state.extracted_skills = response.json()["skills"]
                    else:
                        st.error(f"Extraction failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

        with col3:
            if st.button("Analyze Resume", use_container_width=True):
                try:
                    with st.spinner("Analyzing..."):
                        response = requests.post(
                            f"{API_BASE_URL}/analyze-resume/{st.session_state.resume_filename}",
                            timeout=60
                        )
                    if response.status_code == 200:
                        st.session_state.resume_analysis = response.json()["analysis"]
                    else:
                        st.error(f"Analysis failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

        st.divider()

        if "parsed_resume" in st.session_state:
            with st.expander("📄 Parsed Resume Data", expanded=True):
                st.json(st.session_state.parsed_resume)

        if "extracted_skills" in st.session_state:
            with st.expander("🛠️ Extracted Skills", expanded=True):
                st.json(st.session_state.extracted_skills)

        if "resume_analysis" in st.session_state:
            analysis = st.session_state.resume_analysis
            if "error" not in analysis:
                st.markdown("### 📊 Resume Analysis")

                score = analysis.get("overall_score", 0)
                st.metric("Overall Score", f"{score}/100")
                st.write(analysis.get("summary", ""))

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**✅ Strengths**")
                    for s in analysis.get("strengths", []):
                        st.markdown(f"- {s}")
                with col_b:
                    st.markdown("**⚠️ Areas to Improve**")
                    for w in analysis.get("weaknesses", []):
                        st.markdown(f"- {w}")

                if analysis.get("bullet_point_improvements"):
                    st.markdown("**✏️ Bullet Point Rewrites**")
                    for item in analysis["bullet_point_improvements"]:
                        st.markdown(f"❌ *{item['original']}*")
                        st.markdown(f"✅ **{item['improved']}**")
                        st.write("")

                if analysis.get("formatting_notes"):
                    st.markdown("**📐 Formatting Notes**")
                    for note in analysis["formatting_notes"]:
                        st.markdown(f"- {note}")
            else:
                st.error("Could not parse analysis results.")

# --- Tab 3: Job Match & Learning Roadmap ---
with tab_match:
    if "resume_filename" not in st.session_state:
        st.info("Upload a resume from the sidebar first.")
    else:
        st.markdown("**🎯 Match with Job Description**")
        job_description = st.text_area(
            "Paste the job description here",
            height=150,
            key="jd_input"
        )

        if st.button("Match Resume", use_container_width=True):
            if not job_description.strip():
                st.warning("Please paste a job description first.")
            else:
                try:
                    with st.spinner("Matching..."):
                        response = requests.post(
                            f"{API_BASE_URL}/match-job/{st.session_state.resume_filename}",
                            json={"job_description": job_description},
                            timeout=60
                        )
                    if response.status_code == 200:
                        st.session_state.job_match = response.json()["match"]
                    else:
                        st.error(f"Matching failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

        if "job_match" in st.session_state:
            match = st.session_state.job_match
            if "error" not in match:
                st.markdown("### 🎯 Match Results")
                st.metric("Overall Match", f"{match.get('overall_match_percentage', 0)}%")
                st.write(match.get("summary", ""))

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**✅ Matched Skills**")
                    for s in match.get("matched_skills", []):
                        st.markdown(f"- {s}")
                with col_b:
                    st.markdown("**❌ Missing Skills**")
                    for s in match.get("missing_skills", []):
                        st.markdown(f"- {s}")

                if match.get("missing_soft_skills"):
                    st.markdown("**🗣️ Missing Soft Skills**")
                    for s in match["missing_soft_skills"]:
                        st.markdown(f"- {s}")

                st.info(f"💡 {match.get('recommendation', '')}")

                missing = match.get("missing_skills", [])
                missing_soft = match.get("missing_soft_skills", [])

                if missing or missing_soft:
                    st.divider()
                    if st.button("Generate Learning Roadmap", use_container_width=True):
                        try:
                            with st.spinner("Building your roadmap..."):
                                response = requests.post(
                                    f"{API_BASE_URL}/skill-gap-roadmap",
                                    json={"missing_skills": missing, "missing_soft_skills": missing_soft},
                                    timeout=60
                                )
                            if response.status_code == 200:
                                st.session_state.learning_roadmap = response.json()["roadmap"]
                            else:
                                st.error(f"Failed: {response.status_code}")
                        except requests.exceptions.ConnectionError:
                            st.error("Cannot reach backend.")
            else:
                st.error("Could not parse match results.")

        if "learning_roadmap" in st.session_state:
            roadmap_data = st.session_state.learning_roadmap
            if "error" not in roadmap_data:
                st.markdown("### 🗺️ Your Learning Roadmap")
                for item in roadmap_data.get("roadmap", []):
                    st.markdown(f"**Week {item['week']}: {item['focus']}**")
                    st.write(item["goal"])
                    if item.get("suggested_resources"):
                        st.caption(f"Resources: {', '.join(item['suggested_resources'])}")
                    st.write("")

                if roadmap_data.get("priority_order_reasoning"):
                    st.info(f"💡 {roadmap_data['priority_order_reasoning']}")
            else:
                st.error("Could not generate roadmap.")

# --- Tab 4: Interview Prep ---
with tab_interview:
    if "resume_filename" not in st.session_state:
        st.info("Upload a resume from the sidebar first.")
    else:
        st.markdown("**🎤 Interview Preparation**")
        target_role = st.text_input("What role are you preparing for?", key="interview_role_input")

        if st.button("Generate Interview Prep", use_container_width=True):
            if not target_role.strip():
                st.warning("Please enter a target role.")
            else:
                try:
                    with st.spinner("Preparing your interview questions..."):
                        response = requests.post(
                            f"{API_BASE_URL}/interview-prep/{st.session_state.resume_filename}",
                            json={"target_role": target_role},
                            timeout=60
                        )
                    if response.status_code == 200:
                        st.session_state.interview_prep = response.json()["interview_prep"]
                    else:
                        st.error(f"Failed: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend.")

        if "interview_prep" in st.session_state:
            prep = st.session_state.interview_prep
            if "error" not in prep:
                st.markdown("### 🎤 Your Interview Prep")

                st.markdown("**💬 Behavioral Questions**")
                for q in prep.get("behavioral_questions", []):
                    st.markdown(f"- {q}")

                st.markdown("**⚙️ Technical Questions**")
                for q in prep.get("technical_questions", []):
                    st.markdown(f"- {q}")

                if prep.get("questions_about_gaps"):
                    st.markdown("**🔍 Questions About Potential Gaps**")
                    for q in prep["questions_about_gaps"]:
                        st.markdown(f"- {q}")

                if prep.get("tips"):
                    st.markdown("**💡 Tips**")
                    for tip in prep["tips"]:
                        st.markdown(f"- {tip}")
            else:
                st.error("Could not generate interview prep.")

# --- Tab 5: Visa Q&A ---
with tab_visa:
    st.markdown("**🛂 Visa Q&A**")
    st.caption("Ask about student visas, work permits, and immigration pathways in Ireland.")

    visa_question = st.text_input("Ask a visa-related question", key="visa_question_input")

    if st.button("Ask", key="visa_ask_button"):
        if not visa_question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Looking that up..."):
                    response = requests.post(
                        f"{API_BASE_URL}/visa-qa",
                        json={"question": visa_question},
                        timeout=60
                    )
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result["answer"])
                    if result.get("sources"):
                        st.caption(f"📄 Sources: {', '.join(result['sources'])}")
                else:
                    st.error(f"Failed: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend.")
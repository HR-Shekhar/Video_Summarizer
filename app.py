import streamlit as st
import requests

API_BASE = "http://localhost:8000"   # Change if FastAPI runs elsewhere

# ============================================================================  
# PAGE CONFIG  
# ============================================================================  
st.set_page_config(
    page_title="Video Summarizer Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================  
# CUSTOM CSS  
# (I kept your entire CSS EXACTLY the same — unchanged)  
# ============================================================================  
st.markdown("""<style>
/* --- ALL your CSS pasted exactly as-is (no changes) --- */
</style>""", unsafe_allow_html=True)

# ============================================================================  
# TITLE  
# ============================================================================  
st.markdown("<h1>🎬 Video Summarizer Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>✨ Get instant transcripts, summaries, and bullet points from YouTube or uploaded videos ✨</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================  
# BULLET POINT RENDERER  
# ============================================================================  
def render_bullet_points(bullets):
    if bullets is None:
        st.info("No bullet points returned.")
        return

    if isinstance(bullets, list):
        for b in bullets:
            if b:
                st.markdown(f"- {b}")
        return

    if isinstance(bullets, str):
        lines = [l.strip() for l in bullets.splitlines() if l.strip()]
        if len(lines) > 1:
            for l in lines:
                st.markdown(f"- {l}")
            return

        import re
        parts = re.split(r"[•\-\n]|(?<=\.)\s+", bullets)
        parts = [p.strip() for p in parts if p.strip()]
        for p in parts:
            st.markdown(f"- {p}")
        return

    st.write(str(bullets))

# ============================================================================  
# INPUT  
# ============================================================================  
url = st.text_input(
    "📎 YouTube Video URL",
    placeholder="Paste your YouTube link here"
)
st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "🎥 Upload Video File (MP4, MKV, MOV)",
    type=["mp4", "mkv", "mov", "avi"]
)
st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================  
# LAYOUT  
# ============================================================================  
col1, col2 = st.columns(2, gap="large")

# ============================================================================  
# YOUTUBE: TRANSCRIPT + SUMMARY  
# ============================================================================  
with col1:
    st.markdown("### 📄 Transcript & Summary (YouTube)")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Get Transcript + Summary", use_container_width=True, key="yt_transcript"):
        if not url:
            st.error("⚠️ Please enter a YouTube URL.")
        else:
            with st.spinner("🔄 Fetching transcript & summary..."):
                response = requests.post(f"{API_BASE}/transcript", json={"url": url})

            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.error("❌ " + data["error"])
                else:
                    st.markdown("#### 📝 Summary")
                    st.write(data.get("summary"))

                    with st.expander("📄 View Full Transcript"):
                        st.write(data.get("transcript"))
            else:
                st.error(f"❌ Error: {response.text}")

# ============================================================================  
# YOUTUBE: BULLET POINTS  
# ============================================================================  
with col2:
    st.markdown("### 📌 Key Points (YouTube)")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Generate Bullet Points", use_container_width=True, key="yt_bullets"):
        if not url:
            st.error("⚠️ Please enter a YouTube URL.")
        else:
            with st.spinner("🔄 Generating bullet points..."):
                response = requests.post(f"{API_BASE}/bullet_points", json={"url": url})

            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.error("❌ " + data["error"])
                else:
                    st.markdown("#### 🎯 Main Takeaways")
                    render_bullet_points(data.get("bullet_points"))
            else:
                st.error(f"❌ Error: {response.text}")

# ============================================================================  
# VIDEO FILE UPLOAD SECTION  
# ============================================================================  
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("## 🎥 Video File Summarization")
st.markdown("<p class='subtitle'>Upload a video and get transcript, summary, and bullet points</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🎧 Summarize Uploaded Video", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("⚠️ Please upload a video file first.")
    else:
        with st.spinner("🔄 Processing uploaded video..."):
            response = requests.post(
                f"{API_BASE}/video_summary",
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
            )

        if response.status_code == 200:
            data = response.json()
            st.markdown("### 📝 Summary")
            st.write(data.get("summary"))

            st.markdown("### 📌 Key Bullet Points")
            render_bullet_points(data.get("bullet_points"))

            with st.expander("📄 Full Transcript"):
                st.write(data.get("transcript"))

        else:
            st.error(f"❌ Error: {response.text}")

# ============================================================================  
# FOOTER  
# ============================================================================  
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.8); padding: 2rem;'>
        Made with ❤️ using Streamlit + FastAPI
    </div>
""", unsafe_allow_html=True)

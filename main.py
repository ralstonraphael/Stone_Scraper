import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Set advanced page configuration
st.set_page_config(
    page_title="🪨 Stone Scraper | Web Intelligence Tool",
    page_icon="🪨",
    layout="wide"
)

# --- HEADER SECTION ---
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem;'>🪨 Stone Scraper</h1>
        <p style='font-size: 1.3rem; color: #555;'>
            Your all-in-one tool to <strong>scrape websites</strong> and extract <strong>structured, intelligent data</strong> using AI.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("🔧 Scraper Config")
    url = st.text_input("🌐 Enter Website URL")
    st.markdown("Enter the full URL (including https://) of the website you want to scrape.")

    if st.button("🚀 Scrape Website"):
        if url:
            st.info("🔄 Scraping in progress...")
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content
            st.success("✅ Scraping completed!")
        else:
            st.error("⚠️ Please enter a valid URL.")

# --- MAIN PANEL ---
if "dom_content" in st.session_state:
    st.markdown("## 📄 Preview Cleaned Content")
    with st.expander("🔍 Click to Expand DOM Content"):
        st.text_area("Extracted Text Content", value=st.session_state.dom_content, height=300)

    st.markdown("## 🧠 Parse the Content Using AI")
    st.markdown("Describe what information you want to extract from the cleaned content.")

    parse_description = st.text_area("📝 Parsing Prompt", placeholder="e.g. Extract all headlines, prices, or metadata")

    if st.button("🧠 Run AI Parsing"):
        if parse_description:
            st.info("🤖 Parsing the content using Ollama...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.success("✅ Parsing completed!")

            st.markdown("### 🧾 Parsed Output")
            st.code(result, language="markdown")
        else:
            st.warning("⚠️ Please provide a description of what to parse.")

else:
    st.markdown("""
        <div style='text-align: center; padding: 2rem; color: #888;'>
            <h3>👈 Start by entering a website URL on the left</h3>
            <p>Then describe what kind of information you want to extract. Perfect for data analysts, web researchers, and curious minds.</p>
        </div>
    """, unsafe_allow_html=True)

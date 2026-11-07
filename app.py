import time
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

try:
    for _k in ("GOOGLE_API_KEY", "TAVILY_API_KEY"):
        if _k in st.secrets:
            os.environ[_k] = st.secrets[_k]
except Exception:
    pass

# Local dev fallback — .env still works
from dotenv import load_dotenv
load_dotenv()

from agents import writer_chain, critic_chain
from tools import web_search, scrape_url
from utils import extract_text, extract_urls

st.set_page_config(page_title="ResearchMind", page_icon="🔬", layout="wide")

with st.sidebar:
    st.subheader("How it works")
    st.markdown(
        """
        1. **Search** — finds recent web sources
        2. **Scrape** — pulls full page content
        3. **Writer** — drafts the report
        4. **Critic** — scores & reviews it
        """
    )
    st.divider()
    st.subheader("Example topics")
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
        st.code(ex, language=None)
    st.divider()
    if st.button("🗑 Clear results", use_container_width=True):
        st.session_state.pop("results", None)
        st.rerun()

st.title("🔬 ResearchMind")
st.caption("A 4-step research pipeline: search → scrape → write → critique")

topic = st.text_input("Research topic", placeholder="e.g. Quantum computing breakthroughs in 2025")
run = st.button("⚡ Run research", type="primary", use_container_width=True, disabled=not topic.strip())

if run:
    results = {}
    try:
        with st.status("Step 1/4 · Searching…", expanded=True) as s:
            raw = web_search.invoke({"query": f"Find recent, reliable, detailed information about: {topic}"})
            results["sources"] = extract_urls(raw)[:5]
            results["search"] = raw
            st.write(f"Found {len(results['sources'])} sources")
            s.update(label="Step 1/4 · Search complete", state="complete", expanded=False)

        with st.status("Step 2/4 · Scraping…", expanded=True) as s:
            parts = []
            for url in results["sources"][:3]:
                parts.append(f"=== {url} ===\n{scrape_url.invoke({'url': url})}")
            results["reader"] = "\n\n".join(parts)[:6000]
            st.write(f"Extracted {len(results['reader']):,} characters")
            s.update(label="Step 2/4 · Reading complete", state="complete", expanded=False)

        with st.status("Step 3/4 · Writing…", expanded=True) as s:
            research = f"SEARCH:\n{raw}\n\nSCRAPED:\n{results['reader']}"
            report = extract_text(writer_chain.invoke({"topic": topic, "research": research}))
            if results["sources"]:
                report += "\n\n### Sources\n" + "\n".join(f"- {u}" for u in results["sources"])
            results["writer"] = report
            s.update(label="Step 3/4 · Draft ready", state="complete", expanded=False)

        with st.status("Step 4/4 · Critiquing…", expanded=True) as s:
            results["critic"] = critic_chain.invoke({"report": results["writer"]})
            s.update(label="Step 4/4 · Review complete", state="complete", expanded=False)

        st.session_state.results = results
        st.session_state.topic = topic
        st.success("Pipeline finished ✅")
    except Exception as e:
        st.error(f"Pipeline failed: {e}")
        st.stop()

results = st.session_state.get("results")
if results:
    st.divider()
    st.subheader(f"Results · {st.session_state.get('topic', '')}")
    t1, t2, t3, t4 = st.tabs(["📝 Report", "🧐 Critic", "🔗 Sources", "📄 Scraped"])
    with t1:
        st.markdown(results["writer"])
        st.download_button("⬇ Download (.md)", data=results["writer"],
                           file_name=f"report_{int(time.time())}.md", mime="text/markdown")
    with t2:
        st.markdown(results["critic"])
    with t3:
        if not results["sources"]:
            st.info("No URLs found.")
        for u in results["sources"]:
            st.markdown(f"- [{u}]({u})")
    with t4:
        st.text(results["reader"])
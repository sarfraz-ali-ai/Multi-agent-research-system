# ResearchMind 🔬
A 4-stage research pipeline that searches the web, scrapes sources, drafts a report, and critiques its own output.

**🔴 [Live Demo](https://multi-agent-research-system-4tfvmtxnvnthaedytsb6tm.streamlit.app/)**

## Architecture
`Search (Tavily) -> Scrape (BeautifulSoup) -> Write (Gemini 3.5 Flash Lite) -> Critique (Structured Output)`

## Features
- **Deterministic Sourcing:** Extracts real URLs from search results and passes them to the writer, eliminating LLM-hallucinated sources.
- **Self-Correction:** A dedicated critic chain scores the report out of 10 and provides actionable feedback.
- **Production Deployment:** Fully deployed on Streamlit Cloud with secrets management and session-state history.

## Tech Stack
Python, LangChain 1.0, Gemini 3.5 Flash Lite, Tavily, Streamlit, BeautifulSoup

## Run Locally
1. Clone repo
2. `pip install -r requirements.txt`
3. Add `GOOGLE_API_KEY` and `TAVILY_API_KEY` to a `.env` file
4. `streamlit run app.py`

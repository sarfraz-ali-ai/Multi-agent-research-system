# ResearchMind 🔬

**🔴 [Live Demo on Hugging Face](https://huggingface.co/spaces/sarfraz-ali-007/Multi-agent-research-system)**

An autonomous, 4-stage AI research pipeline that takes a topic, searches the web, scrapes the top sources, drafts a comprehensive report, and then critiques its own output. 

## 🧠 Architecture & Features

The pipeline is built using **LangChain 1.0** and follows a deterministic 4-stage workflow:
1. **Search:** Uses the Tavily API to find recent, reliable, and detailed information on the given topic.
2. **Scrape:** Dynamically reads the top URLs to extract deeper context and full-page content.
3. **Write:** A dedicated LLM chain drafts a structured report (Introduction, Key Findings, Conclusion).
4. **Critique:** A secondary LLM acts as an expert critic, scoring the report out of 10 and providing actionable feedback.

**Key Engineering Highlight:** 
To eliminate the risk of LLMs hallucinating sources, this project implements **deterministic URL extraction** directly in Python. Instead of asking the LLM to list its sources, the app extracts verified URLs from the raw search data and appends them to the final report.

## 🛠️ Tech Stack

- **Framework:** LangChain 1.0 (LCEL)
- **LLM:** Google Gemini (gemini-3.5-flash-lite)
- **Search & Scraping:** Tavily API, BeautifulSoup, Requests
- **Frontend:** Streamlit
- **Deployment:** Hugging Face Spaces

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarfraz-ali-ai/Multi-agent-research-system.git
   cd Multi-agent-research-system

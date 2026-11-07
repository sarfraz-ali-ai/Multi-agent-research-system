from agents import writer_chain, critic_chain
from tools import web_search, scrape_url
from utils import extract_text, extract_urls


def run_research_pipeline(topic: str) -> dict:
    state = {"topic": topic}

    print("=" * 50, "\nstep 1 - searching ...")
    raw = web_search.invoke({"query": f"Find recent, reliable, detailed information about: {topic}"})
    state["search_results"] = raw
    state["sources"] = extract_urls(raw)[:5]
    print(f"found {len(state['sources'])} sources")

    print("=" * 50, "\nstep 2 - scraping ...")
    parts = []
    for url in state["sources"][:3]:
        print(f"scraping {url}")
        parts.append(f"=== {url} ===\n{scrape_url.invoke({'url': url})}")
    state["scraped_content"] = "\n\n".join(parts)[:6000]

    print("=" * 50, "\nstep 3 - writing ...")
    research = f"SEARCH:\n{raw}\n\nSCRAPED:\n{state['scraped_content']}"
    state["report"] = extract_text(writer_chain.invoke({"topic": topic, "research": research}))

    print("=" * 50, "\nstep 4 - critiquing ...")
    state["critique"] = critic_chain.invoke({"report": state["report"]})
    print(state["critique"])

    if state["sources"]:
        state["report"] += "\n\n### Sources\n" + "\n".join(f"- {u}" for u in state["sources"])
    return state


if __name__ == "__main__":
    run_research_pipeline(input("\nTopic: "))
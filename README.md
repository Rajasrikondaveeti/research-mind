---
title: ResearchMind
emoji: 🔬
colorFrom: yellow
colorTo: red
sdk: streamlit
sdk_version: "1.38.0"
app_file: app.py
pinned: false
---

<div align="center">

# 🔬 ResearchMind

### Multi-Agent AI Research System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Four specialized AI agents collaborate — searching, scraping, writing, and critiquing — to deliver a polished research report on any topic in seconds.**

[Getting Started](#-getting-started) · [How It Works](#-how-it-works) · [Architecture](#-architecture) · [Usage](#-usage) · [Tech Stack](#-tech-stack)

---

</div>

## ✨ Features

- 🔍 **Intelligent Web Search** — AI-powered search agent finds the most relevant and recent sources using Tavily
- 📄 **Smart Content Extraction** — Reader agent autonomously selects the best source and scrapes deep content
- ✍️ **Structured Report Generation** — Writer chain produces professional reports with introduction, key findings, conclusion, and sources
- 🧐 **Quality Assurance** — Critic chain scores the report (X/10) with detailed strengths, improvements, and a verdict
- 🎨 **Premium Dark UI** — Glassmorphism-styled Streamlit interface with real-time pipeline status tracking
- ⬇️ **Export Support** — Download generated reports as Markdown files
- 💻 **Dual Interface** — Run via the web UI or directly from the command line

---

## 🏗 Architecture

```
                          ┌─────────────────────┐
                          │     User Input       │
                          │  "CRISPR Gene Editing"│
                          └──────────┬──────────┘
                                     │
                                     ▼
                ┌────────────────────────────────────────┐
                │         STEP 1: SEARCH AGENT           │
                │   GPT-4o-mini  ──▶  web_search()       │
                │                      (Tavily API)      │
                │   Output: 5 results (title+URL+snippet)│
                └──────────────────┬─────────────────────┘
                                   │
                                   ▼
                ┌────────────────────────────────────────┐
                │         STEP 2: READER AGENT           │
                │   GPT-4o-mini  ──▶  scrape_url()       │
                │                  (BeautifulSoup)       │
                │   Output: Extracted article text       │
                └──────────────────┬─────────────────────┘
                                   │
                                   ▼
                ┌────────────────────────────────────────┐
                │         STEP 3: WRITER CHAIN           │
                │   Prompt Template  ──▶  GPT-4o-mini    │
                │   Input: topic + search + scraped data │
                │   Output: Structured research report   │
                └──────────────────┬─────────────────────┘
                                   │
                                   ▼
                ┌────────────────────────────────────────┐
                │         STEP 4: CRITIC CHAIN           │
                │   Prompt Template  ──▶  GPT-4o-mini    │
                │   Input: Full report                   │
                │   Output: Score + Feedback + Verdict   │
                └──────────────────┬─────────────────────┘
                                   │
                                   ▼
                          ┌─────────────────────┐
                          │    Final Output      │
                          │  Report + Critique   │
                          └─────────────────────┘
```

---

## 🔍 How It Works

The system uses a **sequential pipeline** of four specialized AI components:

| Step | Component | Type | What It Does |
|:----:|-----------|------|-------------|
| 1 | **Search Agent** | 🤖 Agent (LLM + Tool) | Searches the web via Tavily API, returns top 5 results with titles, URLs, and snippets |
| 2 | **Reader Agent** | 🤖 Agent (LLM + Tool) | Autonomously picks the most relevant URL and scrapes its content (up to 3000 chars) |
| 3 | **Writer Chain** | ⛓️ Chain (Prompt → LLM) | Synthesizes all gathered research into a structured report with Introduction, Key Findings, Conclusion, and Sources |
| 4 | **Critic Chain** | ⛓️ Chain (Prompt → LLM) | Reviews and scores the report (X/10) with strengths, areas to improve, and a one-line verdict |

> **Agent vs Chain:** An *agent* has an LLM brain + tools and autonomously decides when/how to use them. A *chain* is a simple prompt → LLM → output pipeline with no tool access.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Tavily API Key](https://tavily.com) (free tier: 1000 searches/month)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rajasrikondaveeti/Multi-agent-research-system.git
cd Multi-agent-research-system

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install streamlit

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your keys
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## 💡 Usage

### Web UI (Recommended)

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` with a premium dark-themed interface:

1. Enter any research topic in the input field
2. Click **⚡ Run Research Pipeline**
3. Watch the 4-step pipeline execute in real-time
4. View the full report + critic feedback
5. Download the report as a `.md` file

### Command Line

```bash
python pipeline.py
```

Prompts for a topic in the terminal and prints all outputs to the console — useful for quick testing and development.

---

## 📁 Project Structure

```
Multi-agent-research-system/
├── tools.py              # Tool definitions (web_search, scrape_url)
├── agents.py             # Agent & chain builders (search, reader, writer, critic)
├── pipeline.py           # CLI orchestrator — runs the 4-step pipeline
├── app.py                # Streamlit web UI with custom dark-mode CSS
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not committed)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

| File | Lines | Role |
|------|:-----:|------|
| `tools.py` | 38 | Defines `web_search` (Tavily API) and `scrape_url` (BeautifulSoup) tools |
| `agents.py` | 79 | Builds Search Agent, Reader Agent, Writer Chain, and Critic Chain |
| `pipeline.py` | 76 | Orchestrates all 4 steps sequentially with a shared state dictionary |
| `app.py` | 508 | Full Streamlit app with 290 lines of custom CSS, session state, and result rendering |

---

## 🛠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| **[LangChain](https://langchain.com)** | Agent & chain orchestration framework |
| **[OpenAI GPT-4o-mini](https://openai.com)** | LLM powering all agents and chains |
| **[Tavily](https://tavily.com)** | AI-optimized web search API |
| **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** | HTML parsing and content extraction |
| **[Streamlit](https://streamlit.io)** | Web application framework |
| **[python-dotenv](https://github.com/theskumar/python-dotenv)** | Environment variable management |
| **[Rich](https://github.com/Textualize/rich)** | Enhanced console output |

---

## 📊 Expected Output

| Metric | Typical Value |
|--------|:-------------:|
| Report length | 500–1500 words |
| Critic score | 7–9 / 10 |
| Key findings | 3–5 points |
| Sources cited | 3–5 URLs |
| Pipeline runtime | 30–90 seconds |
| Cost per run | ~$0.01–0.03 |

---

## ⚙️ Configuration

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| LLM Model | `agents.py` | `gpt-4o-mini` | Change to `gpt-4o` or `gpt-4-turbo` for higher quality |
| Temperature | `agents.py` | `0` | Increase for more creative outputs (0–1) |
| Max Search Results | `tools.py` | `5` | Number of Tavily results per search |
| Scrape Char Limit | `tools.py` | `3000` | Max characters extracted per URL |
| Scrape Timeout | `tools.py` | `8s` | HTTP request timeout for scraping |
| Search Input Limit | `pipeline.py` | `800 chars` | How much search data is passed to Reader |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using LangChain, OpenAI, and Streamlit**

</div>

# Heeramoti AI Agent 💎

A full-stack, AI-powered customer service representative built for a luxury jewelry storefront. This project demonstrates Agentic AI capabilities, Retrieval-Augmented Generation (RAG), database management, and asynchronous UI design.

## 🚀 Features

* **Agentic Tool Use:** The AI autonomously decides when to trigger external Python functions (checking hardcoded inventory, capturing lead data, or reading policies).
* **RAG (Retrieval-Augmented Generation):** Dynamically opens and reads a local `policies.txt` file to accurately answer customer questions about warranties and returns without hallucinating.
* **Database Integration & Lead Generation:** Writes customer contact information (Name and Phone Number) directly to a local SQLite database when a custom order is requested.
* **Rolling Window Memory:** Prevents context-window overflow and manages API token costs by querying SQLite to only feed the last 6 messages of conversation history to the model.
* **Defensive Prompt Engineering:** Strict state-machine instructions prevent the "Lazy Agent" problem, ensuring the AI gathers mandatory data before triggering write functions.
* **Asynchronous Frontend:** A vanilla JavaScript UI with dynamic DOM manipulation to handle "typing..." loading states while waiting for backend API resolution.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Database:** SQLite3
* **AI Provider:** Google GenAI SDK (`gemini-2.5-flash`)
* **Frontend:** Vanilla HTML, CSS, JavaScript (Fetch API)

## 📂 Project Structure

* `server.py` - FastAPI entry point, handles CORS and routing.
* `bot.py` - Core AI logic, database connection, tool definitions, and SDK integration.
* `index.html` - The frontend user interface.
* `policies.txt` - The knowledge base document used for RAG operations.
* `chat_history.db` - *(Ignored via .gitignore)* Local SQLite database storing messages and leads.

## 💻 How to Run Locally

### 1. Clone the repository
```bash
git clone [https://github.com/Raghunadh1597/heeramoti-ai-agent.git](https://github.com/Raghunadh1597/heeramoti-ai-agent.git)
cd heeramoti-ai-agent

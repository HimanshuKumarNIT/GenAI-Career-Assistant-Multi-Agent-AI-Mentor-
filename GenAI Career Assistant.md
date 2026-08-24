# 🤖 GenAI Career Assistant

A **LangGraph-based multi-agent Generative AI application** designed to assist users with different career-related tasks such as learning Generative AI, creating resumes, preparing for interviews, and searching for jobs.

The application uses **LangGraph for intelligent query routing**, specialized agents for different career tasks, **Gemini LLMs** for generation, **FastAPI** as the backend API, and **React** as the frontend interface.

---

## 🚀 Overview

The GenAI Career Assistant acts as a centralized AI career companion.

Instead of using one LLM prompt for every request, the application first understands the user's intent and routes the request to the appropriate specialized workflow.

### High-Level Architecture

```text
                         ┌─────────────────────┐
                         │     React UI        │
                         │    Frontend         │
                         └──────────┬──────────┘
                                    │
                              HTTP Request
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     LangGraph       │
                         │   Query Router      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             Learning Agent   Resume Agent   Interview Agent
                    │               │                │
                    │               │          ┌─────┴─────┐
                    │               │          │           │
                    │               │          ▼           ▼
                    │               │      Questions   Mock Interview
                    │               │
                    └───────────────┼────────────────┐
                                    │                │
                                    ▼                ▼
                              Tutorial Agent    Job Search Agent
                                    │                │
                                    └────────┬───────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │     Gemini LLM      │
                                  └─────────────────────┘
```

---

# ✨ Key Features

## 1. Intelligent Query Categorization

The system first categorizes the user's query into one of four major areas:

1. **Learn Generative AI Technology**
2. **Resume Making**
3. **Interview Preparation**
4. **Job Search**

The categorization is performed using an LLM-based classifier.

Example:

```text
User:
"What is RAG and how does it work?"

        ↓

Category:
1 - Learn Generative AI Technology

        ↓

Learning Agent
```

---

# 🤖 Multi-Agent Architecture

The application contains specialized workflows rather than relying on a single general-purpose prompt.

## 1. Learning Resource Agent

Responsible for helping users learn Generative AI concepts.

It further categorizes learning requests into:

- General Questions
- Tutorials

### Example

```text
User:
"What is LangGraph?"

        ↓

Learning Resource Agent

        ↓

Question

        ↓

Generative AI Expert Response
```

For tutorial-related requests:

```text
User:
"Create a tutorial on prompt engineering."

        ↓

Learning Resource Agent

        ↓

Tutorial Agent

        ↓

Structured Markdown Tutorial
```

---

## 2. Resume Agent

The Resume Agent is responsible for creating customized resumes for AI and Generative AI-oriented roles.

It is designed to consider:

- Technical skills
- Education
- Projects
- Experience
- AI/GenAI technologies
- Job-relevant keywords

### Example

```text
User:
"Create an AI Engineer resume using my Python,
LangChain, FastAPI and Generative AI projects."

        ↓

Resume Agent

        ↓

Customized Resume
```

The generated resume can be structured in Markdown format.

---

## 3. Interview Preparation Agent

The Interview Agent supports two major workflows.

### Interview Questions

Provides curated interview questions related to:

- Generative AI
- AI Engineering
- LLMs
- LangChain
- LangGraph
- RAG
- Other relevant AI technologies

### Example

```text
User:
"Give me important GenAI interview questions."

        ↓

Interview Agent

        ↓

Interview Question Generation
```

---

### Mock Interview

The Mock Interview workflow is designed to simulate a Generative AI interview.

The workflow can cover:

- Technical questions
- Generative AI concepts
- Candidate responses
- Interview evaluation

The goal is to provide an interview-practice environment rather than simply returning a static list of questions.

---

## 4. Job Search Agent

The Job Search Agent is responsible for finding relevant job opportunities based on the user's requirements.

It uses a web search tool to retrieve job-related information and then uses the LLM to organize the retrieved results into a more readable format.

### Example

```text
User:
"Find AI Engineer jobs in Bangalore."

        ↓

Job Search Agent

        ↓

Web Search

        ↓

LLM-based Formatting

        ↓

Organized Job Results
```

The job search workflow uses **DuckDuckGo search** for retrieving current web information.

---

# 🔀 LangGraph Workflow

LangGraph is used to coordinate the different workflows.

The main workflow follows:

```text
START
  │
  ▼
Categorize Query
  │
  ├───────────────┬────────────────┬────────────────┐
  │               │                │                │
  ▼               ▼                ▼                ▼
Learning        Resume          Interview        Job Search
  │                                │
  │                                │
  ▼                                ▼
Learning Type                Interview Type
  │                                │
  ├────────────┐             ┌─────┴─────┐
  ▼            ▼             ▼           ▼
Question    Tutorial      Questions   Mock Interview
  │            │             │           │
  └──────┬─────┘             └─────┬─────┘
         │                           │
         ▼                           ▼
        END                         END
```

This allows the application to make routing decisions before executing the specialized workflow.

---

# 🧠 Agent Routing

The main categorizer classifies the user request into four categories.

```text
1 → Learning Resource
2 → Resume Making
3 → Interview Preparation
4 → Job Search
```

### Learning Routing

```text
Learning Resource
       │
       ├── Question
       │      ↓
       │   Ask Query Bot
       │
       └── Tutorial
              ↓
         Tutorial Agent
```

### Interview Routing

```text
Interview Preparation
       │
       ├── Question
       │      ↓
       │ Interview Questions
       │
       └── Mock
              ↓
        Mock Interview
```

---

# 🛠️ Technology Stack

## Frontend

- React
- JavaScript
- HTML
- CSS

## Backend

- Python
- FastAPI
- Pydantic

## Agent Orchestration

- LangGraph
- LangChain

## LLM

- Google Gemini
- `gemini-2.5-flash`

## Search

- DuckDuckGo Search

## Development

- Visual Studio Code
- Python virtual environment
- Node.js / npm

---

# 📁 Project Structure

```text
GenAI_Career_Assistant/
│
├── backend/
│   │
│   ├── agent.py
│   │
│   ├── main.py
│   │
│   └── ...
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── ...
│   │
│   ├── package.json
│   └── package-lock.json
│
├── .venv/
│
├── .env
│
├── README.md
│
└── ...
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd GenAI_Career_Assistant
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## 3. Install Python Dependencies

Install the required dependencies used by the backend.

Example:

```bash
pip install fastapi uvicorn
pip install langchain
pip install langchain-community
pip install langchain-google-genai
pip install langgraph
pip install python-dotenv
```

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

**Never commit your API key to GitHub.**

Add `.env` to `.gitignore`:

```text
.env
.venv/
__pycache__/
node_modules/
```

---

# ▶️ Running the Backend

Open a terminal from the project root:

```powershell
cd backend
python -m uvicorn main:app --reload
```

The FastAPI server will start at:

```text
http://127.0.0.1:8000
```

---

# ▶️ Running the Frontend

Open a **second terminal**:

```powershell
cd frontend
npm start
```

The React application will be available at:

```text
http://localhost:3000
```

---

# 🔌 API

## Health Check

### Request

```http
GET /
```

### Response

```json
{
  "message": "GenAI Career Assistant API is running"
}
```

---

## Chat Endpoint

### Request

```http
POST /chat
```

### Input

```json
{
  "query": "What is LangGraph?"
}
```

### Successful Response

```json
{
  "success": true,
  "category": "1",
  "response": "LangGraph is ..."
}
```

### Error Response

```json
{
  "success": false,
  "error": "Gemini API quota exceeded. Please try again later."
}
```

---

# 🌐 React → FastAPI Communication

The frontend sends user queries to the FastAPI backend using an HTTP POST request.

```text
React
  │
  │ POST /chat
  │
  ▼
FastAPI
  │
  ▼
LangGraph
  │
  ▼
Specialized Agent
  │
  ▼
LLM / Search Tool
  │
  ▼
FastAPI Response
  │
  ▼
React UI
```

CORS middleware is configured in FastAPI so that the React development server can communicate with the backend.

---

# 🧪 Example Queries

## Generative AI Learning

```text
What is LangGraph?
```

```text
Explain RAG with a simple example.
```

```text
What is the difference between LangChain and LangGraph?
```

---

## Tutorial Generation

```text
Create a beginner-friendly tutorial on prompt engineering.
```

```text
Create a tutorial explaining RAG using Python.
```

---

## Resume Generation

```text
Create an AI Engineer resume using the following details:

Name: Candidate Name

Skills:
Python, SQL, LangChain, LangGraph, FastAPI

Projects:
GenAI Career Assistant
RAG-based Question Answering System

Education:
MSc Computer Science
```

---

## Interview Preparation

```text
Give me important Generative AI interview questions.
```

```text
What topics should I prepare for an AI Engineer interview?
```

---

## Mock Interview

```text
Conduct a mock interview for a Generative AI Engineer role.
```

---

## Job Search

```text
Find AI Engineer jobs in Bangalore.
```

```text
Find Generative AI internships in Pune.
```

---

# 🔄 End-to-End Execution Flow

A typical user request follows this process:

```text
1. User enters a query in React
              ↓
2. React sends POST /chat
              ↓
3. FastAPI receives the query
              ↓
4. run_user_query() invokes LangGraph
              ↓
5. categorize() determines the main category
              ↓
6. route_query() selects the appropriate workflow
              ↓
7. Specialized agent processes the request
              ↓
8. Agent calls the required LLM/search capability
              ↓
9. Response is returned through FastAPI
              ↓
10. React displays the result
```

---

# 🧩 Why LangGraph?

A single LLM prompt could answer many of these queries, but the goal of this application is to separate responsibilities into specialized workflows.

LangGraph provides:

- Explicit workflow structure
- Conditional routing
- Specialized agent nodes
- State-based execution
- Clear separation between different career tasks

This makes the system easier to extend with additional agents and workflows.

---

# 🏗️ Design Approach

The application follows a **router → specialized workflow** architecture.

Instead of:

```text
User
 ↓
One LLM
 ↓
Answer
```

the application follows:

```text
User
 ↓
Query Categorization
 ↓
Workflow Routing
 ↓
Specialized Agent
 ↓
LLM / Tool
 ↓
Response
```

This allows each agent to focus on a specific responsibility.

---

# 🚧 Current Limitations

The current version is primarily designed as a functional prototype and demonstration system.

Some workflows, particularly Resume and Mock Interview, were originally designed around conversational/interactive execution and can be further improved for production-grade session management.

Other planned improvements include:

- Persistent conversation memory
- Session-based multi-turn interactions
- More advanced Resume Agent workflow
- Improved Mock Interview state management
- Better UI/UX
- Structured job-search filters
- Better response rendering
- Production-grade authentication
- LLM provider abstraction
- Local LLM support using Ollama
- Production deployment

---

# 🔮 Future Improvements

## 1. Persistent Conversation Memory

Introduce session-based conversation management:

```text
User
 ↓
Session ID
 ↓
Conversation State
 ↓
Agent
 ↓
Response
```

This would allow Resume and Mock Interview agents to maintain context across multiple requests.

---

## 2. Local LLM Support

The architecture can be extended to support local models through Ollama.

```text
React
 ↓
FastAPI
 ↓
LangGraph
 ↓
Ollama
 ↓
Local LLM
```

This can reduce dependency on cloud API quotas during development and testing.

---

## 3. Improved UI

Future UI improvements can include:

- Chat-style interface
- Agent/category indicators
- Loading states
- Markdown rendering
- Resume preview
- Job cards
- Interview dashboard
- Conversation history

---

# 🔒 Security Considerations

API credentials should always be stored in environment variables.

Never hard-code:

```python
GOOGLE_API_KEY = "actual-key"
```

Instead:

```env
GOOGLE_API_KEY=your_key
```

and load it through environment configuration.

---

# 📌 Project Goal

The primary goal of the project is to demonstrate how **Generative AI, LLMs, LangChain, LangGraph, web APIs, search tools, and a modern frontend** can be combined to build a practical multi-agent career assistant.

The system demonstrates both:

- **LLM-based generation**
- **Agentic workflow orchestration**

rather than treating the LLM as a standalone chatbot.

---

# 👨‍💻 Author

**Himanshu**

GenAI / AI Engineering Project

---

# ⭐ Key Takeaway

```text
                 GenAI Career Assistant

                         User
                          │
                          ▼
                      React UI
                          │
                          ▼
                       FastAPI
                          │
                          ▼
                     LangGraph
                          │
                  Query Categorizer
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Learning           Resume          Interview
     Agent             Agent             Agent
        │                                  │
        │                            ┌─────┴─────┐
        │                            │           │
        ▼                            ▼           ▼
   Tutorial /                  Questions    Mock Interview
    Question
        │
        └──────────────────┬──────────────────┘
                           │
                           ▼
                    Job Search Agent
                           │
                           ▼
                      Gemini / Tools
                           │
                           ▼
                       Response
```

**A modular, LangGraph-orchestrated GenAI career assistant with a React frontend and FastAPI backend.**
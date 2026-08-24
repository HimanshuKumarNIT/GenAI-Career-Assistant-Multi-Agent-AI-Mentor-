 

# %%
from typing import Dict, TypedDict
from langgraph.graph import StateGraph, END, START  
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
 
from dotenv import load_dotenv
import os
from ddgs import DDGS
 
load_dotenv()

# Set the Gemini API key for authentication with Google Generative AI services
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Instantiate a chat model using Google's Gemini-2.5-flash with specified configurations
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                             verbose=True,
                             temperature=0.5,
                             max_output_tokens=2048,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

 
class State(TypedDict):
    query: str
    category: str
    response: str

# %%
# Importing message types and utilities from langchain_core:
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, trim_messages

def trim_conversation(prompt):
    """Trims conversation history to retain only the latest messages within the limit."""
    max_messages = 10 
    return trim_messages(
        prompt,
        max_tokens=max_messages,   
        strategy="last",  
        token_counter=len,   
        start_on="human",   
        include_system=True,   
        allow_partial=False,   
    )

 
from datetime import datetime

def save_file(data, filename):
    """Saves data to a markdown file with a timestamped filename."""
    folder_name = "Agent_output"  
    os.makedirs(folder_name, exist_ok=True)   
    
    # Generate a timestamped filename for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  
    filename = f"{filename}_{timestamp}.md"
    
    
    file_path = os.path.join(folder_name, filename)
    
    # Save the data to the file in the specified path
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)
        print(f"File '{file_path}' created successfully.")
    
     
    return file_path

 
# %%
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class LearningResourceAgent:
    def __init__(self, prompt):
        # Initialize the chat model and prompt template
        self.model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=2048
)
        self.prompt = prompt

    def TutorialAgent(self, user_input):

        chain = self.prompt | self.model

        response = chain.invoke({
            "input": user_input,
            "chat_history": []
        })

        return (
            str(response.content)
            .replace("```markdown", "")
            .replace("```", "")
            .strip()
        )

    def QueryBot(self, user_input):
        """
        Answer a single user query.
        Suitable for FastAPI and React.
        """

        self.prompt.append(
        HumanMessage(content=user_input)
        )

        self.prompt = trim_conversation(self.prompt)

        response = self.model.invoke(self.prompt)

        self.prompt.append(
        AIMessage(content=response.content)
        )

        return response.content
 

# %%
class InterviewAgent:

    def __init__(self, prompt):

        # Initialize chat model and prompt
        self.model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=2048
)

        self.prompt = prompt

    def Interview_questions(self, user_input):

        chain = self.prompt | self.model

        response = chain.invoke({
            "input": user_input,
            "chat_history": []
        })

        return (
            str(response.content)
            .replace("```markdown", "")
            .replace("```", "")
            .strip()
        )

    def Mock_Interview(self):

        chain = self.prompt | self.model

        response = chain.invoke({
            "input": """
    Generate a complete Generative AI mock interview.

    Include:

    1. Introduction Questions
    2. Technical Questions
    3. Advanced Questions
    4. Scenario-Based Questions
    5. Evaluation Criteria

    Do not conduct an interactive interview.
    Return all questions together.
    """
        })

        return (
            str(response.content)
            .replace("```markdown", "")
            .replace("```", "")
            .strip()
        )

 

# %%
class ResumeMaker:

    def __init__(self, prompt):

        # Initialize chat model and prompt
        self.model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=2048
)

        self.prompt = prompt

    def Create_Resume(self, user_input):

        chain = self.prompt | self.model

        response = chain.invoke({
        "input": user_input,
        "chat_history": []
        })
        return response.content
        

# %%
class JobSearch:
    def __init__(self, prompt):
        # Initialize the chat model, prompt template, and search tool for job search assistance
        self.model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=2048
)
        self.prompt = prompt
           
      

    def find_jobs(self, user_input):

        results = list(
            DDGS().text(
                user_input,
                max_results=10
            )
        )

        search_results = "\n\n".join(
            [
                f"Title: {r['title']}\n"
                f"Link: {r['href']}\n"
                f"Description: {r['body']}"
                for r in results
            ]
        )

        chain = self.prompt | self.model

        jobs = chain.invoke({
            "result": search_results
        }).content

        path = save_file(
            str(jobs).replace("```markdown", "").strip(),
            'Job_search'
        )

        print(f"Jobs saved to {path}")

        return jobs



# %%
def categorize(state: State) -> State:
    """Categorizes the user query into one of four main categories: Learn Generative AI Technology, Resume Making, Interview Preparation, or Job Search."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following customer query into one of these categories:\n"
        "1: Learn Generative AI Technology\n"
        "2: Resume Making\n"
        "3: Interview Preparation\n"
        "4: Job Search\n"
        "Give the number only as an output.\n\n"
        "Examples:\n"
        "1. Query: 'What are the basics of generative AI, and how can I start learning it?' -> 1\n"
        "2. Query: 'Can you help me improve my resume for a tech position?' -> 2\n"
        "3. Query: 'What are some common questions asked in AI interviews?' -> 3\n"
        "4. Query: 'Are there any job openings for AI engineers?' -> 4\n\n"
        "Now, categorize the following customer query:\n"
        "Query: {query}"
    )

    # Creates a categorization chain and invokes it with the user's query to get the category
    chain = prompt | llm 
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def handle_learning_resource(state: State) -> State:
    """Determines if the query is related to Tutorial creation or general Questions on generative AI topics."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following user query into one of these categories:\n\n"
        "Categories:\n"
        "- Tutorial: For queries related to creating tutorials, blogs, or documentation on generative AI.\n"
        "- Question: For general queries asking about generative AI topics.\n"
        "- Default to Question if the query doesn't fit either of these categories.\n\n"
        "Examples:\n"
        "1. User query: 'How to create a blog on prompt engineering for generative AI?' -> Category: Tutorial\n"
        "2. User query: 'Can you provide a step-by-step guide on fine-tuning a generative model?' -> Category: Tutorial\n"
        "3. User query: 'Provide me the documentation for Langchain?' -> Category: Tutorial\n"
        "4. User query: 'What are the main applications of generative AI?' -> Category: Question\n"
        "5. User query: 'Is there any generative AI course available?' -> Category: Question\n\n"
        "Now, categorize the following user query:\n"
        "The user query is: {query}\n"
    )

    # Creates a further categorization chain to decide between Tutorial or Question
    chain = prompt | llm 
    response = chain.invoke({"query": state["query"]}).content
    return {"category": response}

def handle_interview_preparation(state: State) -> State:
    """Determines if the query is related to Mock Interviews or general Interview Questions."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following user query into one of these categories:\n\n"
        "Categories:\n"
        "- Mock: For requests related to mock interviews.\n"
        "- Question: For general queries asking about interview topics or preparation.\n"
        "- Default to Question if the query doesn't fit either of these categories.\n\n"
        "Examples:\n"
        "1. User query: 'Can you conduct a mock interview with me for a Gen AI role?' -> Category: Mock\n"
        "2. User query: 'What topics should I prepare for an AI Engineer interview?' -> Category: Question\n"
        "3. User query: 'I need to practice interview focused on Gen AI.' -> Category: Mock\n"
        "4. User query: 'Can you list important coding topics for AI tech interviews?' -> Category: Question\n\n"
        "Now, categorize the following user query:\n"
        "The user query is: {query}\n"
    )

    # Creates a further categorization chain to decide between Mock or Question
    chain = prompt | llm 
    response = chain.invoke({"query": state["query"]}).content
    return {"category": response}



# %%
def job_search(state: State) -> State:
    """
    Search and present relevant job opportunities
    based on the user's requirements.
    """

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert Career Advisor and Job Search Assistant.

        Analyze the job search results and generate a professional report.

        Instructions:
        - Show only the most relevant opportunities.
        - Include Job Title.
        - Include Company Name if available.
        - Include Application Link.
        - Include a short job description.
        - Highlight required skills if available.
        - Keep the output clean and recruiter-friendly.
        - Use proper headings and bullet points.
        - Do NOT mention markdown files.
        - Do NOT say "Here is the markdown content".
        - Do NOT explain your process.
        - Directly present the job opportunities.

        Job Search Results:
        {result}
        """
    )

    jobSearch = JobSearch(prompt)

    response = jobSearch.find_jobs(
        state["query"]
    )

    return {"response": response}


def check_resume_completeness(user_input: str):
    """
    Checks whether enough resume information
    is available before generating a resume.
    """

    text = user_input.lower()

    sections_found = []

    if any(word in text for word in [
        "skill", "skills", "python", "sql",
        "power bi", "machine learning", "ai"
    ]):
        sections_found.append("Skills")

    if any(word in text for word in [
        "project", "projects"
    ]):
        sections_found.append("Projects")

    if any(word in text for word in [
        "education", "b.tech", "btech",
        "m.tech", "degree", "college",
        "university"
    ]):
        sections_found.append("Education")

    if any(word in text for word in [
        "experience", "internship",
        "worked", "employee"
    ]):
        sections_found.append("Experience")

    return sections_found


def handle_resume_making(state: State) -> State:
    """
    Generate a customized resume based on user details
    for a tech role in AI and Generative AI.

    Added:
    - Resume information validation
    - Decision making before generation
    """

    sections_found = check_resume_completeness(
        state["query"]
    )

    # Agent decision step
    if len(sections_found) < 2:

        missing_sections = [
            section for section in
            ["Education", "Skills", "Projects", "Experience"]
            if section not in sections_found
        ]

        return {
            "response":
            f"""
Resume Agent Analysis

I don't have enough information to generate a high-quality ATS-friendly resume.

Detected Sections:
{', '.join(sections_found) if sections_found else 'None'}

Missing Sections:
{', '.join(missing_sections)}

Please provide at least:
1. Education
2. Skills
3. Projects

Experience is optional for freshers.
"""
        }

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",

            '''
            Generate a complete ATS-friendly resume
            from the information provided by the user.

            If some information is missing,
            make reasonable assumptions and clearly indicate them.

            Return a complete professional resume
            in markdown format.
            '''
        ),

        MessagesPlaceholder("chat_history"),

        ("human", "{input}"),
    ])

    resumeMaker = ResumeMaker(prompt)

    response = resumeMaker.Create_Resume(
        state["query"]
    )

    return {"response": response}


# %%
def ask_query_bot(state: State) -> State:
    """
    Provide detailed answers to user queries
    related to Generative AI.
    """

    system_message = '''
    You are an expert Generative AI Engineer
    with extensive experience in training
    and guiding others in AI engineering.

    You have a strong track record of solving
    complex problems and addressing various
    challenges in AI.

    Your role is to assist users by providing
    insightful solutions and expert advice
    on their queries.

    Engage in a back-and-forth chat session
    to address user queries.
    '''

    prompt = [
        SystemMessage(content=system_message)
    ]

    learning_agent = LearningResourceAgent(prompt)

    response = learning_agent.QueryBot(state["query"])

    return {"response": response}


def tutorial_agent(state: State) -> State:
    """
    Generate a tutorial blog for Generative AI
    based on user requirements.
    """

    system_message = '''
    You are a knowledgeable assistant
    specializing as a Senior Generative AI Developer
    with extensive experience in both development
    and tutoring.

    Additionally, you are an experienced blogger
    who creates tutorials focused on Generative AI.

    Your task is to develop high-quality tutorial blogs
    in .md format with coding examples
    based on the user's requirements.

    Ensure tutorials include:
    - Clear explanations
    - Well-structured Python code
    - Proper comments
    - Fully functional code examples

    Provide resource reference links
    at the end of each tutorial
    for further learning.
    '''

    prompt = ChatPromptTemplate.from_messages([

        ("system", system_message),

        ("placeholder", "{chat_history}"),

        ("human", "{input}"),
    ])

    learning_agent = LearningResourceAgent(prompt)

    response = learning_agent.TutorialAgent(
        state["query"]
    )

    return {"response": response}



# %%
def interview_topics_questions(state: State) -> State:
    """
    Provide a curated list of interview questions
    related to Generative AI based on user input.
    """

    system_message = '''
    You are a good researcher in finding interview questions
    for Generative AI topics and jobs.

    Your task is to provide a list of interview questions
    for Generative AI topics and jobs
    based on user requirements.

    Provide top questions with references and links if possible.

    You may ask for clarification if needed.

    Generate a .md document containing the questions.
    '''

    prompt = ChatPromptTemplate.from_messages([

        ("system", system_message),

        MessagesPlaceholder("chat_history"),

        ("human", "{input}"),
    ])

    interview_agent = InterviewAgent(prompt)

    response = interview_agent.Interview_questions(
        state["query"]
    )

    return {"response": response}


def mock_interview(state: State) -> State:
    """
    Conduct a mock interview for a Generative AI position,
    including evaluation at the end.
    """

    system_message = '''
    You are a Generative AI Interviewer.

    You have conducted numerous interviews
    for Generative AI roles.

    Your task is to conduct a mock interview
    for a Generative AI position,
    engaging in a back-and-forth interview session.

    The conversation should not exceed
    more than 15 to 20 minutes.

    At the end of the interview,
    provide an evaluation for the candidate.
    '''

    prompt = [
        SystemMessage(content=system_message)
    ]

    interview_agent = InterviewAgent(prompt)

    response = interview_agent.Mock_Interview()

    return {"response": response}


# %%
def route_query(state: State):
    """Route the query based on its category to the appropriate handler."""
    if '1' in state["category"]:
         
        return "handle_learning_resource"   
    elif '2' in state["category"]:
         
        return "handle_resume_making"  
    elif '3' in state["category"]:
         
        return "handle_interview_preparation"   
    elif '4' in state["category"]:
         
        return "job_search"  
    else:
         
        return "handle_learning_resource"   

def route_interview(state: State) -> str:
    """Route the query to the appropriate interview-related handler."""
    if 'Question'.lower() in state["category"].lower():
        return "interview_topics_questions"   
    elif 'Mock'.lower() in state["category"].lower():
        return "mock_interview"  
    else:
        return "mock_interview"  

def route_learning(state: State):
    """Route the query based on the learning path category."""
    if 'Question'.lower() in state["category"].lower():
        return "ask_query_bot" 
    elif 'Tutorial'.lower() in state["category"].lower():
        return "tutorial_agent"  
    else:
        return "ask_query_bot"   


# %%
# Create the workflow graph
workflow = StateGraph(State)

# Add nodes for each state in the workflow
workflow.add_node("categorize", categorize)

workflow.add_node(
    "handle_learning_resource",
    handle_learning_resource
)

workflow.add_node(
    "handle_resume_making",
    handle_resume_making
)

workflow.add_node(
    "handle_interview_preparation",
    handle_interview_preparation
)

workflow.add_node(
    "job_search",
    job_search
)

workflow.add_node(
    "mock_interview",
    mock_interview
)

workflow.add_node(
    "interview_topics_questions",
    interview_topics_questions
)

workflow.add_node(
    "tutorial_agent",
    tutorial_agent
)

workflow.add_node(
    "ask_query_bot",
    ask_query_bot
)

# Starting edge
workflow.add_edge(START, "categorize")

# Main category routing
workflow.add_conditional_edges(
    "categorize",
    route_query,
    {
        "handle_learning_resource":
            "handle_learning_resource",

        "handle_resume_making":
            "handle_resume_making",

        "handle_interview_preparation":
            "handle_interview_preparation",

        "job_search":
            "job_search"
    }
)

# Interview routing
workflow.add_conditional_edges(
    "handle_interview_preparation",
    route_interview,
    {
        "mock_interview":
            "mock_interview",

        "interview_topics_questions":
            "interview_topics_questions",
    }
)

# Learning routing
workflow.add_conditional_edges(
    "handle_learning_resource",
    route_learning,
    {
        "tutorial_agent":
            "tutorial_agent",

        "ask_query_bot":
            "ask_query_bot",
    }
)

# End nodes
workflow.add_edge(
    "handle_resume_making",
    END
)

workflow.add_edge(
    "job_search",
    END
)

workflow.add_edge(
    "interview_topics_questions",
    END
)

workflow.add_edge(
    "mock_interview",
    END
)

workflow.add_edge(
    "ask_query_bot",
    END
)

workflow.add_edge(
    "tutorial_agent",
    END
)

# Entry point
workflow.set_entry_point("categorize")

# Compile workflow
app = workflow.compile()


# %%
def run_user_query(query: str) -> Dict[str, str]:
    """
    Process a user query through the LangGraph workflow.

    Args:
        query (str): The user's query

    Returns:
        Dict[str, str]:
        A dictionary containing the query's category and response
    """

    results = app.invoke(
        {"query": query},

        # Prevent infinite recursion/tool loops
        config={"recursion_limit": 5}
    )

    return {
        "category": results["category"],
        "response": results["response"]
    }
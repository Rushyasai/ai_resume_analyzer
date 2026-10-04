"""Module 6: simple rule-based learning roadmap."""

TOPICS = {
    "Python": "Python basics, functions, OOP, file handling",
    "SQL": "SELECT, JOINs, GROUP BY, window functions",
    "Excel": "Formulas, pivot tables, charts",
    "Pandas": "DataFrames, cleaning, groupby, merging",
    "NumPy": "Arrays, broadcasting, vectorised maths",
    "Power BI": "Build an interactive dashboard from a CSV",
    "Data Visualization": "Matplotlib/Plotly charts and storytelling",
    "Statistics": "Descriptive stats, distributions, hypothesis testing",
    "Machine Learning": "Supervised learning, train/test split, evaluation metrics",
    "scikit-learn": "Pipelines, model selection, cross-validation",
    "FastAPI": "FastAPI basics, then serve an ML model as an API",
    "Docker": "Docker fundamentals, containerise a small app",
    "MLflow": "Experiment tracking and model registry with MLflow",
    "Cloud Deployment": "Deploy an app on Streamlit Cloud / Render / AWS",
    "Git": "Git branching, commits, pull requests on GitHub",
    "Deep Learning": "Neural networks, backpropagation, a CNN/RNN project",
    "LLM": "Prompting, APIs, and building a small LLM app",
    "RAG": "Embeddings, vector search, build a RAG chatbot",
    "LangChain": "Chains, prompts, retrievers with LangChain",
    "REST API": "HTTP methods, building and consuming REST APIs",
    "NLP": "Tokenisation, TF-IDF, text classification",
    "Transformers": "Attention, BERT fine-tuning with Hugging Face",
    "Hugging Face": "Hugging Face pipelines and model hub",
    "spaCy": "spaCy pipelines, NER and phrase matching",
    "PyTorch": "Tensors, autograd, training loops",
    "TensorFlow": "Keras models with TensorFlow",
    "OpenCV": "Image I/O, filters, contours, feature detection",
    "CNN": "Convolution layers, image classification project",
    "YOLO": "Object detection with YOLO on a custom dataset",
    "Flask": "Routes, templates, build a small web app",
    "Django": "Models, views, ORM, build a CRUD app",
    "HTML": "Semantic HTML and forms",
    "CSS": "Flexbox, grid, responsive layout",
    "JavaScript": "ES6, DOM, fetch API",
    "React": "Components, state, hooks",
    "Matplotlib": "Line, bar, scatter plots and subplots",
}


def generate_roadmap(missing: list[str], max_weeks: int = 8) -> list[str]:
    plan = []
    for week, skill in enumerate(missing[:max_weeks], start=1):
        topic = TOPICS.get(skill, f"Learn the fundamentals of {skill} and build one small project")
        plan.append(f"Week {week}: {skill} - {topic}")
    return plan

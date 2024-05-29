from langchain.prompts import ChatPromptTemplate


def assistant_template():
    template = """You are an assistant for question-answering tasks. use the following context to answer the question.
    If you don't know the answer, just say that you don't know. output languse will be the same as question langusge.

    Context: {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt


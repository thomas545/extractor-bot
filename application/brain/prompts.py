from langchain.prompts import ChatPromptTemplate


def default_template():
    template = """You are an assistant for question-answering tasks.
    use the following context to answer the question.
    If you don't know the answer, just say that you don't know.

    Context: {context}
    Question: {query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt


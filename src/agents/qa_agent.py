from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
load_dotenv()
def QAagent(query_text,retrived_chunks):
    """question answering agent"""


    context = [r['embed_text'] for r in retrived_chunks]
    print(context)

    system_template = """
    You are an expert assistant specializing in answering questions .

    Use only the information provided in the context below to answer the question.
    If the answer is not in the context, respond with: "I don't know."
    Do not guess or provide any information beyond the context.
    """

    human_template = """
    <context>
    {context}
    </context>

    <question>
    {question}
    </question>
    """

    key = os.getenv('OPEN_AI_KEY')
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template.strip()),
        HumanMessagePromptTemplate.from_template(human_template.strip())
    ])


    llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key= key)


    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.run(context=context, question=query_text)
 


    return response


from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
template = (
    "You are a data extraction assistant tasked with parsing quantitative or structured data "
    "from the following web content:\n\n{dom_content}\n\n"
    "Instructions:\n"
    "1. Extract only the data relevant to this description: {parse_description}.\n"
    "2. Focus on numerical values, labels, statistical indicators, or tabular information that can be used in data analysis.\n"
    "3. Return only the extracted data — no summaries, comments, or explanations.\n"
    "4. If the requested format implies tabular structure (e.g., multiple rows or variables), output the result as a clean table.\n"
    "5. If no matching data is found, return an empty string ('').\n"
)


model = OllamaLLM(model="llama3.2", temperature=0.1)

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    parsed_results = []

    total = len(dom_chunks)
    for i, chunk in enumerate(dom_chunks, start=1):
        print(f"Parsing chunk {i}/{total}...")
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        print(f"Finished parsing chunk {i}/{total}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

from langchain_ollama import OllamaLLM  # Import the OllamaLLM model for language processing
from langchain_core.prompts import ChatPromptTemplate  # Import ChatPromptTemplate to create structured prompts

# Define the prompt template for the language model
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

# Initialize the OllamaLLM model with specific parameters
model = OllamaLLM(model="llama3.2", temperature=0.1)

# Function to parse web content using the Ollama language model
def parse_with_ollama(dom_chunks, parse_description):
    # Create a prompt object using the defined template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Combine the prompt and the model into a processing chain
    chain = prompt | model
    
    # List to store the parsed results from each chunk of web content
    parsed_results = []

    total = len(dom_chunks)  # Total number of chunks to process
    for i, chunk in enumerate(dom_chunks, start=1):
        # Log the progress of parsing
        print(f"Parsing chunk {i}/{total}...")
        
        # Invoke the chain with the current chunk and the parsing description
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        
        # Log completion of parsing for the current chunk
        print(f"Finished parsing chunk {i}/{total}")
        
        # Append the parsed result to the results list
        parsed_results.append(response)

    # Combine all parsed results into a single string and return
    return "\n".join(parsed_results)

from langchain_groq import ChatGroq
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.chains import LLMChain
import pandas as pd
import os
import threading
from config.config import get_config
from fewshort_examples import examples_prompt
import logging
from set_logging import set_logging_file, set_logging_error


config = get_config()
logger_error = set_logging_error() # sử dụng để ghi log lỗi 
logger_file = set_logging_file() # sủ dụng để ghi log của file đã được thực hiện trong folder

def create_model(idx: int): # create llm model
    api_key = "GROQ_API_KEY_" + str(idx) 
    model = ChatGroq(
        api_key=config['API_KEY'][api_key],
        model=config['MODEL'],
        temperature=0.0,
        max_tokens=500
    )
    return model


def llm_invoke(text_input: str, idx) -> str: #  combine llm and fewshortprompt and excute query

    examples = examples_prompt


    example_formatter_template = """
        Thông tin sản phẩm: {command}
        Thông tin extract được từ sản phẩm:\n
        Sản phẩm: {command}\n
        ID: {ID}
    """

    example_prompt = PromptTemplate(
        input_variables=["command", "ID"],
        template=example_formatter_template,
    )

    few_shot_prompt = FewShotPromptTemplate(
        # These are the examples we want to insert into the prompt.
        examples=examples,
        # This is how we want to format the examples when we insert them into the prompt.
        example_prompt=example_prompt,
        # The prefix is some text that goes before the examples in the prompt.
        # Usually, this consists of intructions.
        prefix="Lấy ra thông tin ID tương ứng với sản phẩm. Lưu ý: chỉ cần đưa ra thông tin trích xuất được theo đúng format, không cần đưa ra thông tin nào khác. Dưới đây là 1 số ví dụ:",
        # The suffix is some text that goes after the examples in the prompt.
        # Usually, this is where the user input will go
        suffix="Thông tin của sản phẩm: {command}\n. Thông tin trích xuất được từ sản phẩm:",
        # The input variables are the variables that the overall prompt expects.
        input_variables=["command"],
        # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
        example_separator="\n\n",
    )

    # print(few_shot_prompt.format(command="máy giặt hãng nào tốt"))

    chain = LLMChain(llm=create_model(idx), prompt=few_shot_prompt)

    return chain.run(command=text_input)



def extract_ID(idx: int, df) -> list: # process response from llm to get ID 
    results = []
    for idx, product in enumerate(df['Keyword'].iloc[: 10], start=1):
        try:
            response = llm_invoke(product, idx)
            print(response)
        except Exception as e:
            # logger_error.info(f"Model {idx} error occurred - Error: {e}")
            ID = None
        else:
            try:
                ID = response.split("\n\n")[-1].split(':')[1].strip()
                print(ID)
            except Exception as e:
                logger_error.info(f"Response returned is not correct format - Response: {response}")
                ID = None
        finally:
            results.append(ID)



def run_mutil_threading(functions: list):
    threads = []

    for func in functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()


def main(folder_name: str): 
    functions = []

    for idx, df_name in enumerate(os.listdir(folder_name), start=1):
        logger_file.info(f"Folder name: {folder_name} - {df_name} file has been made")
        path_df = os.path.join(folder_name, df_name)
        df = pd.read_csv(path_df, skiprows=[0, 1], encoding="utf-16", delimiter='\t')
        functions.append(extract_ID(idx, df))

    run_mutil_threading(functions)


if __name__ == "__main__":
    folder_name = "data"
    # main(folder_name)
    df = pd.read_csv("data/sample.csv", skiprows=[0, 1], encoding="utf-16", delimiter='\t')
    response = llm_invoke(df['Keyword'].iloc[0], 1)
    print(response)
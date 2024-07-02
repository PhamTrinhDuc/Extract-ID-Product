from langchain_groq import ChatGroq
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.chains import LLMChain
import pandas as pd
import os
import threading
from config.config import get_config
from fewshort_examples import examples_prompt
from logs.set_logging import set_logging_error, set_logging_file


config = get_config()
logger_error = set_logging_error() # sử dụng để ghi log lỗi 
logger_file = set_logging_file() # sử dụng để ghi log các file đã xử lí 


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



def extract_ID(idx: int, df, df_name: str) -> list: # process response from llm to get ID 
    results = []
    for product in df['Keyword']:
        try:
            response = llm_invoke(product, idx)
            # print(response)
        except Exception as e:
            logger_error.info(f"MODEL {idx} ERROR OCCURRED: {e}")
            ID = None
        else:
            try:
                ID = response.split("\n\n")[-1].split(':')[1].strip()
                # print(ID)
            except Exception as e:
                logger_error.info(f"RESPONSE ERROR: {response}")
                ID = None
        finally:
            results.append(ID)

    if len(results) == len(df):
        df["model"] = results
        os.makedirs("out_data", exist_ok=True)
        df.to_excel(os.path.join("out_data", df_name))

def mutil_threading(functions_with_args: list[tuple]):
    threads = []
    for func, args in functions_with_args:
        thread = threading.Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    
    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

def run(list_name: list): 
    functions_with_args = []

    for idx, df_path in enumerate(list_name, start=1):
        df = pd.read_excel(df_path)
        df_name = df_path.split("/")[1]
        # logger_file.info(df_name)
        functions_with_args.append((extract_ID, (idx, df, df_name)))

    mutil_threading(functions_with_args)

# list_name = [
#     "data/Bàn chải điện_20240701.xlsx",
#     "data/Bàn phím máy tính_20240701.xlsx"
# ]
# run(list_name)
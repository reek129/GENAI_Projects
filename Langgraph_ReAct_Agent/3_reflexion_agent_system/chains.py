from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion, RevisedAnswer
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
# from execute_tools import ResponderWithRetries
# from dotenv import load_dotenv
# load_dotenv()


pydantic_parser = PydanticToolsParser(tools=[AnswerQuestion])

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researcher.
            Current time: {time}

            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            3. After the reflection, **list 1-3 search queries separately** for researching improvements.
            Do not include them inside the reflection.
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(  # Partial method is to prepoppulate the place holders before invoking a particular chain
    time = lambda:datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = "Provide a detailed ~150 words answer"
)

llm = ChatOpenAI(model="gpt-3.5-turbo")

first_responder_chain = first_responder_prompt_template | llm.bind_tools(
tools=[AnswerQuestion],tool_choice="AnswerQuestion"
) 

validator = PydanticToolsParser(tools=[AnswerQuestion])

# first_responder = ResponderWithRetries(
#     runnable=first_responder_chain, validator=validator
# )

# response = first_responder_chain.invoke(
#     {
#         "messages" :[HumanMessage(
#             content = "Write me a blog post on how small business can leverage AI to grow"
#         )]
#     }
# )


# print(response)

# Revisor Section

revise_instructions = """Revise your previous answer using the new information.
- You should use the previous critique to add important information to your answer.
  - You MUST include numerical citations in your revised answer to ensure it can be verified.
  - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
    - [1] https://example.com
    - [2] https://example.com
- You should use the previous critique to remove superfluous information from your answer and 
make SURE it is not more than 250 words.
"""

revisor_chain = actor_prompt_template.partial(
    first_instruction = revise_instructions
) | llm.bind_tools(tools=[RevisedAnswer],tool_choice="RevisedAnswer")

# revision_validator = PydanticToolsParser(tools=[RevisedAnswer])

# revisor = ResponderWithRetries(runnable=revisor_chain, validator=revision_validator)
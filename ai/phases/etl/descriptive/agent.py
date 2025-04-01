import os
import sys

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.descriptive.context import DataContext
from ai.phases.etl.descriptive.tools import create_tools
from ai.phases.etl.descriptive.prompts import AGENT_WORKFLOW


class NumericDescriptiveAgent:
    def __init__(self):
        self.context = DataContext()
        self.tools = create_tools(self.context)
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Prompt simple: solo system + input
        prompt = ChatPromptTemplate.from_messages([
            ("system", AGENT_WORKFLOW),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Crear agente con función calling
        agent = create_openai_functions_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        # Executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

    def execute(self, user_input: str = "Comienza el análisis descriptivo numérico."):
        result = self.executor.invoke({"input": user_input})
        return result["output"]




def main():
    agent = NumericDescriptiveAgent()
    result = agent.execute()
    print(result)


if __name__ == "__main__":
    main()

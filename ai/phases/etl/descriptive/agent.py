import os
import sys

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

class DescriptiveAgent:
    def __init__(self, data_context, tools, agent_workflow):
        """Initialize the LLM Agent

        Args:
            data_context (DataContext): The global state that the agent manipulate.
            tools (List[functions]): The tool kits that the agent will use.
            agent_workflow (str): The initial prompt
        """
        self.context = data_context
        self.tools = tools
        self.workflow = agent_workflow
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        # Prompt simple: solo system + input
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.workflow),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Crear agente con función calling
        agent = create_openai_functions_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        # Executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=100,  
            max_execution_time=None,
        )

    def execute(self, user_input: str="Comienza el análisis descriptivo numérico."):
        result = self.executor.invoke({"input": user_input})
        return result["output"]

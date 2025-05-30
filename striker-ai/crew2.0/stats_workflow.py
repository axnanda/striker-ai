#  Authors: Alexander Nanda, Levon Sarian, and Joseph Cruz
#  Improvements to be made:
#  1. PDF rag based upon Statlink DB
#  2. Recursive search for stats

import os
#import agentops

from crewai import Agent
from crewai import Crew
from crewai import Process
from crewai import Task
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import YoutubeChannelSearchTool
from crewai_tools import WebsiteSearchTool
from langchain.agents import initialize_agent, load_tools
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
# from langchain_community.tools import SceneXplainTool
import os

'''p
arams = {
    "engine": "google",
    "gl": "us",
    "hl": "en",
}
search_tool = SerpAPIWrapper(params=params)
'''

search_tool = SerperDevTool() 
scraping_tool = SeleniumScrapingTool()
video_tool = YoutubeChannelSearchTool()
website_rag_tool = WebsiteSearchTool(website='https://247sports.com/')
#vision_tool = SceneXplainTool()
maxpreps_tool = WebsiteSearchTool(website='https://www.maxpreps.com/')
espn_tool = WebsiteSearchTool(website='https://www.espn.com/college-football/')
buckeyes_tool = WebsiteSearchTool(website='https://www.si.com/college/ohiostate/football')


# Player for the crew to run
playerInfo = """
KJ Bolden
"""

json_report_validator = Agent(
  role='JSON Validator and creator',
  goal=f'Take all of the information passed to this agent and turn it into json fields for each category.', 
  backstory="Expert in turning text to json fields and outputting the final report in json format",
  tools=[],
  allow_delegation=True, 
  verbose=True, 
  memory = True,
)

master_report_gen = Agent(
  role='Master Report Generator',
  goal=f'Take all of the information passed back to this agent and create a well-formatted report that includes all of the in-depth reserach generated by each respective category.', 
  backstory="You are a expert reporter that specializes in generating in-depth reports",
  tools=[],
  allow_delegation=True, #might want to change this later
  verbose=True, 
  memory = True,
)

### Start of Summary Branch
## Basic Searching Loop

# Expert searcher based upon the given playerInfo. 
master_searcher = Agent(
  role='Master Basic Searcher Executor',
  goal=f'Find sports information online relevent to this specific player using their info: KJ Bolden, Football',
  backstory="You are an expert in searching for specific information and statistics for particular sports players. You have been in this industry for 25 years and you recieve a tip for every relevant, informative, or interesting fact you find about a specific sports player",
  tools=[search_tool],
  allow_delegation=True,
  max_iter=10,
  memory = True,
)

# Search Query Agent

master_search_brancher = Agent(
  role='Master Search Query Brancher',
  goal=f'Take the search results from the Mark, Master Basic Search Executor and pass this information off to each of the Category Managers including Social Meida, Highlights, Stats, and Recursive for KJ,Bolden,Football,S,2024,9,5,190 lbs,6 foot 2 inches,4160 likes.',
  backstory="You are an expert in relaying information to other Agent Category Managers and give them basic search results so that each Manager can conduct in-depth reserach.",
  tools=[],
  allow_delegation=True,
  verbose=True, 
  max_iter=5,
  memory = True,
)


## End of basic searching loop
## Start of Stats Branch
stats_category_manager = Agent(
    role = 'Stats Category Manager',
    goal = 'Using this info: KJ,Bolden,Football. Effectivly coordinate all the agents in the Stats branch and execute tasks effeciently',
    backstory="Expert in coordinatng and managing agents. Expert in delegating tasks to correct agents",
    tools=[], 
    verbose = True,
    memory = True, 
    max_iter=2,
    allow_delegation = True
)

# Teams
team_stats_finder = Agent(
    role = 'Team Stats Finder',
    goal = 'Using this info: KJ,Bolden,Football. Look up information on the teams that the player has played for and find specific stats relevant to them and recursively search based upon your search results until you have a comprehensive list of stats',
    backstory="You are an expert in finding team stats and finding specific stats relevant to the player's team preformance",
    tools=[espn_tool, maxpreps_tool, buckeyes_tool, search_tool, website_rag_tool, scraping_tool], 
    verbose = True,
    memory = True, 
    max_iter=2,
    allow_delegation = True
)

# Matcehs
match_stats_finder = Agent(
    role = 'Match Stats Finder',
    goal = 'Using this info: KJ,Bolden,Football. Look up quantitative information on the matches that the player has played for and find specific stats relevant to them',
    backstory="You are an expert in finding match stats and finding specific stats relevant to the player's individual preformance in matches played",
    tools=[espn_tool, maxpreps_tool, buckeyes_tool, search_tool, website_rag_tool, scraping_tool], 
    verbose = True,
    memory = True, 
    max_iter=2,
    allow_delegation = True
)
general_stats_finder = Agent(
    role = 'General Stats Finder',
    goal = 'Using this info: KJ,Bolden,Football. Look up general quantitative stats about the player',
    backstory="You are an expert in finding stats and finding specific stats relevant to the player's individual preformance",
    tools=[espn_tool, maxpreps_tool, buckeyes_tool, search_tool, website_rag_tool, scraping_tool], 
    verbose = True,
    memory = True, 
    max_iter=2,
    allow_delegation = True
)
## End of Stats Branch

# Stats Summary
stats_summary = Task(
  description=f'Generate a comprehensive summary of statistics using all of the agents in the stats media branch for this info: KJ,Bolden,Football. You must search the internet for information.',
  expected_output='You output an extremely comprehensive report that includes all of the research findings within the stats  branch',
  agents=[team_stats_finder, stats_category_manager, match_stats_finder],
  context=[],
  async_execution=False,
)
information_accuracy_consultor = Agent(
    role = 'Information Accuracy Consultor',
    goal = 'Check over all the information generated by the master_report task. Make sure it is all accurate and if it is not remove it',
    backstory='You are an expert reviewer and fact checker for recruited athletes',
    tools=[search_tool], 
    verbose = True,
    memory = True, 
    max_iter=10,
    allow_delegation = True
)
# Overall Report 
master_report = Task(
  description=f'Generate a master report that is very detailed and long and includes all of the information from each of the category branches for this player: KJ,Bolden',
  expected_output='You output JSON that includes all of the information from the comprehensive player summary ',
  agents=[master_report_gen],
  context=[stats_summary],
  async_execution=False,
)

# Writing task with language model configuration
output_validation = Task(
  description=f'Convert the final report into json, breaking each category into different fields for this player: KJ, Bolden',
  expected_output='You output JSON that includes all of the information from the comprehensive player summary report',
  agents=[json_report_validator],
  context=[master_report],
  async_execution=False,
  output_file='eval_timestamp.json'  
)

# Forming the tech-focused crew with enhanced configurations
crew = Crew(
    # may need to delete blockchain stuff???
  agents=[ master_searcher, master_report_gen, team_stats_finder, stats_category_manager, match_stats_finder, information_accuracy_consultor, general_stats_finder ],
  tasks=[stats_summary, master_report, output_validation, ],
  manager_llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
  # later return back to this and change again to be sure that the modoel is the best
  process=Process.hierarchical,
)
# Starting the task execution process with enhanced feedback
result = crew.kickoff()
print(result)
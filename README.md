# Striker AI

Striker AI is a modular system for **multi-modal Retrieval-Augmented Generation (RAG)**. It ties together large language models (LLMs), web search, visual and audio analysis, and vector-based retrieval to answer queries using up-to-date information. 

## Features

- **Multi-provider LLM support**: Use models via OpenAI, Groq, or Cerebras with a unified interface.
- **Vision & Audio Analysis**: BLIP-2 for image captioning, Whisper for audio transcription.
- **Universal RAG**: Stores text, image captions, and transcripts in a vector DB (Chroma) for semantic search:contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}.
- **Web Scraping**: Google/Bing search (via SerpAPI) and browser-based scraping (Playwright) including social media.
- **Configurable & Containerized**: Docker and docker-compose for easy deployment.
- **MLflow Integration (optional)**: Log inference outputs, embeddings, and artifacts for experiment tracking.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/striker-ai.git
   cd striker-ai


```

# dsa-tds-scraper and PDF Analysis of Wyscout Documents (scroll down for PDF analysis!!)

## Features
- **division, week, league info**
- **Batched and Unbatched Processing**
- **Logging**
- **Customizable Output**
- **input data-scraping**

## Requirements
- Python 3.x
- Pandas
- lxml
- argparse
- selenium

## Installation
1. Ensure that Python 3.x is installed on your system and copy repo.
2. Install the required packages (see each package's webpage for other details or run pip install package_name )

## Usage 
Navigate to the project directory in your terminal or command prompt, and run the script using the following command format:

``` python pre_processing.py ```
 - running this script will fetch the most recent week's information from topdrawersoccer.com
 - this should be run every week, and running this again will overwrite the previously stored most recent week's information
 - after this is run and you have up-to-date infomration, run the following

``` python processing.py <gender> <division> <batched> ```

```<gender>``` The gender of the request you want to process. Either m or w depending on the mens or womens league.

```<division>``` The soccer division you want to process. Choose from:
    - d1: Division 1
    - d2: Division 2
    - d3: Division 3
    - naia: NAIA
    - njcaa: NJCAA
    - all: All divisions

```<batched>```
True: Output in batched format (separate files for each week and division).
False: All data consolidated in a single file.

## Examples
Process all weeks and divisions, and save in batched format:

``` python processing.py f all True ```

Process all weeks of division d1, and save in a single file:

```python processing.py m d1 False ```

## Output
The processed data is saved in the outputs directory. The naming convention of the output files depends on your specified options:

Batched: <division>_week<week_number>_data_batch_<batch_id>.csv
Unbatched: <division>_unbatched_<batch_id>.csv for specific divisions or all_unbatched_<batch_id>.csv for all divisions.
Each CSV file contains the following columns:

Home Team
Away Team
Home Goals
Away Goals
Home Team Conference
Away Team Conference
Week
Division


## PDF Analysis of Wyscout Documents

### Features
- **Analysis of Wyscout PDFs for goals, duels, and passing statistics.**
- **Customizable PDF input paths.**
- **Automated data extraction and formatting.**
- **Timestamped JSON outputs for easy tracking and reference.**

### Preparing for Analysis
Before running the analysis scripts, ensure that the PDF files you want to analyze are available in the designated directory or modify the paths in the scripts accordingly. The PDF paths can be set on specific lines in each script.

### Usage
First, ensure that you have installed the proper pip packages for the scripts to run. This includes pdfplumber.
Run the following scripts in your terminal or command prompt for analyzing different aspects of the Wyscout documents:

1. **Goals Analysis:** 
   ```python goals.py```
   - Modify the PDF paths in `goals.py` on line 82.
   - Outputs a JSON file with goal-related statistics.

2. **Duels Analysis:** 
   ```python duels.py```
   - Modify the PDF paths in `duels.py` on line 83.
   - Outputs a JSON file with duel-related statistics.

3. **Passing Analysis:** 
   ```python passing.py```
   - Modify the PDF paths in `passing.py` on line 86.
   - Outputs a JSON file with passing-related statistics.

Each script processes the specified PDFs and outputs the results in a JSON format. The JSON files are timestamped for convenience and easy identification.

### Output
The scripts generate JSON files containing detailed statistical data extracted from the PDFs. These files are saved in the same directory as the scripts and are named using the following convention:

- For goals: `combined_goals_tables_<timestamp>.json`
- For duels: `combined_duels_tables_<timestamp>.json`
- For passing: `combined_passing_tables_<timestamp>.json`

The timestamp in the file name represents the date and time when the analysis was run, ensuring that each output is uniquely identifiable.
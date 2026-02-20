# news_handler v3.0.1


News Handler is a lightweight system for fetching articles from news websites, categorizing them, and storing them in a database for structured access and long-term use. Its purpose is to help me in my exam preperations by maintaining a record of news that is important for subjective exams.

The project is designed to automate personal news collection by centralizing articles, organizing them using rule-based categorization, and persisting them reliably. It serves as the foundation for a future API-driven service to manage news-related tasks remotely.

This system can easily be modified to suit individual needs like tracking buisness related news, or stock market news, or a blog. (Only requirement is that they should support [RSS](https://en.wikipedia.org/wiki/RSS) or else you have to use RSS genertor websites).

## Current Capabilities

- Fetches articles from news sources
- Categorizes articles based on predefined rules
- Stores articles in a database for structured access
- Maintains local backups for reliability

## Planned Features

- An API for remote article and task management
- AI-driven article summarization
- Automatic storage of summaries in an Obsidian vault
- Smarter automation for end-to-end news handling

## Tech Stack

- Python  
- MongoDB  

*Updates coming soon!*

# Documentation
Step by step to run the project (as it is) with setup instructions, configuration details & execution workflow:

[How to run the project](https://github.com/1-noob/news_handler/blob/main/docs/how_to_run.md)

## API Documentation    
# Sentinel & Sage
This is a repo that records my journey as I learn to design and build a dual-agent CLI-driven security research tool with UI designed using Python's textual library.

This project is designed to be an exercise in developing my skills in security research, programming, and to dive into the world of understanding agentic solutions. I have learned how to design and build modern project infrastructure using uv and the importance of using .gitignore to secure keys and keep a repo clean of files that are unnecessary or that may contain sensitive information (user log files, settings, etc)

I used Anthropic's documentation to get a high-level understanding of Basic Multi-LLM workflows, how to write effective tools for AI agents, how to build effective agents, and Anthropic's Agent SDK overview to get quick practical experience building production agents with Claude Code. I Learned about managing Python projects using uv via realpython.com, and I used modelcontextprotocol.io to learn about MCP servers.

My programming experience has mostly been academic up to this point. This is my first attempt at building anything significant beyond the classroom fundamentals. I have made an attempt to use this project as a learning opportunity in further developing my skills as a programmer. I have used Claude to help produce code when I am either lost under the premise that it provide a lesson each time that I prompt it to generate a solution or when the efficiency outweighs the benefit of typing something mundane/simple. 


## Global deps
Before building the environment, ensure that you install tshark, nmap, and uv. This has been entirely designed and built on Ubuntu 24.04.
- `sudo apt install tshark`
- `sudo apt install nmap`
- `curl -LsSf http://astral.sh/uv/install.sh | sh`

## Set up
`uv venv`
`source .venv/bin/activate`
`uv sync --dev` to set up using all dev deps or simply:
`uv sync` to set up as a user

## Run
after initial uv sync:
`source .venv/bin/activate`
then `uv run sent-and-sage`

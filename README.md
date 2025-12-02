# MCP Agent Project

This project implements a **Model Context Protocol (MCP) AI agent** that can interact with platforms like YouTube via a backend server exposing MCP tools.

The project includes:

- **Backend:** FastAPI MCP server exposing YouTube-style tools (search, like, recommend)
- **Frontend:** Next.js web app to demonstrate search and tool usage
- **Agent:** Python script using an LLM to generate recommendations and invoke MCP tools
- **Utils:** Helper modules for logging and YouTube API interactions

---

## Table of Contents

1. [Setup](#setup)
2. [Backend](#backend)
3. [Frontend](#frontend)
4. [Agent](#agent)
5. [Deployment](#deployment)
6. [Environment Variables](#environment-variables)
7. [Extending](#extending)
8. [Security Notes](#security-notes)

---

## Setup

Clone the repo:

```bash
git clone https://github.com/saikrishnavarmauppalapati/mcp-agent-repo
cd mcp-agent-project

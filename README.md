## Global Air Quality Dashboard
Initially tired to vibe code this whole project using a range of different agents and tools. It has started off a mess, but set myself the challenge of fixing it from a very broken stage to back to what I want.

Using marimo notebooks to test out the API calls and the data I get back to go from there. Have also decided to move from the requests library to httpx after being recommended to try it.

Using uv for dependency management
```
uv sync
```
This will sync after downloading this mess of a project
```
uv add
```
This adds any new dependencies you need
```
uv run marimo edit api_test.py
```
This opens up the marimo notebooks to do some work in
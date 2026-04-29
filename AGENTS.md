# AGENTS.md — AI Usage During Development

## Where AI Helped

**Project Structure** — Claude helped design the overall project structure. it split the logic into `src/` modules and set up the `tests/` directory. This saved a lot of time let me focus on the actual functionality.

**MLB Stats API integration** — Claude knew the MLB Stats API structure, which allowed me to learn the basics that we were using instead of having to dig through unneeded instruction.

**Test design** — Claude introduced me to using `unittest.mock` and `MagicMock` to mock API responses in tests. This was genuinely new to me — I hadn't used mocking before and it made a big difference. Tests now run offline and don't depend on the API being available.

**Debugging** — I ran into several issues, and was able to debug for the most part using claude, most of the time being syntax or order of operations issues

## Where AI Steered Me Wrong 

**pybaseball turned out not to work** — Claude initially suggested using `pybaseball` as the data source, which we had troubles with. We pivoted to the MLB Stats API directly, which worked better anyway since it requires no API key.

**Default year was 2024** — Since alot of these AIs default to where there knowledge bank is from, we initially were getting 2024 stats just because i didnt catch it from the jump

**Vagueness** — Some of the things Claude would suggest were too vague if you didnt have baseball context. For example the leaders returned "AVG" and then a bunch of pitchers. If you dont know what baseball averages normally are, you would never be able to conclude what it was measuring

## What I Learned

This honestly showed me how much error there still is in LLMs and AI. My own knowledge of python and how these projects are supposed to work was just as, if not more important than my ability to use a chatbot here. We ran into alot of issues and if i didnt know how to articulate what the issue is and be able to work collaboratively with the AI, it wouldnt have worked.

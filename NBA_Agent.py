import anthropic
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

df = pd.read_csv("all_seasons.csv")

tools = [
    {
        "name": "get_top_players",
        "description": "Top N players by a stat. Optional season filter.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stat": {"type": "string"},
                "n": {"type": "integer"},
                "season": {"type": "string"}
            },
            "required": ["stat", "n"]
        }
    },
    {
        "name": "player_career",
        "description": "All seasons of stats for a specific player.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
        }
    }
]

def run_tool(name, inputs):
    if name == "get_top_players":
        data = df.copy()
        if inputs.get("season"):
            data = data[data["season"] == inputs["season"]]
        top = data.nlargest(inputs["n"], inputs["stat"])
        return top[["player_name", "season", inputs["stat"]]].to_json(orient="records")
    
    elif name == "player_career":
        player = df[df["player_name"].str.lower() == inputs["name"].lower()]
        if player.empty:
            return "Player not found"
        return player[["season", "pts", "reb", "ast"]].to_json(orient="records")

def ask_agent(question):
    messages = [{"role": "user", "content": question}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            system="""You are an NBA analyst with access to historical stats.

            The dataset uses these column names (use exactly these, not full words):
            - pts (points per game)
            - reb (rebounds per game)
            - ast (assists per game)
            - net_rating, ts_pct, usg_pct (advanced stats)
            - player_name, season, team_abbreviation

            Always use the exact column abbreviations above when calling tools.""""" ,
            
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            print(response.content[0].text)
            break

        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  → {block.name}({block.input})")
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input)
                })
        messages.append({"role": "user", "content": results})

ask_agent("Who were the top 5 scorers in 2023-24?")

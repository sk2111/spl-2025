
import asyncio
import json
import os
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from collections import defaultdict
import itertools
from datetime import datetime
from pathlib import Path

import websockets

from openai import AsyncOpenAI
from pydantic import BaseModel
from uuid import uuid4
from dotenv import load_dotenv
import time

from prompts import GAME_PROMPT
load_dotenv()
async def make_llm_call(prompt):
    no_of_tips = 5
    max_characters_per_tip = 140

    if not os.environ.get("OPENAI_API_KEY"):
        print(f"⚠️ OPENAI_API_KEY was not found in the environment.")

    # Single async OpenAI client
    client = AsyncOpenAI()

    MODEL_NAME = "gpt-5.1"
    REASONING_EFFORT = "low"   # "minimal""low" / "medium" / "high"
    VERBOSITY = "low"             # keep answers short/direct

    try:
        print("Making an LLM call")
        print(f"{prompt=}")
        
        
        # resp = await asyncio.wait_for(
        #     client.responses.parse(
        #         model=MODEL_NAME,
        #         input=[{"role": "user", "content": prompt}],
        #         reasoning={"effort": REASONING_EFFORT},
        #         text={"verbosity": VERBOSITY},
        #     ),
        # )
        
        start = time.perf_counter()

        resp = await asyncio.wait_for(
            client.responses.parse(   # <-- MUST have parentheses
                model=MODEL_NAME,
                input=[{"role": "user", "content": prompt}],
                reasoning={"effort": REASONING_EFFORT},
                text={"verbosity": VERBOSITY},
            ),
            timeout=35,
        )

        print("Elapsed:", time.perf_counter() - start)
        print("LLM call completed")
        return resp.output_text

    except asyncio.TimeoutError:
        print("Timeout reached: returning dummy response")
        return "DUMMY_RESPONSE"

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        raise

# async def main():
#     response = await make_llm_call(GAME_PROMPT)
#     print(response)

# if __name__ == "__main__":
#     asyncio.run(main())


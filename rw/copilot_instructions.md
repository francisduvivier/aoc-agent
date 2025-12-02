You need to create an llm coding agent that reads and solves advent of code puzzles.
- You should base the implementation on the instructions in this file and @./Coding_Agent_Implementation_Workbook.docx.md
- Make a commit every time after you edit a file saying what was done.
- Make sure that the agent that you make always creates commits as well
- the agent should read the public problem statement by doing a curl to the problem statment for the current year and date.
  - To help with that, you should create a function that does this call and processes it for the agent so that only the problem statement remains
- the agent code should create a directory for the current day and download the input file using a curl request with a session cookie that I have already put in the environment as AOC_SESSION_COOKIE=[value after session=]
- the agent should run in a docker environment, only having access to a mounted directory, for that purpose, a docker compose should be made.
- a scaffold should be created for the agent so that reading the input as lines and triming, and a part_1 solve_sample_input_1, etc is already provided and the agent can start from that.
- a function that the agent can use for submitting the solution should be given. The implementation of this function make sure that the input and the response is logged. And if the solution was not correct, the feedback should  be returned to the llm agent. And the function should also wait in a blocking and exponentially backing off fasion to prevent trying too many times.
- the agent should use opensearch, the api key is provided in the env as AOC_OPENROUTER_API_KEY, and you should use the grok 4.1 fast free model as the model for the agent.


If something is not clear, ask me.

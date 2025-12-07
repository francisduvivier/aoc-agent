# Things to improve

## Simple improvements
- we should use chat history instead of feeding the previous solution as user input.
- when the request is rate limited, it should not be handled like a failure, but instead, user interaction should be asked to continue.
 - also, if user interaction was requested and approved, it should never be rate limited.
 - So the whole rate limiting system should be reworked.
- the previous tries of results should be persisted and checked so that we never try to submit the same wrong answer again.
- We need to be able to set up an experiment that varies the temperature and then checks the result on 3 runs on 5 problems
- We need a controlled way to introduce some variation in the code that will not cause things like syntax errors
- Detect syntax errors and make special log for them
- code should be refactored so that code between part 1, 2 and verification is reused, the right abstractions are made and utility code is moved into another function.
- We should be able to mock out the AOC server to test our flows and agent without any interaction with the real system
- We should be able to mock out the LLM response to test our flows and agent code without any interaction with a real LLM


## Hard improvements
- We should be able to fire agents simultaneously, so we can get to a solution faster. The first agent that has met the criteria should submit the answer, and if it is correct, all other agents should stop. To achieve this. we should set something up so that the solution is written to a unique file per parallel agent, or that the generated python code is just evaluated from memory directly.

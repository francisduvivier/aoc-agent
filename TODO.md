# Things to improve

## Simple improvements
- when the request is rate limited, it should not be handled like a failure, but instead, user interaction should be asked to continue.
 - also, if user interaction was requested and approved, it should never be rate limited.
 - So the whole rate limiting system should be reworked.
- the previous tries of results should be persisted and checked so that we never try to submit the same wrong answer again.
- We need to be able to set up an experiment that varies the temperature and then checks the result on 3 runs on 5 problems
- We need a controlled way to introduce some variation in the code that will not cause things like syntax errors
- Detect syntax errors and make special log for them


## Hard improvements
- We should be able to fire agents simultaneously, so we can get to a solution faster. The first agent that has met the criteria should submit the answer, and if it is correct, all other agents should stop. To achieve this. we should set something up so that the solution is written to a unique file per parallel agent, or that the generated python code is just evaluated from memory directly.

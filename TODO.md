# Things to improve
- We should be able to fire agents simultaneously, so we can get to a solution faster. The first agent that has met the criteria should submit the answer, and if it is correct, all other agents should stop. To achieve this. we should set something up so that the solution is written to a unique file per parallel agent, or that the generated python code is just evaluated from memory directly.
- The agent should be informed that it can add debug statements before the final solution. To differentiate, we should change it so that the sample solution is printed as "---- [Sample/Final] Solution Part [1/2]: [solution] ----". To allow this, we should change our code so that the output is parsed for this format.
- when the request is rate limited, it should not be handled like a failure, but instead, user interaction should be asked to continue.
 - also, if user interaction was requested and approved, it should never be rate limited.
 - So the whole rate limiting system should be reworked.
- Before sending a request to openrouter, the pricing should be checked, if input or output tokens cost more than 0.0001 per million tokens, the request should be skipped.
- Token usage counts should be logged in the console.
- README should be updated.
- Fix current day not being used automatically anymore.
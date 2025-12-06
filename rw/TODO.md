# Things that should be improved
- After every fetch of the input, the solutions dir for that day should be committed to git
- After every updating of the solution file by the agent, a commit should be made
- Part 1 and Part 2 should be solved in different files, and the agent should be instructed to only solve the part that is not yet solved. So if part 1 is not solved, the agent should only solve part 1, and if part 2 is not solved, the agent should only solve part 2.
- If Part 2 is already solved according to the site, the agent should try to solve it again, but the solution should never be submitted to the site, instead, the new solution should be compared to what is shown on the site, and if it is different, the agent should try to solve it again.
- If Part 2 is already solved, then the solution number should be hidden from the agent, so that it solves it in the same way that it would solve it if it was not solved yet.
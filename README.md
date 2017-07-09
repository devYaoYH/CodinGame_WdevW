# Legend #46

I'm a bit late to the party...got carried away making graphics for illustration, ended up writing as much code to generate the graphics as I did during contest time :sweat_smile: Messed around with python turtle graphics library and got some interactive simulation for Wondev working :P One in which you can play as the enemy! \o/ Still figuring out how to isolate it to read/write to other processes tho...the version I have now has my bot's python code embedded inside it XD

## Wood -> Gold
Only had time to work on this contest during the weekends this time round...almost didn't make it to legend >.< 
The ~200 lines of python I rushed out on the first weekend surprisingly got me from Wood II to Gold :astonished:

## Unsophisticated but somewhat effective
Some observations I made watching replays that made it into my initial strategy:

#### MOVE&BUILD
- Try to climb higher
- Build higher
- Don't waste time building higher than you can climb to
  - E.g. On 1, building 2 -> 3 would incur a penalty
- When moving from 3 -> 3, build lower (maximize time spent jumping around at height 3)
- When I have to build a 3 -> 4, I pick the one that gives maximum floodfill area
  - That is max accessible area when I run a BFS on the resulting state (allowing my bot to play a decent end-game)

#### PUSH&BUILD
- Push enemy lower

My early focus was on point-scoring and MOVE&BUILD action, not paying much attention to PUSH&BUILD. Even so, by scoring moves according to the above naive rules, my bot climbed straight from Wood to Gold league...

## Gold -> Legend
Climbing to legend required some more sophisticated code haha :P However, my final submit was also based on simply scoring the moves given as input...

### Enemy Tracking
After some debugging whilst generating the graphics, I now hesitate to call it 'enemy tracking'...more like scoring for 'best' enemy position.

The approach my bot took to tracking enemies was simply to overlay possible moves (from previous turn's predictions) against possible positions to build at the detected grid.

<img src="/uploads/default/original/3X/7/9/79301e7ebd57289cfc75baaf3c8f5d30b23b86d8.PNG" width="519" height="263">

So in the above image, enemy was at (3, 6) then moved to (2, 7) and built at (1, 7).

- **Green** are the possible grids the enemy could've built at (1, 7) from.
- **Red** are possible positions the enemy could've moved to from possible locations tracked the previous turn.
- **Yellow** are the overlapping positions (predicted enemy locations this turn).
- **Darker shades** of yellow and red are previous turn's predictions.

It becomes obvious that this won't work after a few moves where all 8 adjacent cells around the build location could've been moved to from the previous turn's guessed locations. However, with some pruning and cases of enemy pushes, the possibilities can be narrowed down.

- When (-1, -1) is read for enemy position, it actually provides information on where the enemy **is not**, namely, the cells adjacent to your units.
- When pushed, the enemy could be in 1 of 3 locations that gives the valid push-angle.

So with these two additional method of pruning in conjunction with the above 'tracking', my bot was able to guess the enemy's locations to a useful degree of accuracy.

### Voronoi Diagram
What's the use of tracking enemies? 

<img src="/uploads/default/original/3X/e/8/e8d56febb3479bf20cd5ae36de295073d4223e0d.PNG" width="519" height="263">
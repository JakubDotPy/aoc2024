# Day 14: Restroom Redoubt  
## Part One  

One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near  
an unvisited location on their list, and so you're all quickly teleported directly to the lobby  
of Easter Bunny Headquarters.  

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The  
area outside the bathroom is swarming with robots!  

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will  
be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight  
lines.  

You make a list (your puzzle input) of all of the robots' current positions (`p`) and velocities  
(`v`), one robot per line. For example:  

```  
p=0,4 v=3,-3  
p=6,3 v=-1,-3  
p=10,3 v=-1,2  
p=2,0 v=2,-1  
p=0,0 v=1,3  
p=3,0 v=-2,-2  
p=7,6 v=-1,-3  
p=3,0 v=-1,-2  
p=9,3 v=2,3  
p=7,3 v=-1,2  
p=2,4 v=2,-3  
p=9,5 v=-3,-3  
```  

### Robot Behavior  

- Each robot's position is given as `p=x,y` where `x` represents the number of tiles the robot is  
  from the left wall and `y` represents the number of tiles from the top wall.  
- Each robot's velocity is given as `v=x,y` where `x` and `y` represent the tiles moved per second.  
- Robots wrap around the edges of their space when they reach the boundary.  

In this example, the robots are in a space which is `11` tiles wide and `7` tiles tall.  

### Example Motion  

Here is what robot `p=2,4 v=2,-3` does for the first few seconds:  

**Initial State:**  

```  
...........  
...........  
...........  
...........  
..1........  
...........  
...........  
```  

**After 1 second:**  

```  
...........  
....1......  
...........  
...........  
...........  
...........  
...........  
```  

**After 5 seconds:**  

```  
...........  
...........  
...........  
.1.........  
...........  
...........  
...........  
```  

### Quadrant Analysis  

After `100` seconds, count the number of robots in each quadrant of the 101x103 space. Robots in  
the middle don't count toward any quadrant. Multiplying the counts of robots in the four quadrants  
gives a **safety factor**.  

For example, after `100` seconds:  

```  
......2..1.  
...........  
1..........  
.11........  
.....1.....  
...12......  
.1....1....  
```  

In this example:  

- Quadrants contain `1`, `3`, `4`, and `1` robots.  
- The safety factor is `1 * 3 * 4 * 1 = 12`.  

### Question  

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles  
tall. What will the safety factor be after exactly `100` seconds have elapsed?  

## Part Two  

During the bathroom break, someone notices that these robots seem awfully similar to ones built  
and used at the North Pole. If they're the same type of robots, they should have a hard-coded  
Easter egg: very rarely, most of the robots should arrange themselves into a picture of a  
**Christmas tree**.  

### Question  

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?  
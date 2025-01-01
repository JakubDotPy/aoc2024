# Day 16: Reindeer Maze  
## Part One  

It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where  
the Reindeer compete for the lowest score.  

You and The Historians arrive to search for the Chief right as the event is about to start. It  
wouldn't hurt to watch a little, right?  

The Reindeer start on the **Start Tile** (marked `S`) facing **East** and need to reach the  
**End Tile** (marked `E`). They can:  

1. **Move forward** one tile at a time (increasing their score by **1 point**).  
2. **Rotate** clockwise or counterclockwise 90 degrees (increasing their score by **1000 points**).  

The goal is to find the **lowest possible score** to traverse the maze.  

### Example Maze  

```  
###############  
#.......#....E#  
#.#.###.#.###.#  
#.....#.#...#.#  
#.###.#####.#.#  
#.#.#.......#.#  
#.#.#####.###.#  
#...........#.#  
###.#.#####.#.#  
#...#.....#.#.#  
#.#.#.###.#.#.#  
#.....#...#.#.#  
#.###.#.#.#.#.#  
#S..#.....#...#  
###############  
```  

The best path through this maze incurs a score of **7036**, achieved by:  

- Moving forward **36 steps** (36 points).  
- Rotating **7 times** (7 * 1000 = 7000 points).  

This path looks like this:  

```  
###############  
#.......#....E#  
#.#.###.#.###^#  
#.....#.#...#^#  
#.###.#####.#^#  
#.#.#.......#^#  
#.#.#####.###^#  
#..>>>>>>>>v#^#  
###^#.#####v#^#  
#>>^#.....#v#^#  
#^#.#.###.#v#^#  
#^....#...#v#^#  
#^###.#.#.#v#^#  
#S..#.....#>>^#  
###############  
```  

### Another Example  

```  
#################  
#...#...#...#..E#  
#.#.#.#.#.#.#.#.#  
#.#.#.#...#...#.#  
#.#.#.#.###.#.#.#  
#...#.#.#.....#.#  
#.#.#.#.#.#####.#  
#.#...#.#.#.....#  
#.#.#####.#.###.#  
#.#.#.......#...#  
#.#.###.#####.###  
#.#.#...#.....#.#  
#.#.#.#####.###.#  
#.#.#.........#.#  
#.#.#.#########.#  
#S#.............#  
#################  
```  

The best paths through this maze cost **11048 points**.  

### Question  

What is the **lowest score** a Reindeer could possibly get in your maze?  

---

## Part Two  

Now that you know the best paths through the maze, you can figure out the **best place to sit**.  

Each tile (`S`, `.`, `E`) has places to sit along its edges. The best place to sit is any tile  
that is **part of at least one of the best paths** through the maze.  

### Example  

In the first example, **45 tiles** (marked `O`) are part of the best paths:  

```  
###############  
#.......#....O#  
#.#.###.#.###O#  
#.....#.#...#O#  
#.###.#####.#O#  
#.#.#.......#O#  
#.#.#####.###O#  
#..OOOOOOOOO#O#  
###O#O#####O#O#  
#OOO#O....#O#O#  
#O#O#O###.#O#O#  
#OOOOO#...#O#O#  
#O###.#.#.#O#O#  
#O..#.....#OOO#  
###############  
```  

In the second example, **64 tiles** are part of the best paths:  

```  
#################  
#...#...#...#..O#  
#.#.#.#.#.#.#.#O#  
#.#.#.#...#...#O#  
#.#.#.#.###.#.#O#  
#OOO#.#.#.....#O#  
#O#O#.#.#.#####O#  
#O#O..#.#.#OOOOO#  
#O#O#####.#O###O#  
#O#O#..OOOOO#OOO#  
#O#O###O#####O###  
#O#O#OOO#..OOO#.#  
#O#O#O#####O###.#  
#O#O#OOOOOOO..#.#  
#O#O#O#########.#  
#O#OOO..........#  
#################  
```  

### Question  

How many tiles are part of at least one of the best paths through your maze?  
# Day 15: Warehouse Woes  
## Part One  

You appear back inside your own mini submarine! Each Historian drives their mini submarine in  
a different direction; maybe the Chief has his own submarine down here somewhere as well?  

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they  
seem quite anxious, so you drive your mini submarine over to see if you can help.  

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be  
stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated  
by robots!  

These lanternfish seem so anxious because they have lost control of the robot that operates one  
of their most important warehouses! It is currently running amok, pushing around boxes in the  
warehouse with no regard for lanternfish logistics or lanternfish inventory management strategies.  

### Robot Behavior  

- The robot attempts to move according to a sequence of commands (`<`, `>`, `^`, `v` for left,  
  right, up, and down).  
- If a box (`O`) is in the way, the robot pushes it.  
- If pushing a box would cause it or the robot to move into a wall (`#`), nothing moves.  

The robot begins at its initial position (`@`) in a warehouse map, with boxes, walls, and open  
spaces (`.`).  

### Example  

```  
########  
#..O.O.#  
##@.O..#  
#...O..#  
#.#.O..#  
#...O..#  
#......#  
########  
```  

Commands: `<^^>>>vv<v>>v<<`  

#### Robot and Box Movement  

1. **Initial state:**  
   ```  
   ########  
   #..O.O.#  
   ##@.O..#  
   #...O..#  
   #.#.O..#  
   #...O..#  
   #......#  
   ########  
   ```  

2. **Move `<`:** (Robot cannot move left into a wall.)  
   ```  
   ########  
   #..O.O.#  
   ##@.O..#  
   #...O..#  
   #.#.O..#  
   #...O..#  
   #......#  
   ########  
   ```  

3. **Move `^`:** (Robot moves up.)  
   ```  
   ########  
   #.@O.O.#  
   ##..O..#  
   #...O..#  
   #.#.O..#  
   #...O..#  
   #......#  
   ########  
   ```  

4. **Move `^`:** (Robot cannot move further up into a wall.)  
   ```  
   ########  
   #.@O.O.#  
   ##..O..#  
   #...O..#  
   #.#.O..#  
   #...O..#  
   #......#  
   ########  
   ```  

5. **Move `>`:** (Robot moves right and pushes a box.)  
   ```  
   ########  
   #..@OO.#  
   ##..O..#  
   #...O..#  
   #.#.O..#  
   #...O..#  
   #......#  
   ########  
   ```  

6. **Continue Commands:** (Robot follows the sequence to rearrange boxes.)  

After all moves, the resulting warehouse layout shows the new positions of the boxes.  

### GPS Calculation  

Each box has a **GPS coordinate** calculated as:  

\[ \text{GPS coordinate} = 100 \times (\text{distance from top}) + (\text{distance from left}) \]  

The sum of all boxes' GPS coordinates is the answer for Part One.  

## Part Two  

The lanternfish use your information to determine when to disable the robot. However, a second  
warehouse with double-width features has been reported.  

### Rescaled Warehouse  

- Boxes (`O`) are now represented as `[]`.  
- Walls (`#`) and spaces (`.`) are doubled in width.  
- The robot (`@`) remains unchanged but interacts with double-width tiles.  

Commands remain the same.  

#### Rescaled Example  

```  
################  
##....[]....[]##  
##..............##  
##..[][]....[]..##  
##....[]@.....[]##  
##[]##........[]##  
##[]..........[]##  
##..[][]..[][][]##  
##........[]....##  
################  
```  

### GPS Adjustment  

For double-width boxes, measure GPS coordinates from the **nearest edge** of the box.  

Predict the motion of the robot and boxes in this new, scaled-up warehouse. Calculate the sum  
of all boxes' final GPS coordinates.  
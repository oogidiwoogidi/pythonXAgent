---
mode: agent
---

# Brick Breaker Game Development Plan

## Project Overview

Create a classic brick breaker game where players control a paddle to bounce a ball and break bricks.

## Development Process

### 1. Establish Game Framework

- Extract the basic pygame framework from `class3\class3-2.py`
- Organize and place the framework code into `class3\class3-4.py`
- Ensure inclusion of basic structures such as game window initialization, event handling, and main loop

### 2. Define Game Constants

**Window Settings:**

- `WINDOW_WIDTH = 800`: Window width
- `WINDOW_HEIGHT = 600`: Window height
- `FPS = 60`: Game frame rate

**Game Object Parameters:**

- `BALL_RADIUS = 10`: Ball radius
- `BALL_SPEED = 5`: Ball movement speed
- `PADDLE_WIDTH = 100`: Paddle width
- `PADDLE_HEIGHT = 15`: Paddle height
- `PADDLE_SPEED = 8`: Paddle movement speed
- `BRICK_WIDTH = 75`: Brick width
- `BRICK_HEIGHT = 30`: Brick height
- `BRICK_ROWS = 6`: Number of brick rows
- `BRICK_COLS = 10`: Number of brick columns

**Color Constants:**

- Define various color constants (WHITE, BLACK, RED, GREEN, BLUE, etc.)
- `BRICK_COLORS`: List of brick colors

### 3. Design Game Objects

#### Brick Object

**Attributes:**

- `rect`: pygame.Rect object defining the position and size of the brick
- `color`: Brick color
- `is_hit`: Boolean value marking whether the brick has been hit

**Methods:**

- `__init__(x, y, color)`: Initialize brick object
- `draw(screen)`: Draw the brick on canvas (with border)
- `check_collision(ball)`: Check if the ball collides with the brick
- `destroy()`: Handle brick destruction when hit

#### Paddle Object

**Attributes:**

- Inherits basic structure from Brick object
- Reset width and height to paddle dimensions
- Color set to white

**Methods:**

- `__init__(x, y)`: Initialize paddle object
- `move(mouse_x)`: Update paddle position based on mouse X coordinate, centering paddle to mouse position

### 4. Game Main Loop Integration

#### Event Handling

- Handle window close events
- Handle mouse movement events to control the paddle

#### Screen Rendering

- Clear screen background
- Draw brick and paddle objects
- Update screen display

#### Code Optimization

- Use block comments to separate different functional sections
- Maintain clear and readable code structure

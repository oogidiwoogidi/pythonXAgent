# Visual Enhancement Mod Pack - Asset Guidelines

## Adding Custom Graphics

### Sprite Requirements:
- **Player Sprites**: 40x40 pixels, PNG format with transparency
- **Enemy Sprites**: 40x40 pixels, PNG format with transparency  
- **Weapon Sprites**: 30x8 pixels for rifles, 20x12 for pistols
- **Bullet Sprites**: 8x4 pixels with glow effects
- **Platform Textures**: Variable width, 20px height

### File Organization:
```
assets/
├── sprites/
│   ├── player1.png
│   ├── player2.png
│   ├── enemy.png
│   └── weapons/
│       ├── rifle.png
│       └── pistol.png
├── textures/
│   ├── platform.png
│   └── backgrounds/
│       ├── space.png
│       └── city.png
├── effects/
│   ├── explosion_frames/
│   ├── muzzle_flash/
│   └── particles/
└── ui/
    ├── crosshair.png
    ├── health_bar_bg.png
    └── weapon_icons/
```

### Integration:
1. Place your custom images in the appropriate folders
2. Update the sprite_manager.load_sprite() calls in sprite_system.py
3. The system will automatically fall back to generated sprites if files are missing

### Color Schemes:
- **Player 1**: Black/Dark Gray (#000000, #333333)
- **Player 2**: Blue/Cyan (#0080FF, #00FFFF)  
- **Enemy**: Red/Orange (#FF0000, #FF8C00)
- **Explosions**: Orange/Yellow (#FF8C00, #FFFF00)
- **UI Elements**: White/Gray (#FFFFFF, #CCCCCC)

### Performance Tips:
- Keep sprite files under 50KB each
- Use indexed color mode for better performance
- Avoid too many animation frames (max 8 per animation)

"""
Visual Enhancement Mod Pack Installer

This script installs and configures the visual enhancement mod packs
for the 2D Platform Shooter game.
"""

import os
import shutil


def install_visual_mod_packs():
    """Install all visual enhancement mod packs."""
    print("🎮 Installing Visual Enhancement Mod Packs...")

    # Check if all mod files exist
    mod_files = ["src/visual_effects.py", "src/sprite_system.py", "src/enhanced_ui.py"]

    missing_files = []
    for file in mod_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Missing mod files:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ All mod pack files found!")

    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
        print("📁 Created assets directory")

    # Create subdirectories for organized assets
    asset_dirs = ["assets/sprites", "assets/textures", "assets/effects", "assets/ui"]

    for dir_path in asset_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 Created {dir_path}")

    print("\n🎨 Visual Enhancement Mod Packs Installed Successfully!")
    print("\n📋 Mod Pack Features:")
    print("   ⭐ Particle Effects System")
    print("      - Explosions and muzzle flashes")
    print("      - Bullet trails and blood spatters")
    print("      - Jump dust and environmental effects")
    print("   ⭐ Enhanced Sprite System")
    print("      - Procedurally generated character sprites")
    print("      - Weapon and bullet graphics")
    print("      - Textured platforms")
    print("   ⭐ Advanced UI System")
    print("      - Animated backgrounds (space/city)")
    print("      - Floating damage indicators")
    print("      - Enhanced crosshair and weapon HUD")
    print("      - Mini-map display")
    print("   ⭐ Screen Effects")
    print("      - Screen shake on impacts")
    print("      - Flash effects on damage")
    print("      - Enhanced health bars with gradients")

    print("\n🎮 Your game now has enhanced visuals!")
    print("   Run the game to see all the new effects in action!")

    return True


def create_asset_guidelines():
    """Create guidelines for adding custom assets."""
    guidelines = """# Visual Enhancement Mod Pack - Asset Guidelines

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
"""

    with open("VISUAL_MOD_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guidelines)

    print("📝 Created VISUAL_MOD_GUIDE.md with asset guidelines")


if __name__ == "__main__":
    print("=" * 60)
    print("🎮 2D Platform Shooter - Visual Enhancement Mod Pack")
    print("=" * 60)

    if install_visual_mod_packs():
        create_asset_guidelines()
        print("\n🚀 Ready to play with enhanced visuals!")
    else:
        print("\n❌ Installation failed. Please check missing files.")

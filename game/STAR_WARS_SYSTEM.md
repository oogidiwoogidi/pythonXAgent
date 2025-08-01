# Star Wars Character Selection System - Implementation Guide

## 🌟 New Features Added

### Character Selection Menus

- **Single Player Mode**: Choose Jedi or Sith, AI gets the opposite
- **Two Player Mode**: Both players choose characters with proper restrictions
- **Visual Previews**: See Jedi and Sith sprites before choosing
- **Keyboard Controls**: WASD for Player 1, Arrow Keys for Player 2

### Star Wars Characters

#### 🔵 Jedi Knight

- **Appearance**: Brown robes, hood, blue lightsaber
- **Eyes**: Blue (wise Jedi eyes)
- **Weapon**: Blue lightsaber with glow effect
- **Color Scheme**: Tan/brown robes, traditional Jedi look

#### 🔴 Sith Lord

- **Appearance**: Dark robes, menacing hood, red lightsaber
- **Eyes**: Yellow (Sith eyes showing dark side corruption)
- **Weapon**: Red lightsaber with crimson glow
- **Color Scheme**: Black/dark gray robes, intimidating presence

## 🎮 Game Flow

### Single Player Mode

1. Start Menu → Select "Single Player"
2. Character Selection → Choose Jedi or Sith
3. AI automatically becomes the opposite character
4. Battle begins: Jedi vs Sith

### Two Player Mode

1. Start Menu → Select "2 Player Mode"
2. Character Selection → Player 1 chooses first (A/D keys)
3. Player 2 chooses from remaining option (←/→ keys)
4. Both players must be different characters
5. Battle begins: Player Jedi vs Player Sith

## 🎵 Enhanced Audio

- **Background Music**: Imperial March (Darth Vader's Theme) loops continuously ⚔️
- **Sound Effects**: Custom pistol shot sound (very quiet for music dominance)
- **Volume Balance**: Music at 100% (MAXIMUM POWER), gunshots at 20% (subtle)
- **Epic Atmosphere**: The Empire's theme DOMINATES the entire battlefield!

## 💻 Technical Implementation

### Character System

- `Player` and `Enemy` classes now support `character_type` parameter
- Sprite system has `get_character_sprite()` method for Jedi/Sith sprites
- Menu system has `show_character_selection()` for both game modes

### Visual Enhancements

- Procedurally generated Jedi and Sith sprites with lightsabers
- Character-specific draw methods with appropriate sprite selection
- Star Wars themed character selection UI with dark space background

### Audio System

- Imperial March (high-quality Vienna Philharmonic recording)
- Music system integrated with main game loop
- Custom pistol shot sound (MP3) works alongside background music

## 🎯 Key Rules

- In any mode, one player must be Jedi and the other must be Sith
- Single player: You choose, AI gets opposite
- Two player: First player chooses, second gets remaining option
- Epic lightsaber battles with the Empire's theme!

**The Empire has arrived! May the Dark Side guide your battles!** ⚔️🎮⚔️

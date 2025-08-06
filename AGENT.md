# Clash Royale Build-A-Bot - Agent Configuration

## Project Structure
This is a Python-based AI bot for Clash Royale that uses computer vision and machine learning for gameplay automation.

### Key Directories:
- `clashroyalebuildabot/` - Main bot package
  - `actions/` - Card action implementations  
  - `bot/` - Core bot logic
  - `detectors/` - Computer vision detection
  - `emulator/` - Android emulator interface
  - `gui/` - PyQt6 user interface
  - `models/` - ONNX neural network models
  - `utils/` - Utility functions

## Common Commands

### Development Commands
```bash
# Run bot with MAXIMUM AI intelligence (Enhanced Configuration)
python main.py --optimal

# Run continuous 24x7 mode with enhanced AI
python main_continuous.py

# Run headless (no GUI) - now uses enhanced config by default
python main.py --headless

# View optimal deck configuration
python optimal_deck_setup.py

# Install dependencies
pip install -r pyproject.toml
```

### Testing Commands
```bash
# Check ADB connection
adb devices

# Test emulator connection
adb shell wm size

# Monitor bot performance
python -c "from clashroyalebuildabot.bot.bot import Bot; print('Bot imports working')"
```

### Build Commands
```bash
# Build executable (if using PyInstaller)
pyinstaller ClashRoyaleBuildABot.spec

# Lint code
flake8 clashroyalebuildabot/
pylint clashroyalebuildabot/

# Format code
black clashroyalebuildabot/
```

## Configuration

### Default Config Location
- `clashroyalebuildabot/config.yaml` - Standard configuration
- `clashroyalebuildabot/enhanced_config.yaml` - Enhanced AI configuration

### Key Configuration Settings
- **Resolution**: Must be exactly 720x1280 with DPI 320
- **ADB Settings**: Usually `127.0.0.1:5554` for emulator
- **Performance**: Adjust `play_action` delay based on system performance
- **AI Settings**: Use enhanced config for maximum intelligence
- **Deck**: Use optimal Giant Beatdown deck (run `python optimal_deck_setup.py` for details)

## Code Style & Conventions

### Python Style
- Follow PEP 8 standards
- Use type hints where possible
- Prefer composition over inheritance
- Keep functions focused and small

### Naming Conventions
- Classes: `PascalCase` (e.g., `EnhancedBot`)
- Functions/Variables: `snake_case` (e.g., `calculate_score`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `TILE_WIDTH`)
- Files: `snake_case.py`

### Architecture Patterns
- Actions use abstract base class pattern
- Detectors use ONNX for neural network inference
- Bot uses state machine pattern for screen handling
- GUI uses PyQt6 with MVC-like separation

## Performance Optimization

### System Requirements
- **Minimum**: 8GB RAM, 4-core CPU, integrated graphics
- **Recommended**: 16GB RAM, 6+ core CPU, dedicated GPU
- **Optimal**: 32GB RAM, 8+ core CPU, RTX 3060+ or equivalent

### Emulator Settings
- **RAM Allocation**: 6-8GB
- **CPU Cores**: 4 (or half of available cores)
- **Graphics**: Hardware acceleration enabled
- **Resolution**: Exactly 720x1280, DPI 320

### Bot Performance Settings
```yaml
# For high-end systems
play_action: 0.15-0.25  # Very fast

# For mid-range systems  
play_action: 0.5-0.75   # Balanced

# For low-end systems
play_action: 1.0-1.5    # Conservative
```

## Troubleshooting

### Common Issues
1. **ADB Connection Failed**: Restart emulator and run `adb kill-server && adb start-server`
2. **Slow Performance**: Reduce `play_action` delay or increase emulator RAM
3. **Detection Issues**: Verify exact 720x1280 resolution and DPI 320
4. **Memory Errors**: Close other applications, increase virtual memory

### Debug Commands
```bash
# Check bot state
python -c "from clashroyalebuildabot import constants; print(constants.SCREENSHOT_WIDTH, constants.SCREENSHOT_HEIGHT)"

# Test ONNX models
python -c "import onnxruntime as ort; print(ort.get_available_providers())"

# Verify PyQt6
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 working')"
```

## File Locations

### Important Files
- `main.py` - Standard launcher with GUI
- `main_continuous.py` - 24x7 continuous operation
- `OPTIMAL_SETUP_GUIDE.md` - Complete setup instructions
- `enhanced_config.yaml` - Optimized AI configuration

### Log Files
- Bot logs are displayed in GUI and console
- Debug images saved to `clashroyalebuildabot/debug/` if enabled
- Performance metrics logged every 5 minutes in continuous mode

## Dependencies

### Core Dependencies
- Python 3.10+
- PyQt6 (GUI framework)
- OpenCV (computer vision)
- ONNX Runtime (neural networks)
- Pillow (image processing)
- NumPy (numerical computing)
- Loguru (logging)

### System Dependencies  
- ADB (Android Debug Bridge)
- Android emulator (BlueStacks, LDPlayer, etc.)
- Clash Royale game installed in emulator

## Performance Targets

### Optimal Performance Metrics
- **Actions per minute**: 20-30
- **Response time**: <200ms average
- **Win rate**: 75-85% (with optimal deck)
- **Memory usage**: <2GB
- **CPU usage**: <60%
- **Uptime**: 23+ hours/day (continuous mode)

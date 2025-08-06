#!/usr/bin/env python3
"""
Test script for enhanced navigation with exact coordinates
"""

import sys
import time
from loguru import logger

from error_handling import WikifiedError
from clashroyalebuildabot.actions import (
    ArchersAction, ArrowsAction, FireballAction,
    GiantAction, KnightAction, MinipekkaAction,
    MinionsAction, MusketeerAction
)
from clashroyalebuildabot.gui.utils import load_config
from clashroyalebuildabot.bot.bot import Bot


def get_optimal_actions():
    """Returns the optimal 8-card deck"""
    return [
        GiantAction,           # 1. Primary win condition
        MinipekkaAction,       # 2. High DPS tank killer
        MusketeerAction,       # 3. Ranged DPS and air defense
        MinionsAction,         # 4. Air defense and swarm
        KnightAction,          # 5. Versatile mini-tank
        ArchersAction,         # 6. Cheap ranged support
        FireballAction,        # 7. Medium damage spell
        ArrowsAction,          # 8. Area damage spell
    ]


def get_test_config():
    """Get configuration optimized for testing"""
    config = load_config()
    
    # Fast testing settings
    config['bot']['log_level'] = 'INFO'
    config['bot']['auto_start_game'] = True
    config['bot']['load_deck'] = True
    config['bot']['enable_gui'] = False
    
    # Visual settings off for performance
    config['visuals']['save_labels'] = False
    config['visuals']['save_images'] = False
    config['visuals']['show_images'] = False
    
    # Fast action timing for testing
    config['ingame']['play_action'] = 0.5
    
    return config


def main():
    """Test the enhanced navigation system"""
    logger.info("=" * 60)
    logger.info("🧪 TESTING ENHANCED NAVIGATION SYSTEM")
    logger.info("Battle Button: (357.8, 984.2)")
    logger.info("Primary OK: (360.0, 1157.9)")  
    logger.info("Secondary OK: (242.1, 1164.0)")
    logger.info("=" * 60)
    
    try:
        # Get configuration and actions
        config = get_test_config()
        actions = get_optimal_actions()
        
        logger.info("🤖 Creating bot with enhanced navigation...")
        
        # Create and run the bot
        bot = Bot(actions=actions, config=config)

        logger.info("🚀 Starting bot test...")
        logger.info("Press Ctrl+C to stop")

        # Run the bot
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Test stopped by user")
        
    except WikifiedError as e:
        logger.error(f"❌ Bot error: {e}")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        logger.info("🏁 Enhanced navigation test completed")


if __name__ == "__main__":
    main()

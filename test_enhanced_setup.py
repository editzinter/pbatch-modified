#!/usr/bin/env python3
"""
Test script to verify enhanced bot setup works correctly
"""

from loguru import logger

def test_imports():
    """Test that all imports work"""
    try:
        from main import get_optimal_actions
        from main_continuous import get_actions, get_config
        from clashroyalebuildabot.gui.utils import load_config
        logger.info("✅ All imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_config_loading():
    """Test that config loads without errors"""
    try:
        from clashroyalebuildabot.gui.utils import load_config
        config = load_config()

        # Check required keys exist
        required_keys = ['bot', 'adb', 'visuals', 'ingame']
        for key in required_keys:
            if key not in config:
                logger.error(f"❌ Missing config key: {key}")
                return False

        logger.info("✅ Config loads successfully")
        logger.info(f"Play action timing: {config['ingame']['play_action']}s")
        return True
    except Exception as e:
        logger.error(f"❌ Config loading error: {e}")
        return False

def test_optimal_actions():
    """Test that optimal actions work"""
    try:
        from main import get_optimal_actions
        actions = get_optimal_actions()
        
        if len(actions) != 8:
            logger.error(f"❌ Wrong number of actions: {len(actions)} (expected 8)")
            return False
            
        logger.info("✅ Optimal actions configured correctly")
        logger.info(f"Actions: {[action.__name__ for action in actions]}")
        return True
    except Exception as e:
        logger.error(f"❌ Actions error: {e}")
        return False

def test_continuous_bot():
    """Test that continuous bot initializes"""
    try:
        from main_continuous import ContinuousBot
        bot = ContinuousBot()
        config = bot.get_optimal_config()
        actions = bot.get_optimal_actions()
        
        if len(actions) != 8:
            logger.error(f"❌ Wrong number of continuous actions: {len(actions)}")
            return False
            
        logger.info("✅ Continuous bot initializes successfully")
        logger.info(f"Continuous timing: {config['ingame']['play_action']}s")
        return True
    except Exception as e:
        logger.error(f"❌ Continuous bot error: {e}")
        return False

def main():
    logger.info("=" * 60)
    logger.info("🧪 TESTING ENHANCED BOT SETUP")
    logger.info("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Config Loading", test_config_loading),
        ("Optimal Actions", test_optimal_actions),
        ("Continuous Bot", test_continuous_bot),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            logger.error(f"❌ {test_name} FAILED")
    
    logger.info(f"\n📊 RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        logger.info("🎉 ALL TESTS PASSED! Enhanced bot setup is working correctly.")
        logger.info("\n🚀 Ready to run:")
        logger.info("   python main.py --optimal")
        logger.info("   python main_continuous.py")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()

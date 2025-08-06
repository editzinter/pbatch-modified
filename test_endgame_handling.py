#!/usr/bin/env python3
"""
Test script to verify end-game screen handling logic
"""

import sys
from loguru import logger

def test_endgame_coordinates():
    """Test that the end-game coordinates are properly set in the Bot class"""
    try:
        # Check that the Bot class has the correct coordinate constants
        from clashroyalebuildabot.bot.bot import Bot

        # Check the source code to verify coordinates are defined
        import inspect
        source = inspect.getsource(Bot.__init__)

        # Check for the coordinate definitions
        expected_coords = [
            "(357.8, 984.2)",  # Battle button
            "(360.0, 1157.9)", # Primary OK button
            "(242.1, 1164.0)"  # Secondary OK button
        ]

        for coord in expected_coords:
            if coord not in source:
                logger.error(f"❌ Coordinate {coord} not found in Bot.__init__")
                return False

        logger.info("✅ End-game coordinates properly defined in Bot class")
        logger.info(f"  Battle button: (357.8, 984.2)")
        logger.info(f"  Primary OK button: (360.0, 1157.9)")
        logger.info(f"  Secondary OK button: (242.1, 1164.0)")

        return True
    except Exception as e:
        logger.error(f"❌ End-game coordinates test failed: {e}")
        return False

def test_screen_coordinates():
    """Test that screen coordinates are updated"""
    try:
        from clashroyalebuildabot.namespaces.screens import Screens
        
        # Check lobby screen coordinates
        lobby_coords = Screens.LOBBY.click_xy
        expected_lobby = (357.8, 984.2)
        assert lobby_coords == expected_lobby, f"Lobby coords: expected {expected_lobby}, got {lobby_coords}"
        
        # Check end-of-game screen coordinates
        endgame_coords = Screens.END_OF_GAME.click_xy
        expected_endgame = (360.0, 1157.9)
        assert endgame_coords == expected_endgame, f"End-game coords: expected {expected_endgame}, got {endgame_coords}"
        
        logger.info("✅ Screen coordinates updated correctly")
        logger.info(f"  Lobby screen click: {lobby_coords}")
        logger.info(f"  End-game screen click: {endgame_coords}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Screen coordinates test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("TESTING END-GAME SCREEN HANDLING")
    logger.info("=" * 60)
    
    tests = [
        ("End-game Coordinates Test", test_endgame_coordinates),
        ("Screen Coordinates Test", test_screen_coordinates),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                logger.error(f"Test failed: {test_name}")
        except Exception as e:
            logger.error(f"Test crashed: {test_name} - {e}")
    
    logger.info("=" * 60)
    logger.info(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! End-game handling is ready.")
        logger.info("")
        logger.info("📋 SUMMARY OF END-GAME HANDLING:")
        logger.info("• Unknown screens will be treated as potential end-game screens")
        logger.info("• Primary OK button (360.0, 1157.9) will be tried first")
        logger.info("• If that fails, primary OK button will be tried again after 5 seconds")
        logger.info("• If still failing, secondary OK button (242.1, 1164.0) will be tried")
        logger.info("• Battle button (357.8, 984.2) will be used for lobby screen")
        logger.info("• Robust retry logic with automatic reset after multiple attempts")
        return 0
    else:
        logger.error("❌ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

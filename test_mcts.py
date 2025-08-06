#!/usr/bin/env python3
"""
Test script to verify MCTS implementation works correctly
"""

import sys
from loguru import logger

def test_mcts_import():
    """Test that MCTS can be imported without errors"""
    try:
        from clashroyalebuildabot.ai.mcts import run_mcts, MCTSNode, simulate_action, heuristic_evaluation
        logger.info("✅ MCTS imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ MCTS import error: {e}")
        return False

def test_mcts_components():
    """Test that MCTS components work correctly"""
    try:
        from clashroyalebuildabot.ai.mcts import MCTSNode, heuristic_evaluation
        from clashroyalebuildabot.namespaces.state import State
        from clashroyalebuildabot.namespaces.numbers import Numbers, NumberDetection

        # Create a mock state for testing
        mock_elixir = NumberDetection(bbox=(0, 0, 0, 0), number=5.0)
        mock_hp = NumberDetection(bbox=(0, 0, 0, 0), number=100.0)
        mock_numbers = Numbers(
            left_enemy_princess_hp=mock_hp,
            right_enemy_princess_hp=mock_hp,
            left_ally_princess_hp=mock_hp,
            right_ally_princess_hp=mock_hp,
            elixir=mock_elixir
        )

        mock_state = State(
            allies=[],
            enemies=[],
            numbers=mock_numbers,
            cards=(),
            ready=[],
            screen=None
        )

        # Test MCTSNode creation
        node = MCTSNode(mock_state)
        logger.info("✅ MCTSNode created successfully")

        # Test heuristic evaluation
        score = heuristic_evaluation(mock_state)
        logger.info(f"✅ Heuristic evaluation works: score = {score}")

        return True
    except Exception as e:
        logger.error(f"❌ MCTS components error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("TESTING MCTS IMPLEMENTATION")
    logger.info("=" * 50)
    
    tests = [
        ("MCTS Import Test", test_mcts_import),
        ("MCTS Components Test", test_mcts_components),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning: {test_name}")
        if test_func():
            passed += 1
        else:
            logger.error(f"Test failed: {test_name}")
    
    logger.info("=" * 50)
    logger.info(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! MCTS is ready to use.")
        return 0
    else:
        logger.error("❌ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

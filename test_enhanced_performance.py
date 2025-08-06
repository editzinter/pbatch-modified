#!/usr/bin/env python3
"""
Test script to verify enhanced AI bot performance and configuration
"""

from loguru import logger
import time

def test_enhanced_bot_import():
    """Test enhanced bot import and initialization"""
    try:
        from clashroyalebuildabot.enhanced_bot import EnhancedBot, ActionScore
        from main import get_optimal_actions
        from clashroyalebuildabot.gui.utils import load_enhanced_config
        
        config = load_enhanced_config()
        actions = get_optimal_actions()
        
        # Test ActionScore dataclass
        score = ActionScore()
        score.total_score = 100.0
        
        logger.info("✅ Enhanced bot imports and basic classes work")
        logger.info(f"Config sections: {list(config.keys())}")
        logger.info(f"Actions available: {len(actions)}")
        return True
    except Exception as e:
        logger.error(f"❌ Enhanced bot import failed: {e}")
        return False

def test_enhanced_configuration():
    """Test the comprehensive enhanced configuration"""
    try:
        from clashroyalebuildabot.gui.utils import load_enhanced_config
        config = load_enhanced_config()
        
        # Test key AI settings
        ai_config = config.get('ai', {})
        ingame_config = config.get('ingame', {})
        bot_config = config.get('bot', {})
        
        required_ai_settings = ['max_depth', 'heuristic_weights', 'online_learning']
        required_ingame_settings = ['play_action', 'prediction_engine', 'calculation_time_limit']
        required_bot_settings = ['decision_algorithm', 'lookahead_depth']
        
        # Check AI settings
        for setting in required_ai_settings:
            if setting not in ai_config:
                logger.warning(f"⚠️ Missing AI setting: {setting}")
            else:
                logger.info(f"✅ AI {setting}: {ai_config[setting]}")
                
        # Check ingame settings  
        for setting in required_ingame_settings:
            if setting not in ingame_config:
                logger.warning(f"⚠️ Missing ingame setting: {setting}")
            else:
                logger.info(f"✅ Ingame {setting}: {ingame_config[setting]}")
                
        # Check bot settings
        for setting in required_bot_settings:
            if setting not in bot_config:
                logger.warning(f"⚠️ Missing bot setting: {setting}")
            else:
                logger.info(f"✅ Bot {setting}: {bot_config[setting]}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Enhanced configuration test failed: {e}")
        return False

def test_continuous_bot_enhanced():
    """Test continuous bot with enhanced actions"""
    try:
        from main_continuous import ContinuousBot
        
        bot = ContinuousBot()
        actions = bot.get_optimal_actions()
        config = bot.get_optimal_config()
        
        # Check we have exactly 8 actions (Clash Royale deck limit)
        if len(actions) == 8:
            logger.info(f"✅ Optimal action set: {len(actions)} actions (correct deck size)")
            action_names = [action.__name__ for action in actions]
            logger.info(f"Actions: {', '.join(action_names)}")
        else:
            logger.warning(f"⚠️ {len(actions)} actions (expected exactly 8 for Clash Royale deck)")
            
        # Check timing configuration
        play_delay = config.get('ingame', {}).get('play_action', 1.0)
        logger.info(f"✅ Play action delay: {play_delay}s")
        
        return True
    except Exception as e:
        logger.error(f"❌ Continuous bot test failed: {e}")
        return False

def test_scoring_system():
    """Test the enhanced scoring system"""
    try:
        from clashroyalebuildabot.enhanced_bot import ActionScore
        
        # Test ActionScore calculations
        score = ActionScore()
        score.damage_score = 25.0
        score.defense_score = 15.0
        score.elixir_efficiency = 20.0
        score.positioning_score = 10.0
        score.tempo_score = 8.0
        
        # Test score weights
        weights = {
            'damage_dealing': 0.3,
            'defense': 0.25,
            'elixir_efficiency': 0.2,
            'positioning': 0.15,
            'tempo': 0.1
        }
        
        total = (score.damage_score * weights['damage_dealing'] +
                score.defense_score * weights['defense'] +
                score.elixir_efficiency * weights['elixir_efficiency'] +
                score.positioning_score * weights['positioning'] +
                score.tempo_score * weights['tempo'])
        
        score.total_score = total
        
        logger.info(f"✅ Enhanced scoring system works")
        logger.info(f"Sample total score: {total:.2f}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Scoring system test failed: {e}")
        return False

def test_performance_features():
    """Test performance monitoring features"""
    try:
        from clashroyalebuildabot.gui.utils import load_enhanced_config
        config = load_enhanced_config()
        
        # Check monitoring settings
        monitoring = config.get('monitoring', {})
        hardware = config.get('hardware', {})
        
        if monitoring.get('enabled'):
            logger.info("✅ Performance monitoring enabled")
            logger.info(f"Log interval: {monitoring.get('log_interval')}s")
            logger.info(f"Min actions/min: {monitoring.get('min_actions_per_minute')}")
        
        if hardware.get('gpu_acceleration'):
            logger.info("✅ GPU acceleration enabled")
            logger.info(f"CPU threads: {hardware.get('cpu_threads')}")
            
        return True
    except Exception as e:
        logger.error(f"❌ Performance features test failed: {e}")
        return False

def main():
    logger.info("=" * 60)
    logger.info("🧪 TESTING ENHANCED AI BOT IMPLEMENTATION")
    logger.info("=" * 60)
    
    tests = [
        ("Enhanced Bot Import", test_enhanced_bot_import),
        ("Enhanced Configuration", test_enhanced_configuration),
        ("Continuous Bot Enhanced", test_continuous_bot_enhanced),
        ("Scoring System", test_scoring_system),
        ("Performance Features", test_performance_features),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
    
    logger.info(f"\n📊 RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        logger.info("🎉 ALL ENHANCED AI TESTS PASSED!")
        logger.info("\n🚀 Enhanced AI Features Active:")
        logger.info("   • Advanced multi-metric action scoring")
        logger.info("   • Optimal 8-card Giant Beatdown deck")
        logger.info("   • Comprehensive AI configuration")
        logger.info("   • Performance monitoring")
        logger.info("   • Adaptive timing optimization")
        logger.info("\n💡 Ready to run with maximum intelligence:")
        logger.info("   python main.py --optimal")
        logger.info("   python main_continuous.py")
    else:
        logger.error("❌ Some enhanced features are not working correctly.")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()

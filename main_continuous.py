#!/usr/bin/env python3
"""
Clash Royale Bot - Continuous 24x7 Operation with GPU Acceleration
This script runs the bot in a loop, ensuring it automatically restarts after crashes.
Optimized for maximum performance with GPU acceleration.
"""

import os
import signal
import sys
import time
import traceback

# Add local cudnn_libs directory to PATH
cudnn_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cudnn_libs")
if os.path.exists(cudnn_path):
    os.environ["PATH"] = cudnn_path + os.pathsep + os.environ["PATH"]


from loguru import logger

from error_handling import WikifiedError
from clashroyalebuildabot.actions import (
    ArchersAction,
    ArrowsAction,
    BarbariansAction,
    BattleRamAction,
    FireballAction,
    GiantAction,
    KnightAction,
    MinipekkaAction,
    MinionsAction,
    MusketeerAction,
    SkeletonsAction,
    SpearGoblinsAction,
)
from clashroyalebuildabot.gui.utils import load_config
from clashroyalebuildabot.utils.git_utils import check_and_pull_updates
from clashroyalebuildabot.bot.bot import Bot


def check_and_setup_gpu():
    """Check GPU availability and setup optimal configuration"""
    try:
        import onnxruntime as ort

        logger.info("🔍 Checking GPU acceleration status...")

        # Get available providers
        available_providers = ort.get_available_providers()
        cuda_available = "CUDAExecutionProvider" in available_providers

        if cuda_available:
            logger.info("🚀 GPU acceleration ENABLED - Using CUDA")
            logger.info(f"   Available providers: {available_providers}")

            # Check GPU info
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    gpu_info = result.stdout.strip().split('\n')[0]
                    logger.info(f"   GPU: {gpu_info}")
            except:
                pass

            return True
        else:
            logger.warning("⚠️  GPU acceleration DISABLED - Using CPU only")
            logger.warning("   For better performance, install: pip install onnxruntime-gpu")
            logger.info(f"   Available providers: {available_providers}")
            return False

    except ImportError:
        logger.error("❌ ONNX Runtime not found")
        return False
    except Exception as e:
        logger.error(f"❌ GPU check failed: {e}")
        return False


def get_actions():
    """Returns the deck actions for the bot"""
    return [
        BarbariansAction,
        MinipekkaAction,
        MusketeerAction,
        SpearGoblinsAction,
        MinionsAction,
        ArchersAction,
        BattleRamAction,
        SkeletonsAction,
    ]


def get_config():
    """Returns optimized configuration for continuous operation"""
    config = load_config()

    # Ensure auto-start is enabled for continuous operation
    config['bot']['auto_start_game'] = True
    
    # NEVER load deck - assume it's already set for continuous operation
    config['bot']['load_deck'] = False
    config['bot']['skip_deck_copy'] = True
    config['bot']['skip_user_input'] = True

    # Optimize for MAXIMUM AI performance and speed
    config['ingame']['play_action'] = 0.15  # Ultra-fast action delay for maximum intelligence

    # Disable visual processing to save CPU
    config['visuals']['save_labels'] = False
    config['visuals']['save_images'] = False
    config['visuals']['show_images'] = True

    return config

def run_bot_continuously():
    """Run the bot continuously, restarting on crashes"""
    crash_count = 0

    while True:
        try:
            logger.info("=" * 60)
            logger.info("CLASH ROYALE BOT - CONTINUOUS 24x7 OPERATION")
            logger.info("Using Original Bot Logic + MCTS AI + GPU Acceleration")
            logger.info("=" * 60)

            # Check GPU status for this run
            gpu_status = check_and_setup_gpu()

            # Get configuration and actions
            config = get_config()
            actions = get_actions()

            logger.info(f"Starting bot with {len(actions)} cards")
            logger.info("Deck: Barbarians, Mini P.E.K.K.A, Musketeer, Spear Goblins, Minions, Archers, Battle Ram, Skeletons")
            logger.info(f"AI Acceleration: {'🚀 GPU (CUDA)' if gpu_status else '⚠️  CPU Only'}")

            # Create and run the bot (this includes all the original screen handling logic)
            bot = Bot(actions=actions, config=config)
            logger.info("Bot created successfully, starting main loop...")

            # Reset crash count on successful start
            crash_count = 0

            # Run the bot - this will handle all screens (lobby, end of game, etc.) automatically
            bot.run()

        except KeyboardInterrupt:
            logger.info("Bot stopped by user (Ctrl+C)")
            break

        except Exception as e:
            crash_count += 1
            logger.error(f"Bot crashed (crash #{crash_count}): {e}")
            logger.error(traceback.format_exc())

            # Wait before restarting, with exponential backoff
            wait_time = min(30, 5 * crash_count)
            logger.info(f"Waiting {wait_time} seconds before restart...")
            time.sleep(wait_time)

            logger.info("Restarting bot...")


def setup_optimal_emulator_settings():
    """Display optimal emulator configuration"""
    logger.info("=" * 60)
    logger.info("OPTIMAL EMULATOR CONFIGURATION")
    logger.info("=" * 60)
    logger.info("Resolution: 720x1280 (9:16 aspect ratio)")
    logger.info("DPI: 320")
    logger.info("RAM: 4GB minimum, 8GB recommended")
    logger.info("CPU Cores: 4 cores minimum")
    logger.info("Graphics: Hardware acceleration enabled")
    logger.info("ADB Port: 5554")
    logger.info("Performance Mode: High")
    logger.info("VT-x/AMD-V: Enabled in BIOS")
    logger.info("=" * 60)


def get_optimal_deck_recommendation():
    """Display optimal deck configuration"""
    logger.info("=" * 60)
    logger.info("OPTIMAL DECK CONFIGURATION")
    logger.info("For Maximum Bot Effectiveness")
    logger.info("=" * 60)
    logger.info("1. Barbarians (Defense/Offense) - Strong ground swarm")
    logger.info("2. Mini P.E.K.K.A (Tank Killer) - High DPS")
    logger.info("3. Musketeer (Air Defense) - Versatile ranged")
    logger.info("4. Spear Goblins (Chip Damage) - Cheap ranged attackers")
    logger.info("5. Minions (Air Support) - Flying swarm")
    logger.info("6. Archers (Support) - Cheap ranged units")
    logger.info("7. Battle Ram (Win Condition) - Bridge spam and building targeter")
    logger.info("8. Skeletons (Cycle/Distraction) - Cheap swarm")
    logger.info("")
    logger.info("Average Elixir Cost: 3.3")
    logger.info("Playstyle: Bridge Spam with strong defensive capabilities")
    logger.info("=" * 60)

def main():
    """Main function for continuous operation with GPU optimization"""
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}")
        logger.info("Shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logger.info("=" * 60)
        logger.info("🤖 CLASH ROYALE BOT - GPU ACCELERATED CONTINUOUS MODE")
        logger.info("=" * 60)

        # Check GPU acceleration first
        gpu_enabled = check_and_setup_gpu()

        if not gpu_enabled:
            logger.info("")
            logger.info("💡 TO ENABLE GPU ACCELERATION:")
            logger.info("   1. pip uninstall onnxruntime")
            logger.info("   2. pip install onnxruntime-gpu")
            logger.info("   3. Restart the bot")
            logger.info("   Expected speedup: 2-5x faster AI inference!")
            logger.info("")

        # Check for updates
        logger.info("Checking for updates...")
        check_and_pull_updates(auto_update=True)

        # Display optimal configurations
        setup_optimal_emulator_settings()
        get_optimal_deck_recommendation()

        # Start continuous operation
        run_bot_continuously()

    except WikifiedError:
        raise
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

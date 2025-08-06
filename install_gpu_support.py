#!/usr/bin/env python3
"""
Install GPU support for Clash Royale Bot
This script will install onnxruntime-gpu to enable CUDA acceleration
"""

import subprocess
import sys
from loguru import logger

def check_nvidia_gpu():
    """Check if NVIDIA GPU is available"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract GPU info
            lines = result.stdout.split('\n')
            for line in lines:
                if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Quadro' in line:
                    gpu_info = line.strip()
                    logger.info(f"✅ NVIDIA GPU detected: {gpu_info}")
                    return True
            logger.info("✅ NVIDIA GPU detected")
            return True
        else:
            logger.error("❌ No NVIDIA GPU found or drivers not installed")
            return False
    except FileNotFoundError:
        logger.error("❌ nvidia-smi not found - NVIDIA drivers not installed")
        return False
    except Exception as e:
        logger.error(f"❌ Error checking GPU: {e}")
        return False

def install_gpu_support():
    """Install onnxruntime-gpu"""
    try:
        logger.info("🔄 Uninstalling CPU-only onnxruntime...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'uninstall', 'onnxruntime', '-y'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ CPU-only onnxruntime uninstalled")
        else:
            logger.warning("⚠️  onnxruntime may not have been installed")
        
        logger.info("🔄 Installing GPU-accelerated onnxruntime...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'onnxruntime-gpu'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ onnxruntime-gpu installed successfully!")
            return True
        else:
            logger.error(f"❌ Failed to install onnxruntime-gpu: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Installation failed: {e}")
        return False

def verify_gpu_support():
    """Verify that GPU support is working"""
    try:
        import onnxruntime as ort
        
        available_providers = ort.get_available_providers()
        cuda_available = "CUDAExecutionProvider" in available_providers
        
        if cuda_available:
            logger.info("🎉 GPU acceleration is now ENABLED!")
            logger.info(f"   Available providers: {available_providers}")
            return True
        else:
            logger.error("❌ GPU acceleration still not available")
            logger.error(f"   Available providers: {available_providers}")
            return False
            
    except ImportError:
        logger.error("❌ onnxruntime not found after installation")
        return False
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False

def main():
    """Main installation process"""
    logger.info("=" * 60)
    logger.info("🚀 CLASH ROYALE BOT - GPU ACCELERATION INSTALLER")
    logger.info("=" * 60)
    
    # Check if NVIDIA GPU is available
    if not check_nvidia_gpu():
        logger.error("❌ No NVIDIA GPU detected. GPU acceleration requires NVIDIA GPU.")
        logger.info("💡 If you have an NVIDIA GPU:")
        logger.info("   1. Install latest NVIDIA drivers")
        logger.info("   2. Restart your computer")
        logger.info("   3. Run this script again")
        return 1
    
    # Install GPU support
    logger.info("\n🔧 Installing GPU support...")
    if not install_gpu_support():
        logger.error("❌ Installation failed")
        return 1
    
    # Verify installation
    logger.info("\n🔍 Verifying GPU support...")
    if not verify_gpu_support():
        logger.error("❌ Verification failed")
        return 1
    
    # Success message
    logger.info("\n" + "=" * 60)
    logger.info("🎉 GPU ACCELERATION SUCCESSFULLY INSTALLED!")
    logger.info("=" * 60)
    logger.info("✅ Your Clash Royale Bot will now use GPU acceleration")
    logger.info("✅ Expected performance improvement: 2-5x faster AI inference")
    logger.info("✅ Neural networks will run on your graphics card")
    logger.info("")
    logger.info("🚀 You can now run the bot with GPU acceleration:")
    logger.info("   python main_continuous.py")
    logger.info("")
    logger.info("The bot will automatically detect and use GPU acceleration!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

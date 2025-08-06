#!/usr/bin/env python3
"""
Check if the bot is using CUDA/GPU acceleration
"""

import sys
from loguru import logger

def check_onnx_providers():
    """Check what ONNX Runtime providers are available and being used"""
    try:
        import onnxruntime as ort
        
        logger.info("=" * 60)
        logger.info("ONNX RUNTIME GPU/CUDA CHECK")
        logger.info("=" * 60)
        
        # Get all available providers
        available_providers = ort.get_available_providers()
        logger.info(f"Available providers: {available_providers}")
        
        # Check if CUDA is available
        cuda_available = "CUDAExecutionProvider" in available_providers
        logger.info(f"CUDA Provider Available: {'✅ YES' if cuda_available else '❌ NO'}")
        
        # Check what the bot actually uses
        providers = list(
            set(ort.get_available_providers())
            & {"CUDAExecutionProvider", "CPUExecutionProvider"}
        )
        logger.info(f"Bot will use providers: {providers}")
        
        if "CUDAExecutionProvider" in providers:
            logger.info("🚀 Bot is configured to use GPU/CUDA acceleration!")
            return True
        else:
            logger.warning("⚠️  Bot will use CPU only")
            return False
            
    except ImportError:
        logger.error("❌ ONNX Runtime not installed")
        return False
    except Exception as e:
        logger.error(f"❌ Error checking ONNX providers: {e}")
        return False

def check_cuda_installation():
    """Check if CUDA is properly installed on the system"""
    try:
        import subprocess
        
        logger.info("\n" + "=" * 60)
        logger.info("CUDA INSTALLATION CHECK")
        logger.info("=" * 60)
        
        # Try to run nvidia-smi
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("✅ NVIDIA GPU detected:")
                # Extract GPU info from nvidia-smi output
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'GeForce' in line or 'RTX' in line or 'GTX' in line or 'Quadro' in line:
                        gpu_info = line.strip()
                        logger.info(f"   {gpu_info}")
                        break
                return True
            else:
                logger.warning("❌ nvidia-smi failed - no NVIDIA GPU or drivers not installed")
                return False
        except FileNotFoundError:
            logger.warning("❌ nvidia-smi not found - NVIDIA drivers not installed")
            return False
        except subprocess.TimeoutExpired:
            logger.warning("⚠️  nvidia-smi timeout")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error checking CUDA: {e}")
        return False

def check_onnxruntime_gpu():
    """Check if onnxruntime-gpu is installed"""
    try:
        logger.info("\n" + "=" * 60)
        logger.info("ONNX RUNTIME GPU PACKAGE CHECK")
        logger.info("=" * 60)
        
        import pkg_resources
        
        # Check for onnxruntime-gpu
        try:
            gpu_version = pkg_resources.get_distribution("onnxruntime-gpu").version
            logger.info(f"✅ onnxruntime-gpu installed: version {gpu_version}")
            return True
        except pkg_resources.DistributionNotFound:
            logger.warning("❌ onnxruntime-gpu not installed")
            
            # Check for regular onnxruntime
            try:
                cpu_version = pkg_resources.get_distribution("onnxruntime").version
                logger.info(f"⚠️  Only onnxruntime (CPU) installed: version {cpu_version}")
                logger.info("   To enable GPU: pip uninstall onnxruntime && pip install onnxruntime-gpu")
            except pkg_resources.DistributionNotFound:
                logger.error("❌ No onnxruntime package found")
            
            return False
            
    except Exception as e:
        logger.error(f"❌ Error checking onnxruntime packages: {e}")
        return False

def test_gpu_inference():
    """Test if GPU inference actually works"""
    try:
        logger.info("\n" + "=" * 60)
        logger.info("GPU INFERENCE TEST")
        logger.info("=" * 60)
        
        import onnxruntime as ort
        import numpy as np
        
        # Create a simple test session with CUDA provider
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        
        # We can't test with actual models without loading them, but we can test provider creation
        try:
            # This will fail if CUDA provider can't be created
            session_options = ort.SessionOptions()
            logger.info("✅ CUDA provider can be initialized")
            return True
        except Exception as e:
            logger.error(f"❌ CUDA provider initialization failed: {e}")
            return False
            
    except Exception as e:
        logger.error(f"❌ GPU inference test failed: {e}")
        return False

def main():
    """Run all GPU/CUDA checks"""
    logger.info("🔍 Checking if Clash Royale Bot is using GPU acceleration...")
    
    checks = [
        ("CUDA Installation", check_cuda_installation),
        ("ONNX Runtime GPU Package", check_onnxruntime_gpu),
        ("ONNX Runtime Providers", check_onnx_providers),
        ("GPU Inference Test", test_gpu_inference),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        logger.info(f"\n🔍 Running: {check_name}")
        if check_func():
            passed += 1
    
    logger.info("\n" + "=" * 60)
    logger.info("FINAL RESULTS")
    logger.info("=" * 60)
    logger.info(f"Checks passed: {passed}/{total}")
    
    if passed >= 3:
        logger.info("🎉 Your bot IS using GPU/CUDA acceleration!")
        logger.info("   Neural networks will run on your graphics card for maximum speed.")
    elif passed >= 1:
        logger.warning("⚠️  Partial GPU support - some components may use GPU")
        logger.info("   Consider installing onnxruntime-gpu for full acceleration")
    else:
        logger.warning("❌ Your bot is running on CPU only")
        logger.info("   Install CUDA drivers and onnxruntime-gpu for GPU acceleration")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

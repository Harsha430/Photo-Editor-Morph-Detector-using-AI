#!/usr/bin/env python3
"""
Alternative Background Remover using OpenCV
Does not require onnxruntime - uses GrabCut algorithm
"""

import cv2
import numpy as np
from PIL import Image
import os
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def remove_background(image_path: str, output_path: str = "no_background.png") -> str:
    """
    Removes background from the input image using OpenCV GrabCut algorithm.
    
    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the image with background removed.
    
    Returns:
        str: Path to the output image.
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Input image not found: {image_path}")

        logger.info(f"🔄 Removing background from: {image_path}")

        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        logger.info(f"📐 Input image size: {img.shape}")

        # Optimize: Resize large images for faster processing
        original_height, original_width = img.shape[:2]
        max_dimension = 1024  # Process at max 1024px for speed
        
        if max(original_height, original_width) > max_dimension:
            scale = max_dimension / max(original_height, original_width)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            logger.info(f"📏 Resized to {img_resized.shape} for faster processing")
        else:
            img_resized = img
            scale = 1.0

        # Create a mask initialized with probable background
        mask = np.zeros(img_resized.shape[:2], np.uint8)
        
        # Define rectangle around the object (assuming object is in center)
        height, width = img_resized.shape[:2]
        margin = int(min(height, width) * 0.05)  # 5% margin
        rect = (margin, margin, width - 2*margin, height - 2*margin)
        
        # Initialize background and foreground models
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        logger.info("🎯 Processing with GrabCut algorithm...")
        
        # Apply GrabCut algorithm (reduced iterations for speed)
        cv2.grabCut(img_resized, mask, rect, bgd_model, fgd_model, 3, cv2.GC_INIT_WITH_RECT)
        
        logger.info("✂️ Creating mask...")
        
        # Create binary mask where 0 and 2 are background, 1 and 3 are foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # If we resized, upscale the mask back to original size
        if scale != 1.0:
            mask2 = cv2.resize(mask2, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
            logger.info(f"📏 Upscaled mask back to {mask2.shape}")
        
        # Apply mask to original image
        img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img_rgba[:, :, 3] = mask2 * 255
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Ensure PNG extension for transparency
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'
        
        # Save using PIL to ensure proper PNG with transparency
        pil_img = Image.fromarray(cv2.cvtColor(img_rgba, cv2.COLOR_BGRA2RGBA))
        pil_img.save(output_path, 'PNG')
        
        logger.info(f"✅ Background removed successfully: {output_path}")
        logger.info(f"📐 Output image size: {pil_img.size}")
        
        return output_path

    except Exception as e:
        logger.error(f"❌ Background removal failed: {e}")
        raise Exception(f"Background removal error: {str(e)}")

# Test function
def test_background_remover():
    """Test the background remover with a sample image."""
    try:
        logger.info("🧪 Testing background remover...")
        
        # Create a test image with a simple object
        test_input = "test_bg_input.jpg"
        test_output = "test_bg_output.png"
        
        # Create a test image with a colored circle on white background
        img = np.ones((300, 300, 3), dtype=np.uint8) * 255
        cv2.circle(img, (150, 150), 80, (0, 0, 255), -1)
        cv2.imwrite(test_input, img)
        
        # Test background removal
        result = remove_background(test_input, test_output)
        
        if os.path.exists(result):
            logger.info("✅ Background remover test passed!")
        else:
            logger.error("❌ Background remover test failed - output not created")
            
        # Cleanup
        for file in [test_input, test_output]:
            if os.path.exists(file):
                os.remove(file)
                
    except Exception as e:
        logger.error(f"❌ Background remover test failed: {e}")

if __name__ == "__main__":
    test_background_remover()

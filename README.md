# Photo Editor Morph Detector using AI

A full-stack AI-powered image processing application with AI detection, background removal, and morph detection capabilities.

## Features

- **AI Detection**: Detect if an image is AI-generated or a real photo using the Ateeqq/ai-vs-human-image-detector model
- **Background Removal**: Remove backgrounds from images with optimized GrabCut algorithm
- **Morph Detection**: Analyze images for signs of morphing/editing using multi-analysis techniques
- **Modern UI**: React-based frontend with beautiful, responsive design

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - High-performance web framework
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face model library
- **OpenCV** - Image processing
- **Pillow** - Image manipulation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Harsha430/Photo-Editor-Morph-Detector-using-AI.git
cd Photo-Editor-Morph-Detector-using-AI
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download AI models:
The Ateeqq AI detection model will be automatically downloaded on first run. Alternatively, you can download it manually:
```bash
# The model will be saved to models/ai-vs-human-image-detector/
# Size: ~354MB
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend Server
```bash
# From project root
python api_server_simple.py
# Or use the batch file (Windows)
start_backend.bat
```
Backend will run on: http://localhost:8001

### Start Frontend Server
```bash
# From frontend directory
npm run dev
# Or use the batch file (Windows) from project root
start_frontend.bat
```
Frontend will run on: http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Upload an image
3. Choose a feature:
   - **AI Detection**: Analyze if the image is AI-generated
   - **Background Removal**: Remove the background (outputs PNG with transparency)
   - **Morph Detection**: Detect if the image has been morphed/edited

## Project Structure

```
Photo-Editor-Morph-Detector-using-AI/
├── api_server_simple.py          # Main FastAPI backend server
├── ateeqq_final_working.py       # AI detection module (Ateeqq model)
├── background_remover.py         # Background removal (optimized GrabCut)
├── photo_morph_detector.py       # Morph detection module
├── utils.py                      # Utility functions
├── requirements.txt              # Python dependencies
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   └── context/             # React context
│   ├── package.json
│   └── vite.config.js
├── models/                       # AI models (not in git, download separately)
├── uploads/                      # Uploaded images
└── outputs/                      # Processed images
```

## AI Models

### Ateeqq AI Detector
- **Model**: Ateeqq/ai-vs-human-image-detector
- **Architecture**: SigLIP (Vision Transformer)
- **Size**: ~354MB
- **Accuracy**: Detects AI-generated images vs real photos
- **Threshold**: 50% (balanced detection)

### Photo Morph Detector
- **Type**: Multi-analysis algorithm
- **Techniques**: Compression analysis, noise patterns, edge consistency, lighting, color, texture
- **No external model required**

## Performance Optimizations

- **Background Removal**: Automatically resizes large images to max 1024px before processing, then upscales the mask back to original size
- **GrabCut Iterations**: Reduced from 5 to 3 for faster processing
- **Result**: Processes large images in seconds instead of minutes

## API Endpoints

- `GET /health` - Health check
- `POST /upload` - Upload image
- `POST /ai-detect` - AI detection
- `POST /morph-detect` - Morph detection
- `POST /remove-background/{image_id}` - Background removal
- `GET /uploads/{filename}` - Serve uploaded images
- `GET /outputs/{filename}` - Serve processed images

## Configuration

### Backend Port
Default: 8001 (configured in `api_server_simple.py`)

### Frontend Port
Default: 3000 (configured in `vite.config.js`)

### CORS
Configured to allow requests from:
- http://localhost:3000
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:5173

## Troubleshooting

### Model Download Issues
If the AI model fails to download automatically:
1. Check your internet connection
2. Ensure you have ~500MB free disk space
3. The model will be saved to `models/ai-vs-human-image-detector/`

### Port Already in Use
If port 8001 or 3000 is already in use:
```bash
# Windows - Find and kill process
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Module Import Errors
Ensure virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Known Limitations

- **Fork Restriction**: This repository is a fork. Large model files are not stored in git - they must be downloaded separately
- **Model Compatibility**: Some Hugging Face models (e.g., umm-maybe/AI-image-detector, Organika/sdxl-detector) are not compatible with transformers 4.57.3
- **GPU Support**: Currently configured for CPU. For GPU support, ensure CUDA-compatible PyTorch is installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Ateeqq** for the AI vs Human image detector model
- **Hugging Face** for the Transformers library
- **OpenCV** for image processing capabilities

## Contact

For issues, questions, or contributions, please open an issue on GitHub.

---

**Note**: Model files are not included in the repository due to size constraints. They will be automatically downloaded on first run or can be downloaded manually from Hugging Face.

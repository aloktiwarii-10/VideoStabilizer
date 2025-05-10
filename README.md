# VideoStabilizer
🎞️ Video Stabilizer
A desktop-based Python application to stabilize shaky videos using OpenCV. This tool reduces unwanted motion in videos caused by handheld shooting or camera instability, producing smoother and more visually appealing output.

📽️ Demo
Coming Soon – Sample videos before and after stabilization will be added here.

🧰 Features
✅ Stabilizes shaky video footage using motion estimation and smoothing

✅ GUI built with PyQt5 for ease of use

✅ Input support for most common video formats (e.g., .mp4, .avi)

✅ Real-time progress display

✅ Supports batch processing

✅ Frame interpolation for smoother transitions

🏗️ Project Structure
VideoStabilizer/
├── sampleVideos/       # Example videos to test
├── src/                # Main application source code
│   ├── preproc.py      # Preprocessing script
│   ├── stabilize.py    # Core stabilization logic
│   └── generate.py     # Output generation script
├── requirements.txt    # Python dependencies
├── script.sh           # Shell script to run the app
└── README.md           # Project documentation

🚀 Getting Started
Prerequisites
Ensure you have Python 3.7+ installed.

Installation

Clone the repository :-
git clone https://github.com/aloktiwarii-10/VideoStabilizer.git
cd VideoStabilizer

Install dependencies:-
pip install -r requirements.txt

🧪 Run the Pipeline (Command Line)
# Step 1: Extract transforms
python3 src/preproc.py sampleVideos/testing.mp4

# Step 2: Smooth the motion trajectory
python3 src/stabilize.py 40

# Step 3: Generate the final stabilized video
python3 src/generate.py sampleVideos/testing.mp4 40

📊 Output
Final stabilized video: video_out.avi
Intermediate files:
transforms.pkl: Raw transform data
trajectory.pkl: Computed camera trajectory
smoothTrajectory.pkl: Optimized/smoothed trajectory

⚙️ How It Works

Preprocessing (preproc.py)
Extracts SIFT features and computes affine transforms frame-by-frame.
Saves raw motion data to transforms.pkl.

Stabilization (stabilize.py)
Computes trajectory using cumulative transforms.
Applies convex optimization to smooth camera motion.
Outputs smoothed trajectory in smoothTrajectory.pkl.

Video Generation (generate.py)
Applies corrected transforms to frames.
Generates the stabilized output video as video_out.avi.

✅ Dependencies
Python 3.7+
OpenCV
NumPy
matplotlib
cvxpy

📌 Notes
Uses SIFT for keypoint detection (OpenCV >= 4.4 required).
Optimization powered by cvxpy with the ECOS solver.
Ideal for videos with minor to moderate shake (e.g. handheld mobile footage).

🔧 Troubleshooting
Command not found: python
➤ Use python3 instead.

Permission error on script.sh
➤ Run chmod +x script.sh before execution.

cvxpy solver issues
➤ Ensure ECOS is installed: pip install ecos.

👨‍💻 Author
Alok Tiwari

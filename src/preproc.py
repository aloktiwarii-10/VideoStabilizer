import cv2
import numpy as np
import pickle
import sys

# Use main repo SIFT instead of contrib (fix deprecation warning)
sift = cv2.SIFT_create(200)  # Changed from xfeatures2d

def getAffMat(I1, I2):
    I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
    I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)

    # Finding sift features
    kp1, desc1 = sift.detectAndCompute(I1, None)
    kp2, desc2 = sift.detectAndCompute(I2, None)

    if desc1 is None or desc2 is None:
        return None

    # Finding good matches using ratio testing
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(desc1, desc2, k=2)
    
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    # Need at least 3 points for affine estimation
    if len(good) < 3:
        return None

    pts_src = []
    pts_dst = []
    for i in range(len(good)):
        pts_src.append(kp1[good[i].queryIdx].pt)
        pts_dst.append(kp2[good[i].trainIdx].pt)

    pts_src = np.array(pts_src).astype(np.float32)
    pts_dst = np.array(pts_dst).astype(np.float32)

    # Compute affine matrix with RANSAC
    try:
        mat, _ = cv2.estimateAffinePartial2D(
            pts_src, pts_dst, 
            method=cv2.RANSAC,
            ransacReprojThreshold=3.0
        )
        return mat
    except:
        return None

v = cv2.VideoCapture(sys.argv[1])
n_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))

transforms = [[0], [0], [0], [1]]  # Initialize with identity transform
count = 0
prev = None

while v.isOpened():
    ret, frame = v.read()
    if not ret:
        break

    if count == 0:
        prev = frame
        count += 1
        continue

    transMat = getAffMat(prev, frame)
    
    if transMat is not None:
        transforms[0].append(transMat[0][2])
        transforms[1].append(transMat[1][2])
        transforms[2].append(np.arctan2(transMat[1][0], transMat[0][0]))
        transforms[3].append(np.sqrt(transMat[1][0]**2 + transMat[0][0]**2))
    else:
        # Reuse previous transform if estimation fails
        transforms[0].append(transforms[0][-1])
        transforms[1].append(transforms[1][-1])
        transforms[2].append(transforms[2][-1])
        transforms[3].append(transforms[3][-1])

    prev = frame
    count += 1
    print(f"{count/n_frames*100:.2f}% completed")

v.release()

# Storing the data
with open('transforms.pkl', 'wb') as f:
    pickle.dump(transforms, f)
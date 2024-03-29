% legs
hipJoint = [0 0 0];
rightHip = hipJoint + [0 hip_hip/2 0];
rightKnee = rightHip + [0 0 -thigh_length];
rightAnkle = rightKnee + [0 0 -knee_ankle];

plot3([rightHip(1) rightKnee(1)], [rightHip(2) rightKnee(2)], [rightHip(3) rightKnee(3)], 'r', LineWidth=10);
plot3([rightKnee(1) rightAnkle(1)], [rightKnee(2) rightAnkle(2)], [rightKnee(3) rightAnkle(3)], 'g', LineWidth=10);

leftHip = HipJoint + [0 -hip_hip/2 0];
leftKnee = leftHip + [0 0 -thigh_length];
leftAnkle = leftKnee + [0 0 -knee_ankle];

plot3([leftHip(1) leftKnee(1)], [leftHip(2) leftKnee(2)], [leftHip(3) leftKnee(3)], 'r', LineWidth=10);
plot3([leftKnee(1) leftAnkle(1)], [leftKnee(2) leftAnkle(2)], [leftKnee(3) leftAnkle(3)], 'g', LineWidth=10);
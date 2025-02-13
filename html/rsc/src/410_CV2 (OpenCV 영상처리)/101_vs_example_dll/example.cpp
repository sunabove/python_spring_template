#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <chrono>

using namespace std;
using namespace cv;

int countFingers(vector<Point> contour, vector<Vec4i> defects) {
    int count = 0;
    for (size_t i = 0; i < defects.size(); i++) {
        Vec4i v = defects[i];
        Point start = contour[v[0]];
        Point end = contour[v[1]];
        Point far = contour[v[2]];
        double depth = v[3] / 256.0;

        if (depth > 20) {
            count++;
            circle(contour, far, 4, Scalar(0, 0, 255), -1); // 오목한 부분 표시
        }
    }
    return count;
}

string recognizeGesture(int fingerCount) {
    if (fingerCount == 0) return "Fist";
    if (fingerCount == 1) return "Thumbs Up";
    if (fingerCount == 5) return "Open Palm";
    return "";
}

int main() {
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        cerr << "Error: Could not open camera." << endl;
        return -1;
    }

    auto start = chrono::high_resolution_clock::now();
    int frame_count = 0;
    float fps = 0.0;

    while (true) {
        Mat frame;
        cap >> frame;
        if (frame.empty()) {
            cerr << "Error: Empty frame captured." << endl;
            break;
        }
        frame_count++;

        // HSV 색상 공간 변환
        Mat hsv_frame;
        cvtColor(frame, hsv_frame, COLOR_BGR2HSV);

        Scalar lower_skin(0, 20, 60);
        Scalar upper_skin(20, 255, 255);

        Mat skin_mask;
        inRange(hsv_frame, lower_skin, upper_skin, skin_mask);

        Mat morph_kernel = getStructuringElement(MORPH_ELLIPSE, Size(5, 5));
        morphologyEx(skin_mask, skin_mask, MORPH_CLOSE, morph_kernel);
        morphologyEx(skin_mask, skin_mask, MORPH_OPEN, morph_kernel);

        vector<vector<Point>> contours;
        vector<Vec4i> hierarchy;
        findContours(skin_mask, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

        Mat left_side = frame.clone();
        Mat right_side = Mat::zeros(left_side.size(), CV_8UC3);

        int fingerCount = 0;
        string gesture = "None";

        if (!contours.empty()) {
            auto largest_contour = max_element(contours.begin(), contours.end(),
                [](const vector<Point>& a, const vector<Point>& b) {
                    return contourArea(a) < contourArea(b);
                });

            // 손 검출
            drawContours(left_side, vector<vector<Point>>{*largest_contour}, -1, Scalar(0, 255, 0), 2);
            drawContours(right_side, vector<vector<Point>>{*largest_contour}, -1, Scalar(255, 255, 255), FILLED);
            drawContours(right_side, vector<vector<Point>>{*largest_contour}, -1, Scalar(0, 255, 0), 2);

            vector<int> hull;
            convexHull(*largest_contour, hull, false);

            vector<Vec4i> defects;
            if (hull.size() > 3) {
                convexityDefects(*largest_contour, hull, defects);
                fingerCount = countFingers(*largest_contour, defects);
                gesture = recognizeGesture(fingerCount);
            }
        }

        if (frame_count % 10 == 0) {
            auto end = chrono::high_resolution_clock::now();
            chrono::duration<float> duration = end - start;
            fps = frame_count / duration.count();
        }

        char fps_text[50], time_text[50];
        snprintf(fps_text, sizeof(fps_text), "FPS  : %5.2f", fps);
        snprintf(time_text, sizeof(time_text), "Time : %5.2f s", frame_count / fps);

        // 모든 텍스트 출력의 폰트 크기(scale)를 0.9로 맞춤
        putText(left_side, fps_text, Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 255, 0), 2);
        putText(left_side, time_text, Point(10, 60), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 255, 0), 2);
        // 오른쪽 하단에 배치
        putText(left_side, "Press 'q' to quit!", Point(10, left_side.rows - 20), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 0, 255), 2);

        char fingers_text[50];
        snprintf(fingers_text, sizeof(fingers_text), "Fingers: %d", fingerCount);
        putText(right_side, fingers_text, Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 255, 255), 2);
        putText(right_side, gesture, Point(10, 70), FONT_HERSHEY_SIMPLEX, 0.9, Scalar(0, 255, 255), 2);

        // 두 화면을 하나로 합치기
        Mat combined(frame.rows, frame.cols * 2, frame.type());
        left_side.copyTo(combined(Rect(0, 0, frame.cols, frame.rows)));
        right_side.copyTo(combined(Rect(frame.cols, 0, frame.cols, frame.rows)));

        imshow("Hand Detection", combined);

        if (waitKey(1) == 'q') {
            break;
        }
    }

    cap.release();
    destroyAllWindows();
    return 0;
}

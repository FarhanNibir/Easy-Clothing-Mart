import cv2

# Load the filter image
filter_img = cv2.imread('bra.jpg')

# Define the function that will apply the filter
def apply_filter(frame):
    # Resize the filter image to match the frame size
    filter_resized = cv2.resize(filter_img, (frame.shape[1], frame.shape[0]))
    # Apply the filter to the frame
    filtered = cv2.addWeighted(frame, 0.7, filter_resized, 0.3, 0)
    return filtered

# Open the camera
cap = cv2.VideoCapture(0)

# Loop through the frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    # Apply the filter to the frame
    filtered = apply_filter(frame)
    # Display the filtered frame
    cv2.imshow('Filtered', filtered)
    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

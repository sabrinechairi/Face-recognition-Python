import cv2
from simple_facerec import SimpleFacerec
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")


def face_recognition_photo(img_path):
    if not os.path.isfile(img_path):
        print("Invalid path to photo.")
        return

    img = cv2.imread(img_path)
    if img is None:
        print("Unable to read the photo.")
        return

    # Detect Faces
    face_locations, face_names, face_accuracies = sfr.detect_known_faces(img)
    for face_loc, name, accuracy in zip(face_locations, face_names, face_accuracies):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        title=f"{name}"
        cv2.putText(img,title, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 4)
        # Resize the image
        resized_img = cv2.resize(img, (800, 600))

        cv2.imshow("Photo", resized_img)
    cv2.imshow("Photo", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def face_recognition_video(video_path):
    if not os.path.isfile(video_path):
        print("Invalid path to video.")
        return

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detect Faces
        face_locations, face_names, face_accuracies = sfr.detect_known_faces(frame)
        for face_loc, name, accuracy in zip(face_locations, face_names, face_accuracies):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            title=f"{name}"
            cv2.putText(frame, title, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (16, 14, 200), 4)

        cv2.imshow("Video", frame)



        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord('a'):  # Press 'A' to deactivate the camera
            break
            # Resize the frame
            frame_resized = cv2.resize(frame, (800, 600))
            cv2.imshow("Video", frame_resized)

    cap.release()
    cv2.destroyAllWindows()

def face_recognition_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detect Faces
        face_locations, face_names, face_accuracies = sfr.detect_known_faces(frame)
        for face_loc, name, accuracy in zip(face_locations, face_names, face_accuracies):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            title=f"{name}"
            cv2.putText(frame,title, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 4)

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord('a'):  # Press 'A' to deactivate the camera
            break

    cap.release()
    cv2.destroyAllWindows()

def face_add_user():
    # Create a tkinter window
    window = tk.Toplevel()
    window.title("Add User")

    # Label for the camera feed
    video_label = tk.Label(window)
    video_label.pack(pady=10)

    # Label for image name
    name_label = tk.Label(window, text="Enter the name of the new user:")
    name_label.pack(pady=5)

    # Entry for user to input name
    name_entry = tk.Entry(window)
    name_entry.pack(pady=5)

    # Button to capture image
    capture_button = tk.Button(window, text="Capture Image")
    capture_button.pack(pady=5)

    # Button to try again
    try_again_button = tk.Button(window, text="Try Again")
    try_again_button.pack(pady=5)

    # Create a video capture object
    cap = cv2.VideoCapture(0)

    # Initialize variables
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    user_name = None

    # Function to capture an image
    def capture_image():
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Display the captured frame in the label
        img = Image.fromarray(frame)
        img.thumbnail((800, 700))  # Resize the image to fit the label
        img_tk = ImageTk.PhotoImage(image=img)
        video_label.config(image=img_tk)
        video_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Prompt the user to enter the name
        user_name = name_entry.get()

        # Save the captured image with the entered name
        image_path = f"images/{user_name}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as: {image_path}")
        sfr.load_encoding_images("images/")

    # Function to handle closing the window and releasing the video capture
    def close_window():
        cap.release()
        window.destroy()

    # Bind the close_window function to the window close event
    window.protocol("WM_DELETE_WINDOW", close_window)

    # Main loop to continuously update the camera feed
    def update_camera_feed():
        # Read a frame from the video capture
        ret, frame = cap.read()

        if ret:
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Resize the frame to fit the label
            frame_resized = cv2.resize(frame_rgb, (400, 300))

            # Convert the frame to ImageTk format
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the video label with the new frame
            video_label.config(image=img_tk)
            video_label.image = img_tk  # Keep a reference to avoid garbage collection

            # Schedule the update after 10 milliseconds
            window.after(10, update_camera_feed)

    # Start updating the camera feed
    update_camera_feed()

    def try_again():
        # Clear the name entry
        name_entry.delete(0, tk.END)

    # Configure button commands
    capture_button.config(command=capture_image)
    try_again_button.config(command=try_again)

    # Main loop
    window.mainloop()


def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path

def select_image():
    photo_path = open_file_dialog()
    if photo_path:
        face_recognition_photo(photo_path)

def select_video():
    video_path = open_file_dialog()
    if video_path:
        face_recognition_video(video_path)

def select_camera():
    face_recognition_camera()

# Define the key event handler
def on_key(event):
    if event.char == 'a':
        print("Camera deactivated")
        root.unbind('<Key>')
        root.update()

# Define the root GUI window
root = tk.Tk()
root.title("Face Recognition")

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Add buttons to the menu bar
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Select Image", command=select_image)
file_menu.add_command(label="Select Video", command=select_video)
file_menu.add_command(label="Select Camera", command=select_camera)
file_menu.add_command(label="Add User", command=face_add_user)
root.bind('<Key>', on_key)  # Bind the 'a' key to deactivate the camera

root.mainloop()

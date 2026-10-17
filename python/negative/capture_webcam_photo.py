def capture_webcam_photo(filename='photo.jpg', quality=0.8):#ModuleNotFoundError: No module named 'cv2' 
#even via pip was cv2 not found
    """
    Capture a photo from the webcam and save it to a file.
    Notes: Not working outside colab. !pip install -U cv2 can not be found. Extract the libs from a real colab environment and reqwrite the function to work in any env
    
    Depending on the environment, it uses:
    - Google Colab: JS webcam capture method
    - Jupyter Notebook: ipywidgets + OpenCV method (if available)
    - Local script: OpenCV VideoCapture method
    
    Args:
        filename (str): Filename to save the captured photo (default 'photo.jpg').
        quality (float): JPEG quality for Colab JS capture (ignored otherwise, default 0.8).
        
    Returns:
        str: The filename of the saved photo if successful.
        None: If capture failed or unsupported.
        
    Example:
        >>> capture_webcam_photo('my_photo.jpg')
        Saved to my_photo.jpg
    """
    import sys  # To check running environment
    import os
    import cv2

    # --- Helper: Colab webcam capture using JS ---
    def _capture_colab():
        from IPython.display import display, Javascript, Image
        from google.colab.output import eval_js
        from base64 import b64decode

        js = Javascript('''
        async function takePhoto(quality) {
          const div = document.createElement('div');  // Container div
          const capture = document.createElement('button');  // Capture button
          capture.textContent = 'Capture';
          div.appendChild(capture);

          const video = document.createElement('video');  // Video element
          video.style.display = 'block';
          const stream = await navigator.mediaDevices.getUserMedia({video: true});  // Get webcam stream

          document.body.appendChild(div);
          div.appendChild(video);
          video.srcObject = stream;
          await video.play();

          google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);  // Resize iframe

          await new Promise((resolve) => capture.onclick = resolve);  // Wait for click

          const canvas = document.createElement('canvas');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas.getContext('2d').drawImage(video, 0, 0);
          stream.getVideoTracks()[0].stop();
          div.remove();
          return canvas.toDataURL('image/jpeg', quality);
        }
        ''')
        display(js)  # Show capture UI
        data = eval_js(f'takePhoto({quality})')  # Run JS to get photo
        binary = b64decode(data.split(',')[1])  # Decode base64 to bytes
        with open(filename, 'wb') as f:
            f.write(binary)  # Write photo to file
        print(f'Saved to {filename}')
        display(Image(filename))  # Display photo inline
        return filename

    # --- Helper: Jupyter Notebook capture with ipywidgets and OpenCV ---
    def _capture_jupyter():
        try:
            import ipywidgets as widgets  # Widget UI components
            from IPython.display import display, Image, clear_output
            import threading
            import time

            cap = cv2.VideoCapture(0)  # Open default camera
            if not cap.isOpened():
                print("Cannot open webcam")
                return None

            # Widget image to display video feed
            image_widget = widgets.Image(format='jpeg')
            btn = widgets.Button(description="Capture")

            # Thread flag and frame buffer
            stopped = False
            frame = None

            def capture_loop():
                nonlocal frame
                while not stopped:
                    ret, img = cap.read()  # Read frame from camera
                    if not ret:
                        continue
                    _, jpeg = cv2.imencode('.jpg', img)  # Encode frame as JPEG
                    image_widget.value = jpeg.tobytes()  # Update widget image
                    frame = img
                    time.sleep(0.05)

            thread = threading.Thread(target=capture_loop)
            thread.start()

            def on_capture_clicked(b):
                nonlocal stopped
                stopped = True  # Stop video thread
                thread.join()
                cap.release()
                clear_output()
                cv2.imwrite(filename, frame)  # Save captured frame
                print(f'Saved to {filename}')
                display(Image(filename))

            btn.on_click(on_capture_clicked)

            display(image_widget, btn)
            return filename  # Note: user must click capture button manually
        except Exception as e:
            print(f"Jupyter capture error: {e}")
            return None

    # --- Helper: Local script capture with OpenCV VideoCapture ---
    def _capture_local():
        cap = cv2.VideoCapture(0)  # Open default camera
        if not cap.isOpened():
            print("Cannot open webcam")
            return None

        print("Press 'c' to capture photo, 'q' to quit")

        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow('Webcam', frame)  # Show live video

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):  # Capture on 'c'
                cv2.imwrite(filename, frame)
                print(f'Saved to {filename}')
                break
            elif key == ord('q'):  # Quit on 'q'
                print("Capture cancelled")
                break

        cap.release()
        cv2.destroyAllWindows()
        return filename

    # --- Main logic ---
    # Check if running in Colab
    if 'google.colab' in sys.modules:
        return _capture_colab()  # Use JS webcam capture

    # Check if running in Jupyter notebook
    try:
        get_ipython  # If this exists, running in IPython/Jupyter
        if 'ipykernel' in sys.modules:
            return _capture_jupyter()  # Use ipywidgets + OpenCV capture
    except NameError:
        pass

    # Fallback to local script capture
    return _capture_local()

# Example usage:
#capture_webcam_photo('my_photo.jpg')

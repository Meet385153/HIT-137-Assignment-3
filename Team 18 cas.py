# Group Name : Group 18 Cas

# Group Members:
# Meet Pandya - s385153
# Dhrumil Patel - s384146




# code for browse image and load in application window from local device
# code for cropping and resizing image 
# code for saving that image 






import tkinter as tk                                    # Import the tkinter module for GUI
from tkinter import Label, filedialog, messagebox       # Import necessary components from tkinter
from PIL import Image, ImageTk                          # Import ImageTk and Image from the pillow library for image handling 
import cv2                                              
import numpy as np



# Initialize global variables for cropping functionality
rect_start = None                                       # Starting point of the rectangle 
rect_end = None                                         # Ending point of the rectangle  
is_drawing = False                                      # Flag to check if rectangle drawing is in progress
cropped_image = None                                    # For holding the  cropped image 
original_image = None                                   # For holding the original image 

# Creating main window for the application
root = tk.Tk()
root.title("Image Cropping and resizing application")

# Create a frame to organize layout
frame = tk.Frame(root, bg="green")  

# Labels and Entry widgets in application
lbl_pic_path = tk.Label(frame, text="Image Path:", padx=30, pady=30, font=('verdana', 16), bg="green")
entry_pic_path = tk.Entry(frame, font=('verdana', 16))

# Label to display image in the application
thumbnail_label = tk.Label(frame)
thumbnail_label.grid(row=1, column=0, padx=(50,70))

# Label to show preview of cropped image in the application
preview_label = tk.Label(frame)
preview_label.grid(row=1, column=3, padx=(50,70))

# Function to handle image selection and display
def selectPic():
    global original_image, rect_start, rect_end, is_drawing, cropped_image
    filename = filedialog.askopenfilename(initialdir="/images", title="Select Image", 
                                           filetypes=[("PNG", "*.png"), 
                                                      ("JPEG", "*.jpg;*.jpeg"), 
                                                      ("GIF", "*.gif"), 
                                                      ("BMP", "*.bmp")])
    if filename:
        entry_pic_path.delete(0, tk.END)                        # Clear the previous text from the entry field
        entry_pic_path.insert(0, filename)                      # Insert the selected file path into the entry field
 
        original_image = cv2.imread(filename)                   # Read the selected image using OpenCV
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)        # Convert the image from BGR to RGB format
        
        # Create a thumbnail for display
        thumbnail  = cv2.resize(original_image_rgb, (200,200))
                            
        thumbnail_image = Image.fromarray(thumbnail )                    # Convert to PIL image 
        thumbnail_image = ImageTk.PhotoImage(thumbnail_image)           # Convert to Tkinter-compatible image
        thumbnail_label.config(image=thumbnail_image)                   # Display the thumbnail                
        thumbnail_label.image= thumbnail_image                          
         


        # Reset cropping-related variables
        rect_start = None
        rect_end = None
        is_drawing = False
        cropped_image = None

        cv2.imshow("Original Image", original_image)                        # Display the original image in OpenCV window
        cv2.setMouseCallback("Original Image", draw_rectangle)              # Set mouse callback function for cropping


# Function to handle mouse interaction for cropping
def draw_rectangle(event, x, y, flags, param):
    global rect_start, rect_end, is_drawing, original_image, cropped_image

    if event == cv2.EVENT_LBUTTONDOWN:  # Mouse press, start drawing
        rect_start = (x, y)             # To  Record the starting point
        is_drawing = True               # Set flag that rectangle drawing is in progress

    elif event == cv2.EVENT_MOUSEMOVE:  # Mouse drag, update the rectangle
        if is_drawing:
            rect_end = (x, y)           # Update the end point
            temp_image = original_image.copy()                # Make a copy of the  original image  
            cv2.rectangle(temp_image, rect_start, rect_end, (0, 255, 0), 2)    # Draw the rectangle
            cv2.imshow("Original Image", temp_image)               # Display the image with rectangle in OpenCV window

    elif event == cv2.EVENT_LBUTTONUP:  # Mouse release, finalize the rectangle
        is_drawing = False             # End drawing
        rect_end = (x, y)              # Finalize the end point

        x1, y1 = rect_start             # Get starting point
        x2, y2 = rect_end               # Get ending point
        cropped_image = original_image[y1:y2, x1:x2]                     # Crop the image using the coordinates
 
        cv2.imshow("Cropped Result", cropped_image)                     # Show the cropped image in OpenCV window

# Function to update the preview size of the cropped image using a slider
def update_preview_size(val):
    if cropped_image is not None:
        resize_factor = int(val) / 100.0             # Calculate resize factor based on slider value
        resized_image = cv2.resize(cropped_image, None, fx=resize_factor, fy=resize_factor)             # Resize the image
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)             # Convert resized image to RGB
        img_pil = Image.fromarray(resized_image_rgb)           # Convert to PIL image
        img_tk = ImageTk.PhotoImage(img_pil)                   # Convert to Tkinter-compatible image


        preview_label.config(image=img_tk)         # Update the preview label with resized image
        preview_label.image = img_tk

# Function to save the final image
def save_image():
    if cropped_image is not None:               #  Check if there is a cropped image to save
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), 
                                                                                     ("PNG files", "*.png"),
                                                                                     ("GIF", "*.gif"),
                                                                                       ("BMP", "*.bmp")])
        if save_path:
            cv2.imwrite(save_path, cropped_image)        # Save the cropped image to the selected path
            messagebox.showinfo("Save", "Image saved successfully!")       # Show successfull message 
    else:
        messagebox.showerror("Error", "No cropped image to save.")        # Error to save image message 

# Button to select an image file
btn_browse = tk.Button(frame, text="Select Image", bg="grey", fg="#ffffff", font=('verdana', 16), command=selectPic)

# Slider for resizing the cropped image (10 to 150 for scaling factor)
resize_slider = tk.Scale(frame, from_=10, to=150, orient="horizontal", label="Resize Preview", command=update_preview_size)
resize_slider.set(75)     # To set default value 

# Save image button
save_button = tk.Button(frame, text="Save Cropped Image", command=save_image)

# Packing the widgets
frame.pack(padx=20, pady=20)
lbl_pic_path.grid(row=0, column=0)
entry_pic_path.grid(row=0, column=1, padx=(0, 20))
btn_browse.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
resize_slider.grid(row=3, column=0, columnspan=2)
save_button.grid(row=4, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()

# Close OpenCV windows after GUI is closed
cv2.destroyAllWindows()

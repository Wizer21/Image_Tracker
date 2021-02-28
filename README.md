# Image Tracker

This program allows you to find complex shapes from an image, depending on their color

# Image
## Explore the pixel map
 - The program crosses every line of the map to find lines which are matching* the chosen color
 - Lines are stored in a dictionnary with their Y position as keys
 
## Rows compilation 
 - The program crosses every row, step* by step and check if the current row's Y position is already in the dictionnary
 - In this case, new rows are stored in a list of temporary shapes
 - Every new line added in a temparory shape will become the key for joining the latter
    - For example:
       My shape has defined entry keys like [ X= 10, X= 15 ]
       If I find the pattern [ X= 5, X= 15 ] in the next row
       The line will be inserted in my shape and becomes the entry keys for the next following rows

## Compile nearby shapes
If my shape is not perfectly monochrome, such as a red book that contains white text, this will create multiple shapes
So I might activate this option to compile nearby shapes 
- It will examine every shape and check if they have common Top/Left and Bottom/Right points
     
<img width="1000" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=1UDICYAB0Oj8HggUOFTqwQXG0FRzSw6Dp">
<img width="1000" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=1q5OCfY6mxUWCAMGVXeyO0GLxyW2rPKt4">


# Video

## Initiation

By clicking on the image, the algorithm will get the pixel clicked and start tracking it. 

## Tracking

- At every frame the algorithm will, from the previous position, search in 8 directions until pixels do not match anymore the selected color.
- This way the algorithm will get 8 positions that will allow it to build a shape structure with corners positions, width, height and center.
- Every time a pixel color matches, its rgb will be added to a stack that is divided by the number of pixels the latter contains to continuously set an average color. This way, the algorithm will handle brightness variations.

# Notes

 *matching: the user selects a pixel from the image and an acceptable range  
    - The rgb(12, 150, 255), with a range of 10, will include pixels that have rgb between (2, 140, 245) and (22, 160, 255)  
 *step: int value selected by the user  
    - The step represents the X distance between every analysis  
        
<img width="1000" alt="Failure to load gif, open there" src="https://drive.google.com/uc?export=view&id=1mpBGipsDrsT5TO_yDlGrIN4OU3TMmTED">

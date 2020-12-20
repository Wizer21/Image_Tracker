# Image Tracker

This program allows you to find complex shapes from an image, depending on their color

# Algorithm
## Explore the pixel map
 - The program crosses every line of the map to find lines which are matching* the chosen color
 - Lines are stored in a dictionnary with their Y position as keys
 
## Rows ompilation 
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
 
 
 *matching: the user selects a pixel from the image and an acceptable range  
    - The rgb(12, 150, 255), with a range of 10, will include pixels that have rgb between (2, 140, 245) and (22, 160, 255)  
 *step: int value selected by the user  
    - The step represents the X distance between every analysis  
    
        
<img width="508" alt="imagetracker" src="https://user-images.githubusercontent.com/72104477/102719846-b9b28200-42f0-11eb-821c-af5988e5fef0.png"><img width="1136" alt="bananatracker" src="https://user-images.githubusercontent.com/72104477/102719762-4b6dbf80-42f0-11eb-9915-743fc8040181.png">

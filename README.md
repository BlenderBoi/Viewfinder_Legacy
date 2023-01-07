# Viewfinder

![Banner](https://user-images.githubusercontent.com/79613445/210192287-dd02b6c8-7154-47a6-af05-65383c3178ef.png)

Viewfinder is an Addon that Helps provides Utility and Camera Related Tools. It Helps With Managing Cameras In Your Scene

![ViewfinderScreenshot](https://user-images.githubusercontent.com/79613445/210192365-acc5ad68-c66f-4f4d-989f-0413523a5d64.png)




[ViewfinderDemoNew.webm](https://user-images.githubusercontent.com/79613445/211127994-f9ab8597-4697-4326-a8f4-92f8eb9ca3b9.webm)






# Camera Preview

You can Preview Your Camera inside your Viewport Visually

    Note: Cycles Render will not show in Camera Preview

[CameraPreview.webm](https://user-images.githubusercontent.com/79613445/210196869-9d2a11bf-7c0d-4d2b-8b32-7b569018f41d.webm)

## Limitation!

If you Use Left Click Select, it Might Make Gizmo Unclickable, to fix this problem, Make Sure to Change Your

    Preferences-> Keymap-> Activate Gizmo Event

Change it from "Drag" to "Press" to fix this problem

[Minorfix.webm](https://user-images.githubusercontent.com/79613445/210192334-dc32fcb5-ab01-4306-82bb-0f78b46fab9a.webm)


# Camera List

List your camera in the side panel, simplify the process of managing multiple camera in the scene.

![CameraList](https://user-images.githubusercontent.com/79613445/210196911-cd6e00f0-33ca-4f57-a47a-add6bf788b0e.png)

## Camera List Buttons

With each Camera Item Listed, You can Do the Following. 

- View the Camera
- Select the Camera
- Find the Camera (Frame Selected)
- Bind Camera to Timeline Markers
- Remove the Camera
- Change the Camera Settings

![Viewfinder_Item](https://user-images.githubusercontent.com/79613445/210196961-cd04ba8b-38ac-4712-86be-a771828533e6.png)



# Camera Utility Operator

## New Camera From View

You can Create New Camera From View which is a more Intuitive Way of Adding New Camera and Bind Camera to Timeline Marker at Current Frame When you Create The Camera

[CameraFromView.webm](https://user-images.githubusercontent.com/79613445/211126818-7244948e-532c-45db-87c6-ca5fd3fa8c85.webm)



## Camera Booth

Create A "Camera Booth" where it have Camera In Angles from Many Views

[CameraBooth.webm](https://user-images.githubusercontent.com/79613445/211126734-aeaafcf4-498e-4657-a862-9c4842ae5dce.webm)



Can Be useful if you Want to Render For 2.5D Sprite Render, or if You want to Quickly Render Your Model From Multiple Angles. 

![MultiAngle](https://user-images.githubusercontent.com/79613445/210203736-064d28e6-2442-412e-a7fa-3c3a876a31fb.png)


## Markers From Selected Camera

Bind Camera to Timeline Markers and Increment their Frame on Selected Cameras

[MarkerFromCamera.webm](https://user-images.githubusercontent.com/79613445/211126774-d5a0a2b0-e7ee-4933-8d33-4fbf6cf8a2ab.webm)


## Other Features

### Create Clamped Camera From Selected Curves

Create Camera on Curve and Apply Clamped to Constraint on the Selected Curves


### Create Empty Target From Camera 

Create Empty Target for Selected Camera and Apply Track to or Damped Track Constraint. 


### Create Camera And Empty Target 

Create Camera and A Empty with Track to Or Damped Track Constraint Applied. While You can do this manually easily, this could saves a few clicks, 

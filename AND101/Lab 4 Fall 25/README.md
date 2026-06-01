## Lab #4: Red Button

Submitted by: **Ryan Lawton**

### Overview

Congratulations! 🎉 You have been selected by your dream company to participate in a debugging challenge that was designed to find the best talents in Android Development. The winners of this challenge will be granted a full-time offer in the company's Mobile Software Engineering department - this is a once in a lifetime opportunity!

### 🎯 Goals

By the end of this lab you will be able to...

- [x] Debug an app using Android Studio
- [x] Understand Views and view hierarchies
- [x] Understand interaction through click listeners
- [x] Understand View type casting

### Resources

- [Debugging in Android Studio](https://developer.android.com/studio/debug)
- [Debug your Layout with Layout Inspector](https://developer.android.com/studio/debug/layout-inspector)
- [Write and View Logs with Logcat](https://developer.android.com/studio/debug/am-logcat)

## Lab Instructions

### Lab Setup

Before diving into the challenge, we need to clone the starter version of the app:

`https://github.com/driuft/redbutton-debugging-challenge.git`

### Challenges

#### Step 0: App Crashes

In this step, the app crashes automatically when launching.

- [x] Check `Logcat` for crash-related errors - are there any blue hyperlinks pointing to specific lines of code?
- [x] Make necessary changes in the code to allow the app to run

#### Step 1: Something Is Preventing Clicks

The app should now launch successfully, but there is something preventing interaction with the Blue button. Usually there is a [Ripple Animation](https://guides.codepath.com/android/ripple-animation) that occurs when the button is clicked, but nothing seems to be happening.

- [x] Open `activity_main.xml`
- [x] Find any View that might be obstructing our Button from being clicked and **modify/delete** it
- [x] Re-run the app

#### Step 2: A Wild Blue Button Appeared!

The blue button decided to celebrate Halloween early this year with a costume of the red button. It is telling us to check our layout file. Let's try to change the `visibility` of the blue button.

- [x] Open `activity_main.xml`
- [x] Change the visibility of the Button with id `blue_button` to `gone`
- [x] Re-run the app

#### Step 3: That Is One Tiny Yellow Button

There is now a tiny yellow button shown. It's a bit small to be interacted with, so let's try to increase its size.

💡 PRO TIP: Press and hold the _tiny_ button if you are feeling lucky today

- [x] Open `activity_main.xml`
- [x] Find the Button with id `tiny_yellow_button`
- [x] Change its size to allow easier interactivity
- [x] Re-run the app
- [x] Press and hold the Button to trigger its `longClickListener()`

#### Step 4: The Red Button

Is this the **real** red button? Has our journey finally come to an end? Only one way to find out.

- [x] Tap the red button

🎉 Congratulations, you've successfully completed the challenge! 🎉
You have shown that you are more than capable as an Engineer, and the company will be extending an offer. Now go change the world! 🚀

## Video Demo

Here's a video / GIF that demos all of the app's implemented features:

![Demo](https://i.imgur.com/Az4pZKV.gif)

🔗 [Can't see the GIF? Click here to view it directly on Imgur](https://i.imgur.com/Az4pZKV.gif)

GIF created with **EZGif**

<!-- Recommended tools:
- [Kap](https://getkap.co/) for macOS
- [ScreenToGif](https://www.screentogif.com/) for Windows
- [peek](https://github.com/phw/peek) for Linux. -->

## License

Copyright **2025** **Ryan Lawton**

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

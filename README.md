<div align="center">

# BOTTLE CRATE INSPECTION USING OPENCV

</div>

#### This project provides a tool to analyze the quality of crates with classical image processing techniques using OpenCV.

<br>
<br>
<div align="center">

![image2](assets/results/output_bottle_crate_01.png)


<br>

![image1](assets/results/output_bottle_crate_02.png) 

</div>
<br>
<br>

<div align="center">
    <table>
        <tr>
            <td><img src="assets/results/output_bottle_crate_02.png" alt="Image 2" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_06.png" alt="Image 6" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_07.png" alt="Image 7" width="300"/></td>
        </tr>
        <tr>
            <td><img src="assets/results/output_bottle_crate_09.png" alt="Image 9" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_10.png" alt="Image 10" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_12.png" alt="Image 12" width="300"/></td>
        </tr>
        <tr>       
            <td><img src="assets/results/output_bottle_crate_14.png" alt="Image 14" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_15.png" alt="Image 15" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_16.png" alt="Image 16" width="300"/></td>
        </tr>
        <tr>
            <td><img src="assets/results/output_bottle_crate_13.png" alt="Image 13" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_17.png" alt="Image 17" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_19.png" alt="Image 19" width="300"/></td>
        </tr>
        <tr>
            <td><img src="assets/results/output_bottle_crate_08.png" alt="Image 8" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_04.png" alt="Image 4" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_03.png" alt="Image 3" width="300"/></td>
        </tr>
        <tr>
            <td><img src="assets/results/output_bottle_crate_20.png" alt="Image 20" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_01.png" alt="Image 1" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_05.png" alt="Image 5" width="300"/></td>
        </tr>
        <tr>
            <td><img src="assets/results/output_bottle_crate_11.png" alt="Image 11" width="300"/></td>
            <td><img src="assets/results/output_bottle_crate_18.png" alt="Image 18" width="300"/></td>
        </tr>
    </table>

</div>

<br>
<br>

## Features

- Analyzes the quality of a crate based on an image.
- Outputs the quality of the crate and displays the processed image.

## Requirements

- OpenCV
- PyYAML

## Usage

To use the Crate Quality Analyzer, you need to provide an image of the crate as a command-line argument:

```sh
python3 inspect_crate.py <image_path>
```

This will output the quality of the crate and display the processed image.`

## Configuration

The settings for the image processing parameters can be configured in the [settings.yaml](config/setting.yaml) file.Here you can set parameters for the Canny edge detection, Hough Circle Transform, image dimensions, crate dimensions, template matching, and more.

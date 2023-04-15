<div id="top"></div>

[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


# whisper-auto-transcribe

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Easily generate free subtitles for your video</h3>
      

  <a href="https://github.com/tomchang25/whisper-auto-transcribe">
    <img src="images/logo.png" alt="Logo" width="400" height="400">
  </a>

  <p align="center">
    <br />
    <a href="https://github.com/tomchang25/whisper-auto-transcribe#Demo">View Demo</a>
    ·
    <a href="https://github.com/tomchang25/whisper-auto-transcribe/issues">Report Bug</a>
    ·
    <a href="https://github.com/tomchang25/whisper-auto-transcribe/issues">Request Feature</a>
  </p>
  



</div>

<!-- ABOUT THE PROJECT -->
## About The Project
### Features:

- Automatically generates subtitles for video or audio content
- Translates content to English
- Supports 99 languages
- Offers high accuracy and ease of use
- Provides support for GPU acceleration and CLI mode

### Unique feature:

- Includes a one-click installer
- Increased time precision from 1 to 0.01 seconds
- Supports Youtube integration
- Preview subtitles in video
- Provides support for Background Music Mute, works fine even during heavy metal live performances
- Supports long files, 3-hour files have been tested
- Resolves the issue of subtitle repetition

### Future feature:

- Subtitle editing
- Easy batch processing function
- Improved translation


The tool is based on [OpenAI-whisper](https://github.com/openai/whisper), the latest project developed by OpenAI. 

For more details, you can check [this](https://cdn.openai.com/papers/whisper.pdf).


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation

1. Install [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads)

2. Clone the repo
   ```sh
   # Stable version
   git clone https://github.com/tomchang25/whisper-auto-transcribe.git
   cd whisper-auto-transcribe
   
   # If you want to test the unique feature in v3.0
   git clone --branch v3-alpha https://github.com/tomchang25/whisper-auto-transcribe.git whisper-auto-transcribe-v3
   cd whisper-auto-transcribe-v3
   ```


3. Open webui.bat

4. Check for any errors and ensure that the final lines are correct.
   ```
   Launching Web UI with arguments: 
   Running on local URL:  http://127.0.0.1:7860
   ```

5. Open your browser and go to `http://127.0.0.1:7860`

   
<!-- GPU acceleration -->
## (Optional) GPU acceleration (CUDA.11.3)

1. Install [CUDA](https://developer.nvidia.com/cuda-11.3.0-download-archive)
2. Install [CUDNN](https://developer.nvidia.com/rdp/cudnn-archive)
3. Unistall CPU version Pytorch
   ```sh
   pip uninstall torch torchvision torchaudio
   ```
4. Reinstall [GPU version Pytorch](https://pytorch.org/get-started/locally/)
   ```sh
   # on Windows
   python -m pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1+cu113 -f https://download.pytorch.org/whl/torch_stable.html
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- How to use -->
## How to use
  <img src="images/Demo1.png" alt="How to use" width="800" height="450">
  
## Command-line interface
   ```sh
   # Get help messages
   python .\cli.py -h
   
   # A simple example
   python .\cli.py .\mp4\1min.mp4 --output .\tmp\123456.srt -lang ja --task translate --model small
   ```


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Demo -->
## Demo
  ### Heavy Metal [Watch on Youtube](https://www.youtube.com/watch?v=Z0n1N3n9tR0)
  ```
  404
  0:53:33.590 --> 0:53:38.190
  From the depths of hellish silence, bastard spells, explosive violence
  (From the depths of hell in silence, Cast their spells, explosive violence)

  405
  0:53:38.670 --> 0:53:43.190
  Russian minds have my protected, glorious mission undetected
  (Russian night time flight perfected, Flawless vision, undetected)

  406
  0:53:44.190 --> 0:53:48.190
  Put down in all the flames, I'm going strong, I'm half-moon's number one
  (Pushing on and on, their planes are going strong, Air Force number one)

  407
  0:53:49.110 --> 0:53:53.030
  Talking with the moon, looking for the truth, I'm moon's number one
  (Somewhere down below they're looking for the foe, Bomber's on the run)

  408
  0:53:53.870 --> 0:53:58.190
  You can hide, you can move, just to write, learn to expect, learn to think dark
  (You can't hide, you can't move, just abide, Their attack's been proved (raiders in the dark))

  409
  0:53:59.110 --> 0:54:03.190
  Silence is the night, the witch is in the fight, never miss the mark
  (Silent through the night the witches join the fight. Never miss their mark)

  410
  0:54:04.150 --> 0:54:08.090
  Canvas, wings of death, the pattern is your fate
  (Canvas wings of death, Prepare to meet your fate)

  411
  0:54:09.190 --> 0:54:13.030
  Night on the regiment, 188
  (Night Bomber Regiment, 588)

  412
  0:54:14.190 --> 0:54:19.090
  Undetected, unexpected, wings of glory, tell the story
  (Undetected, unexpected, Wings of glory, Tell their story)

  413
  0:54:19.530 --> 0:54:24.110
  Deviation, deviation, undetected, stealth, perfected
  (Aviation, deviation, Undetected, Stealth perfected)

  414
  0:54:24.330 --> 0:54:28.150
  Silence in ground, retreated to the sound, helpless in the air
  (Foes are losing ground, retreating to the sound, Death is in the air)

  415
  0:54:29.130 --> 0:54:33.150
  Suddenly appears, the world in your face, mindful, the witch is there
  (Suddenly appears, confirming all your fears, Strike from witches lair)

  416
  0:54:33.830 --> 0:54:36.850
  Let it fall, come around, I don't sound so, we're about to drown
  (Target found, come around, barrels sound, From the battleground)

  417
  0:54:37.210 --> 0:54:41.210
  Lashes, standing high, the old genie awaits, the beaten at the gates
  (Rodina awaits, defeat them at the gates, Live to fight and fly)

  418
  0:54:41.790 --> 0:54:43.430
  Just to fight and fly
  ()

  419
  0:54:44.250 --> 0:54:48.190
  Canvas, wings of death, the pattern is your fate
  (Canvas wings of death, Prepare to meet your fate)

  420
  0:54:49.270 --> 0:54:53.070
  Night on the regiment, 188
  (Night Bomber Regiment, 588)

  421
  0:54:54.190 --> 0:54:59.110
  Undetected, unexpected, wings of glory, tell the story
  (Undetected, unexpected, Wings of glory, Tell their story)

  422
  0:54:59.470 --> 0:55:04.110
  Deviation, deviation, undetected, stealth, perfected
  (Aviation, deviation, Undetected, Stealth perfected)

  423
  0:55:24.140 --> 0:55:27.410
  Beneath the starlight of the heavens
  (Beneath the starlight of the heavens)

  424
  0:55:29.200 --> 0:55:31.720
  Unlikely heroes in disguise
  (Unlikely heroes in the skies)

  425
  0:55:31.720 --> 0:55:34.040
  Canvas, wings of death, the witch is gonna die
  (Canvas wings of death, Prepare to meet your fate)

  426
  0:55:34.660 --> 0:55:37.320
  Stay in fear, humble horizon
  (As they appear on the horizon)

  427
  0:55:39.540 --> 0:55:43.460
  Win when wisdom, and the night witch has come
  (The wind will whisper when the Night Witches come)

  428
  0:55:44.460 --> 0:55:48.560
  Undetected, unexpected, wings of glory, tell the story
  (Undetected, unexpected, Wings of glory, Tell their story)

  429
  0:55:49.480 --> 0:55:53.540
  Deviation, deviation, undetected, stealth, perfected
  (Aviation, deviation, undetected, Stealth perfected)

  430
  0:55:54.340 --> 0:55:58.140
  From the depths of hell in silence, lost in spells, explosive violence
  (From the depths of hell in silence, Cast their spells, explosive violence)

  431
  0:55:59.260 --> 0:56:04.220
  Russian beta, but perfected, bonus mission, undetected
  (Russian night time flight perfected, Flawless vision, undetected)

   ```

  ### English [Watch on Youtube](https://youtu.be/SJ-11ZX1N4w)
   ```
   0
   0:00:00,0 --> 0:00:10,0
    The most popular is the Yashino Nakama, which stands on the shore of the Makurazaki City in Kagoshima Prefecture.
   
   1
   0:00:11,0 --> 0:00:22,0
    Makurazaki City used to be called the Typhoon Ginza, and the typhoon was approaching it frequently.
   
   2
   0:00:22,0 --> 0:00:27,0
    On Sunday, the Typhoon Ginza approached the Makurazaki City.
   
   3
   0:00:28,0 --> 0:00:41,0
    One of the four trees was named Yasshi on SNS, and there were many supportive comments.
   
   4
   0:00:42,0 --> 0:00:44,0
    Yasshi, do your best!
   
   5
   0:00:45,0 --> 0:00:47,0
    Yasshi, run away quickly!
   
   6
   0:00:47,0 --> 0:00:51,0
    Run away? If you have to, take off your roots and run away?
   
   7
   0:00:51,0 --> 0:01:17,0
    There are also voices asking to sell Yasshi goods.
   
   

   ```
   
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Limitation -->
## Limitation

Currently, there are several restrictions on this project.

1. GPU acceleration only works on CUDA environment.

Also, if you want to use GPU acceleration, please make sure you have enough GPU VRAM.
Here is some recommended value.


| Precision |    Whisper model   | Required VRAM |   *Time used   |   Performance  |
|:---------:|:------------------:|:-------------:|:--------------:|:--------------:|
|     1     |       `tiny`       |     ~1 GB     |      ~1/20      |    ~Disaster   |
|     2     |       `base`       |     ~1 GB     |      ~1/10      |    ~Youtube    |
|     3     |      `small`       |     ~2 GB     |      ~1/8      |       -        |
|     4     |      `medium`      |     ~5 GB     |      ~1/5      |       -        |
|     5     |      `large`       |    ~10 GB     |      ~1/2      |    ~Sonix.ai   |

*Time used is relatived to video/audio time and test in 10 min Enlgish audio with GPU acceleration.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Report Bugs: https://github.com/tomchang25/whisper-auto-transcribe/issues

Project Link: https://github.com/tomchang25/whisper-auto-transcribe

My twitter: https://twitter.com/Greysuki

My Gmail: tomchang25@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

The code and the model weights of Whisper are released under the MIT License. 

This project is distributed under the MIT License. Please refer to `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [OpenAI-whisper](https://github.com/openai/whisper)
* [Gradio](https://gradio.app/)
* [Demucs](https://github.com/facebookresearch/demucs)
* [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[stars-shield]: https://img.shields.io/github/stars/tomchang25/whisper-auto-transcribe.svg?style=for-the-badge
[stars-url]: https://github.com/tomchang25/whisper-auto-transcribe/stargazers
[issues-shield]: https://img.shields.io/github/issues/tomchang25/whisper-auto-transcribe.svg?style=for-the-badge
[issues-url]: https://github.com/tomchang25/whisper-auto-transcribe/issues
[license-shield]: https://img.shields.io/github/license/tomchang25/whisper-auto-transcribe.svg?style=for-the-badge
[license-url]: https://github.com/tomchang25/whisper-auto-transcribe/LICENSE.txt


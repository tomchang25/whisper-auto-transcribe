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
- Supports Youtube integration
- Preview subtitles in video
- Provides support for Background Music Mute, works fine even during rock live performances
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
<div align="center">
  <h3 align="center">Auto generate subtitle from video and translate to English</h3>
  
  ### [Demo on Youtube](https://www.youtube.com/watch?v=y-Df1gA8TeQ)
  ### [Video source (no subtitle)](https://www.youtube.com/watch?v=6w-AvMZT3TY)
</div>

  ### Japanese [Watch on Youtube](https://youtu.be/kec6Kk8b4G0)
   ```
   0
   0:00:00,0 --> 0:00:09,580
   人気を集めているのは鹿児島県 枕崎市の海沿いに立つ高さ20メートルを超える

   1
   0:00:09,580 --> 0:00:16,320
   八市の仲間です 枕崎市はかつては台風銀座と言われるほど

   2
   0:00:16,320 --> 0:00:24,120
   台風の接近が多くこの場所は何度も台風中継に使われてきました

   3
   0:00:24,120 --> 0:00:27,120
   ん

   4
   0:00:27,480 --> 0:00:36,600
   台風14号が接近した日曜日 4本ある木のうちの1本が sns 上で

   5
   0:00:36,600 --> 0:00:45,200
   ヤッシーと名付けられ強風に耐える姿に応援コメントが続出しました よし頑張れ

   6
   0:00:45,200 --> 0:00:54,320
   や c 早く逃げろ イザとなったら根っこを外して逃げろ

   7
   0:00:54,320 --> 0:01:16,760
   欲しいという声もあるということです


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
2. File time should not exceed 30 min, because of the performance problem.

Also, if you want to use GPU acceleration, please make sure you have enough GPU VRAM.
Here is some recommended value.


| Precision |    Whisper model   | Required VRAM |   *Time used   |   Performance  |
|:---------:|:------------------:|:-------------:|:--------------:|:--------------:|
|     1     |       `tiny`       |     ~1 GB     |      ~1/20      |    ~Disaster   |
|     2     |       `base`       |     ~1 GB     |      ~1/10      |    ~Youtube    |
|     3     |      `small`       |     ~2 GB     |      ~1/8      |       -        |
|     4     |      `medium`      |     ~5 GB     |      ~1/5      |       -        |
|     5     |      `large`       |    ~10 GB     |      ~1/2      |    ~Sonix.ai   |

*Time used is relatived to video/audio time and test in 7 min Enlgish audio with GPU acceleration.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Report Bugs: [https://github.com/tomchang25/whisper-auto-transcribe/issues]

Project Link: [https://github.com/tomchang25/whisper-auto-transcribe](https://github.com/tomchang25/whisper-auto-transcribe)

My twitter: [https://twitter.com/Greysuki]

My Gmail: tomchang25@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

The code and the model weights of Whisper are released under the MIT License. 
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [OpenAI-whisper](https://github.com/openai/whisper)
* [Gradio](https://gradio.app/)
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


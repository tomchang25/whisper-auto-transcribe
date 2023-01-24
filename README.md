<div id="top"></div>

[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


# whisper-auto-transcribe

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Whisper Auto Transcribe</h3>
  
  <a href="https://github.com/tomchang25/whisper-auto-transcribe">
    <img src="images/logo.png" alt="Logo" width="400" height="400">
  </a>

  <p align="center">
    The most efficient subtitle solution.
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

The tool is based on [OpenAI-whisper](https://github.com/openai/whisper), the latest project developed by OpenAI. 

For more details, you can check [this](https://cdn.openai.com/papers/whisper.pdf).

Features:

- Auto generates subtitle from video/audio
- Auto translate to English
- 99 language support
- High accuracy. Easy to use.
- GPU acceleration
- CLI mode for batch task
- More features are coming soon

<!--
I made some changes to output the subtitle files, and added a graphical interface.

If you don't want to read an academic paper, this tool can be summed up in one sentence: 

   ```sh
   AI will auto generate subtitle, with more accuracy than most transcribe commercial software.
   The most important, it's FREE!
   ```
-->

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


<!-- GETTING STARTED -->
## Installation (New)

1. Install [Python 3](https://www.python.org/downloads/)
2. Clone the repo
   ```sh
   git clone https://github.com/tomchang25/whisper-auto-transcribe.git
   cd whisper-auto-transcribe
   ```

2. Open webui.bat

3. Check there is no error and last lines are
```
Launching Web UI with arguments: 
Running on local URL:  http://127.0.0.1:7860
```

4. Open browser and enter http://127.0.0.1:7860

## Installation (Old, you don't need this unless something fuck up...or your os isn't Windows)

1. Install [Python 3](https://www.python.org/downloads/)

2. Clone the repo
   ```sh
   git clone https://github.com/tomchang25/whisper-auto-transcribe.git
   cd whisper-auto-transcribe
   ```
3. Install dependency
   ```sh
   pip install git+https://github.com/openai/whisper.git 
   pip install gradio
   ```
4. Install [ffmpeg](https://ffmpeg.org/)
   ```sh
   # on Ubuntu or Debian
   sudo apt update && sudo apt install ffmpeg

   # on MacOS using Homebrew (https://brew.sh/)
   brew install ffmpeg

   # on Windows using Chocolatey (https://chocolatey.org/)
   choco install ffmpeg

   # on Windows using Scoop (https://scoop.sh/)
   scoop install ffmpeg

   ```
5. Open application
   ```sh
   python gui.py
   ```

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
   
<!-- Accompaniment separation -->
## (Optional) Accompaniment separation (WIP)

1. Install [Zlib](https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#install-zlib-windows)
2. Install [Spleeter](https://github.com/deezer/spleeter)
   ```sh
   pip install spleeter
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

<!-- ROADMAP -->
## Roadmap

- [x] pre-alpha version
- [x] english translation
- [x] english translation GUI
- [x] CPU / GPU option
- [x] GPU tutorial
- [x] fit media size
- [x] CLI
- [x] Same file name
- [x] 3 Layer GUI
- [x] Easy install
- [x] preview srt
- [x] Alpha version
- [ ] Slice big file CLI
- [ ] Slice big file GUI
- [ ] Slice big file to multiple small file(5min + 1min), prevent too long proccess time and allow to create progress bar
- [ ] progress bar
- [ ] demo version / 5 min / CPU / model less then 3
- [ ] huggingface space
- [ ] streamlit gui version
- [ ] streamlit cloud
- [ ] English to other language translation
- [ ] Multi-language Support
    - [ ] Traditional Chinese
    - [ ] Japanese

<p align="right">(<a href="#top">back to top</a>)</p>

## Known bug
- [ ] Lots of work to do.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Q & A -->
<!--

## Q & A

1. Is it better then youtube automatic subtitles?
   ```
   Do you really need to ask? Youtube can even fuck up English transcribe.
   ```
   
2. Is it better then Vosk(Subtitle Edit)?
   ```
   Definitely.
   ```

3. Is it better then Trint?
   ```
   Trint is terrible at non-English transcribe, and that's whisper advantage.
   ```

3. Is it better then Sonix.ai?
   ```
   Sonix.ai is nearly perfect actually, but hey! you need to pay the bill!
   ```
4. Your code suck!
   ```
   Why dont you release a better version. So I can use your project and spend more time to relax.
   ```

<p align="right">(<a href="#top">back to top</a>)</p>
-->

<!-- CONTACT -->
## Contact

Greysuki  - tomchang25@gmail.com

Project Link: [https://github.com/tomchang25/whisper-auto-transcribe](https://github.com/tomchang25/whisper-auto-transcribe)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

The code and the model weights of Whisper are released under the MIT License. 
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [OpenAI-whisper](https://github.com/openai/whisper)
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


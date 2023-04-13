# From moviepy 2.0
import inspect
import os
import subprocess as sp

import decorator
import proglog
import imageio_ffmpeg

OS_NAME = os.name
FFMPEG_BINARY = os.getenv("FFMPEG_BINARY", imageio_ffmpeg.get_ffmpeg_exe())


def convert_to_seconds(time):
    """Will convert any time into seconds.
    If the type of `time` is not valid,
    it's returned as is.
    Here are the accepted formats:
    >>> convert_to_seconds(15.4)   # seconds
    15.4
    >>> convert_to_seconds((1, 21.5))   # (min,sec)
    81.5
    >>> convert_to_seconds((1, 1, 2))   # (hr, min, sec)
    3662
    >>> convert_to_seconds('01:01:33.045')
    3693.045
    >>> convert_to_seconds('01:01:33,5')    # coma works too
    3693.5
    >>> convert_to_seconds('1:33,5')    # only minutes and secs
    99.5
    >>> convert_to_seconds('33.5')      # only secs
    33.5
    """
    factors = (1, 60, 3600)

    if isinstance(time, str):
        time = [float(part.replace(",", ".")) for part in time.split(":")]

    if not isinstance(time, (tuple, list)):
        return time

    return sum(mult * part for mult, part in zip(factors, reversed(time)))


def preprocess_args(fun, varnames):
    """Applies fun to variables in varnames before launching the function."""

    def wrapper(func, *args, **kwargs):
        names = inspect.getfullargspec(func).args
        new_args = [
            fun(arg) if (name in varnames) and (arg is not None) else arg
            for (arg, name) in zip(args, names)
        ]
        new_kwargs = {
            kwarg: fun(value) if kwarg in varnames else value
            for (kwarg, value) in kwargs.items()
        }
        return func(*new_args, **new_kwargs)

    return decorator.decorator(wrapper)


def convert_parameter_to_seconds(varnames):
    """Converts the specified variables to seconds."""
    return preprocess_args(convert_to_seconds, varnames)


def convert_path_to_string(varnames):
    """Converts the specified variables to a path string."""
    return preprocess_args(os.fspath, varnames)


def cross_platform_popen_params(popen_params):
    """Wrap with this function a dictionary of ``subprocess.Popen`` kwargs and
    will be ready to work without unexpected behaviours in any platform.
    Currently, the implementation will add to them:
    - ``creationflags=0x08000000``: no extra unwanted window opens on Windows
      when the child process is created. Only added on Windows.
    """
    if OS_NAME == "nt":
        popen_params["creationflags"] = 0x08000000
    return popen_params


def subprocess_call(cmd, logger="bar"):
    """Executes the given subprocess command.
    Set logger to None or a custom Proglog logger to avoid printings.
    """
    logger = proglog.default_bar_logger(logger)
    logger(message="Moviepy - Running:\n>>> " + " ".join(cmd))

    popen_params = cross_platform_popen_params(
        {"stdout": sp.DEVNULL, "stderr": sp.PIPE, "stdin": sp.DEVNULL}
    )

    proc = sp.Popen(cmd, **popen_params)

    out, err = proc.communicate()  # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        logger(message="Moviepy - Command returned an error")
        raise IOError(err.decode("utf8"))
    else:
        logger(message="Moviepy - Command successful")

    del proc


@convert_path_to_string(("inputfile", "outputfile"))
@convert_parameter_to_seconds(("start_time", "end_time"))
def ffmpeg_extract_subclip(
    inputfile, start_time, end_time, outputfile=None, logger="bar"
):
    """Makes a new video file playing video file between two times.
    Parameters
    ----------
    inputfile : str
      Path to the file from which the subclip will be extracted.
    start_time : float
      Moment of the input clip that marks the start of the produced subclip.
    end_time : float
      Moment of the input clip that marks the end of the produced subclip.
    outputfile : str, optional
      Path to the output file. Defaults to
      ``<inputfile_name>SUB<start_time>_<end_time><ext>``.
    """
    if not outputfile:
        name, ext = os.path.splitext(inputfile)
        t1, t2 = [int(1000 * t) for t in [start_time, end_time]]
        outputfile = "%sSUB%d_%d%s" % (name, t1, t2, ext)

    # cmd = [
    #     FFMPEG_BINARY,
    #     "-y",
    #     "-ss",
    #     "%0.2f" % start_time,
    #     "-t",
    #     "%0.2f" % end_time,
    #     "-i",
    #     inputfile,
    #     "-map",
    #     "0",
    #     "-vcodec",
    #     "copy",
    #     "-acodec",
    #     "copy",
    #     "-copyts",
    #     outputfile,
    # ]
    cmd = [
        FFMPEG_BINARY,
        "-ss",
        "%0.2f" % start_time,
        "-t",
        "%0.2f" % (end_time - start_time),
        "-i",
        inputfile,
        "-c",
        "copy",
        "-y",
        outputfile,
    ]
    # print(cmd)
    subprocess_call(cmd, logger=logger)


@convert_path_to_string(("inputfile", "outputfile"))
def ffmpeg_extract_audio(inputfile, outputfile, bitrate=3000, fps=44100, logger="bar"):
    """Extract the sound from a video file and save it in ``outputfile``.
    Parameters
    ----------
    inputfile : str
      The path to the file from which the audio will be extracted.
    outputfile : str
      The path to the file to which the audio will be stored.
    bitrate : int, optional
      Bitrate for the new audio file.
    fps : int, optional
      Frame rate for the new audio file.
    """
    cmd = [
        FFMPEG_BINARY,
        "-y",
        "-i",
        inputfile,
        "-ab",
        "%dk" % bitrate,
        "-ar",
        "%d" % fps,
        outputfile,
    ]
    subprocess_call(cmd, logger=logger)

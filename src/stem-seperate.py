import subprocess


def demucs_seperate(inputfile, outputdir):
    cmd = rf"demucs --two-stems=vocals {inputfile} -o {outputdir} --filename {{stem}}.{{ext}}"

    try:
        subprocess.run(cmd, check=True)
    except:
        print("error: demucs failed")
        # subprocess.run(cmd, capture_output=True, check=True)

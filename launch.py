# this scripts installs necessary requirements and launches main program in webui.py
import importlib
import importlib.util
import os
import shlex
import subprocess
import sys

python = sys.executable
git = os.environ.get("GIT", "git")
torch_command = os.environ.get(
    "TORCH_COMMAND",
    "pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1+cu113 -f https://download.pytorch.org/whl/torch_stable.html",
)


requirements_file = os.environ.get("REQS_FILE", "requirements.txt")
commandline_args = os.environ.get("COMMANDLINE_ARGS", "")

args = shlex.split(commandline_args)


def extract_arg(args, name):
    return [x for x in args if x != name], name in args


args, skip_torch_cuda_test = extract_arg(args, "--skip-torch-cuda-test")


def run(command, desc=None, errdesc=None, cwd=None):
    if desc is not None:
        print(desc)

    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd
    )

    if result.returncode != 0:
        message = f"""{errdesc or 'Error running command'}.
Command: {command}
Error code: {result.returncode}
stdout: {result.stdout.decode(encoding="utf8", errors="ignore") if len(result.stdout)>0 else '<empty>'}
stderr: {result.stderr.decode(encoding="utf8", errors="ignore") if len(result.stderr)>0 else '<empty>'}
"""
        raise RuntimeError(message)

    return result.stdout.decode(encoding="utf8", errors="ignore")


def run_python(code, desc=None, errdesc=None):
    return run(f'"{python}" -c "{code}"', desc, errdesc)


def run_pip(args, desc=None):
    return run(
        f'"{python}" -m pip {args} --prefer-binary',
        desc=f"Installing {desc}",
        errdesc=f"Couldn't install {desc}",
    )


def check_run(command):
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    return result.returncode == 0


def check_run_python(code):
    return check_run(f'"{python}" -c "{code}"')


def is_installed(package):
    try:
        spec = importlib.util.find_spec(package)
    except ModuleNotFoundError:
        return False

    return spec is not None


# def is_installed(package, version=None):
#     try:
#         module = importlib.import_module(package)
#         if version is not None:
#             module_version = version.parse(module.__version__)
#             required_version = version.parse(version)
#             if module_version < required_version:
#                 return False
#     except ImportError:
#         return False

#     return True


try:
    commit = run(f"{git} rev-parse HEAD").strip()
except Exception:
    commit = "<none>"

print(f"Python {sys.version}")
print(f"Commit hash: {commit}")


if not is_installed("torch") or not is_installed("torchvision"):
    run(
        f'"{python}" -m {torch_command}',
        "Installing torch and torchvision",
        "Couldn't install torch",
    )
else:
    print("Check torch and torchvision")


# Only for pre-release
dir_repos = "repositories"
os.makedirs(dir_repos, exist_ok=True)


def repo_dir(name):
    return os.path.join(dir_repos, name)


custom_gradio_commit_hash = os.environ.get(
    "CUSTOM_GRADIO_COMMIT_HASH", "8ac54ca7902a04ede2cb93a11ff42c6cb011b296"
)

custom_gradio_templates_commit_hash = os.environ.get(
    "CUSTOM_GRADIO_TEMPLATES_COMMIT_HASH", "68df69b400ec2871bda9ce6a8dc93c3c30cfa0b5"
)


def git_clone(url, dir, name, commithash=None, branch=None):
    if os.path.exists(dir):
        if commithash is None:
            return

        current_hash = run(
            f"{git} -C {dir} rev-parse HEAD",
            None,
            f"Couldn't determine {name}'s hash: {commithash}",
        ).strip()
        if current_hash == commithash:
            return

        run(
            f"{git} -C {dir} fetch",
            f"Fetching updates for {name}...",
            f"Couldn't fetch {name}",
        )
        run(
            f"{git} -C {dir} checkout {commithash}",
            f"Checking out commint for {name} with hash: {commithash}...",
            f"Couldn't checkout commit {commithash} for {name}",
        )
        return

    if branch is not None:
        run(
            f'{git} clone -b {branch} --single-branch "{url}" "{dir}"',
            f"Cloning {name} into {dir}...",
            f"Couldn't clone {name}",
        )
    else:
        run(
            f'{git} clone "{url}" "{dir}"',
            f"Cloning {name} into {dir}...",
            f"Couldn't clone {name}",
        )

    if commithash is not None:
        run(
            f"{git} -C {dir} checkout {commithash}",
            None,
            "Couldn't checkout {name}'s hash: {commithash}",
        )


if not is_installed("gradio"):
    git_clone(
        "https://github.com/tomchang25/gradio.git",
        repo_dir("gradio"),
        "Custom Gradio",
        custom_gradio_commit_hash,
    )

    run_pip(f"install {dir_repos}/gradio", "gradio")

    git_clone(
        "https://github.com/tomchang25/gradio-templates.git",
        repo_dir("gradio-templates"),
        "Custom Gradio templates",
        custom_gradio_templates_commit_hash,
    )

    run(
        rf"xcopy {dir_repos}\gradio-templates\templates venv\Lib\site-packages\gradio\templates\ /e/y/i",
        "Building gardio front",
        "Couldn't build gardio front",
    )


else:
    print("Check gradio")


run_pip(f"install -r {requirements_file}", "requirements for Web UI")


sys.argv += args

if "--exit" in args:
    print("Exiting because of --exit argument")
    exit(0)


def start_webui():
    print(f"Launching Web UI with arguments: {' '.join(sys.argv[1:])}")
    from gui import gui

    gui().launch()


if __name__ == "__main__":
    start_webui()

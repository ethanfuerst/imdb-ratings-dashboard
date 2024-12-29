import shlex
import subprocess
from pathlib import Path

import modal

app = modal.App("imdb-ratings-dashboard")
current_dir = Path(__file__).parent

required_files = {
    "app.py": "/root/app.py",
    "ratings.csv": "/root/ratings.csv",
    "imdb_data.py": "/root/imdb_data.py"
}

for local_file in required_files:
    if not (current_dir / local_file).exists():
        raise RuntimeError(
            f"{local_file} not found! Place the file in the same directory."
        )

image = (
    modal.Image.debian_slim(python_version="3.9")
    .pip_install(
        "dash-bootstrap-components==1.6.0",
        "plotly==5.24.1",
        "dash==2.18.2",
        "pandas==2.2.3",
    )
)

for local_file, remote_path in required_files.items():
    image = image.add_local_file(
        current_dir / local_file,
        remote_path
    )

@app.function(
    image=image,
    allow_concurrent_inputs=100,
)
@modal.web_server(8050)
def serve():
    target = shlex.quote("/root/app.py")
    cmd = f"python3 {target} --server.port 8050 --server.enableCORS=false --server.enableXsrfProtection=false"
    subprocess.Popen(cmd, shell=True)

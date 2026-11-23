# World of Games

A Python console game collection with a Flask score service and Selenium end-to-end browser test.

## Components and responsibilities

| File | Responsibility |
| --- | --- |
| `MainGame.py` | Console entry point; welcomes the player and launches the menu. |
| `Live.py` | Presents games and difficulty selection, runs the chosen game, and awards points only for wins. |
| `GuessGame.py` | Number guessing game. |
| `MemoryGame.py` | Sequence memory game. |
| `CurrencyRouletteGame.py` | USD-to-ILS guessing game using a live exchange-rate API. |
| `Score.py` | Reads and updates the single cumulative score, using the shared score path. |
| `Utils.py` | Defines `SCORES_FILE_NAME`, `BAD_RETURN_CODE`, and screen clearing. |
| `MainScores.py` | Flask HTTP service; reads the score for each request and renders `id="score"`. |
| `tests/e2e.py` | Selenium test of the score page; exits 0 on success and nonzero on failure. |
| `Dockerfile` | Builds the score-service image and copies an initial `/Scores.txt`. |
| `docker-compose.yml` | Builds, names, and exposes the score-service container. |
| `docker-run-command.txt` | Documents direct Docker startup. |
| `Scores.txt` | Local cumulative score and initial image seed. |

## Dependencies

- Python 3.12 or compatible Python 3.
- `requests` for exchange rates.
- `Flask` for the HTTP score service.
- `selenium` for the browser end-to-end test.
- Google Chrome and a compatible ChromeDriver (Selenium Manager can normally arrange the driver).
- Docker and Docker Compose for container execution.

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Score configuration and storage

`Utils.py` is the **single source of truth** for `SCORES_FILE_NAME`. `Score.py` imports that setting, and `MainScores.py` reads through `Score.py`, so the service and game use the same configured path *within the same environment*. Neither should choose a path based on the current working directory.

The current cross-platform configuration is:

```python
import os

if os.name == "nt":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SCORES_FILE_NAME = os.path.join(BASE_DIR, "Scores.txt")
else:
    SCORES_FILE_NAME = "/Scores.txt"

BAD_RETURN_CODE = -1
```

- **Windows console game:** `<project-directory>\\Scores.txt` (absolute path resolved from `Utils.py`).
- **Linux Docker score service:** `/Scores.txt` inside the container. The Dockerfile initially copies the project-root `Scores.txt` to this path.
- **Isolated browser test:** `tests/fixtures/Scores.txt` on the host, bind-mounted **read-only** at `/Scores.txt` in a *separate* test container. The browser reads the service output; it does not read the fixture directly.

These are distinct files unless you explicitly configure a shared mount. The normal Windows console score is **not automatically shared** with Docker. The image's initial `/Scores.txt` is not persistent across container recreation. The test fixture is intentionally separate to avoid altering real game scores.

The initial `Scores.txt` can contain `0`. The browser test deliberately rejects `0`; its fixture must contain a whole number from 1 to 1000 (the example fixture contains `10`). Invalid score files must cause the service to return HTTP 500 with a red error in `id="score"`, not a fabricated numeric score.

## Console startup

From the project directory:

```bash
python MainGame.py
```

On Windows, successful wins update the project-local `Scores.txt`.

## Flask service startup without Docker

```bash
python MainScores.py
```

The service must listen on `0.0.0.0:8777` with Flask debug mode disabled. Visit <http://localhost:8777>. On Windows it reads the project-local `Scores.txt`.

## Docker Compose startup

Replace `YOUR_DOCKERHUB_USERNAME` in `docker-compose.yml` with your actual Docker Hub username. The full image name is `YOUR_DOCKERHUB_USERNAME/world-of-games-scores:latest` until replaced.

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Visit <http://localhost:8777>. Stop with:

```bash
docker compose down
```

The Compose mapping is **host port 8777 → container port 8777**. The Dockerfile starts `MainScores.py` using `CMD` and includes `/Scores.txt`. No debug mode is enabled.

For direct container startup, see `docker-run-command.txt`. A typical command (when no Compose container is using the name or port) is:

```bash
docker run -d --name world-of-games-scores -p 8777:8777 YOUR_DOCKERHUB_USERNAME/world-of-games-scores:latest
```

## Isolated Selenium browser test

The test function `test_scores_service(application_url)` opens Chrome, waits for a visible `id="score"` element, reads its text, and succeeds only for an integer between **1 and 1000**, inclusive. Navigation errors, missing elements, and invalid data fail. The browser is closed even after errors. `main_function()` exits with code `0` on success and `-1` on failure (often displayed as `255`); treat **any nonzero exit code** as failure.

The repository includes `tests/fixtures/Scores.txt` with the value `10` for the isolated test. To avoid interfering with a running Compose service, stop it first:

```bash
docker compose down
```

Build the image, then start an **ephemeral test container** with the fixture mounted over the image's `/Scores.txt`:

**PowerShell (Windows):**

```powershell
docker compose build
docker run --rm -d --name world-of-games-scores-e2e -p 8777:8777 --mount "type=bind,source=$((Resolve-Path './tests/fixtures/Scores.txt').Path),target=/Scores.txt,readonly" YOUR_DOCKERHUB_USERNAME/world-of-games-scores:latest
python tests/e2e.py http://localhost:8777
$LASTEXITCODE
docker stop world-of-games-scores-e2e
```

**Bash (Linux/macOS):**

```bash
docker compose build
docker run --rm -d --name world-of-games-scores-e2e -p 8777:8777 --mount "type=bind,source=$(pwd)/tests/fixtures/Scores.txt,target=/Scores.txt,readonly" YOUR_DOCKERHUB_USERNAME/world-of-games-scores:latest
python tests/e2e.py http://localhost:8777
status=$?
docker stop world-of-games-scores-e2e
exit "$status"
```

Use the actual Docker Hub username in these commands. Ensure Chrome is installed on the machine running Selenium. The test may fail if the service has not yet started; inspect `docker logs world-of-games-scores-e2e` and rerun when it is ready. If using a browser on a remote machine, provide that machine's reachable service URL instead of `localhost`.

> Note: A read-only bind mount is suitable for the isolated **read-only browser test**. Do not play the console game or attempt score updates inside this test container: writes to `/Scores.txt` will fail. For a persistent writable service, configure an appropriate writable volume separately.


from flask import Flask
from Score import _read_score
from Utils import BAD_RETURN_CODE

app = Flask(__name__)


@app.route("/", methods=["GET"])
def score_server():

    score = _read_score()

    if score == BAD_RETURN_CODE:
        return """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Scores Game</title>
          </head>
          <body>
            <h1>
              The score is
              <span id="score" style="color: red;">
                Error: Unable to retrieve the score.
              </span>
            </h1>
          </body>
        </html>
        """, 500

    return f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Scores Game</title>
      </head>
      <body>
        <h1>
          The score is <span id="score">{score}</span>
        </h1>
      </body>
    </html>
    """, 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8777, debug=False)
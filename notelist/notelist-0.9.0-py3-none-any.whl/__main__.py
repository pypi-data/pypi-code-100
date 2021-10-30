"""Notelist script.

This script runs the Notelist application on a local development server.
"""

from notelist import app


if __name__ == "__main__":
    app.run(host="localhost", port=5000)

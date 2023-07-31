  cd your_work_dir
  git clone git@github.com:JackScher/langchain.git
  cd langchain
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  create .env file and add values to it
  docker build . -t langchain_app:latest
  docker run -d -p 7329:8000 langchain_app

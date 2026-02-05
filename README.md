## Dataset
Kaggle Quotes 500k
https://www.kaggle.com/datasets/manann/quotes-500k?resource=download

## Build
docker build -t trixing/qotd .

## Run
docker run --name trixing_qotd --restart=always --detach trixing/qotd

## Debug
docker run -it -v $PWD:/usr/src/app  trixing/qotd

## Develop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
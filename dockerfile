FROM python:3.10-slim
WORKDIR /app
COPY .gitignore Apple-stock.py requirements.txt /app/
COPY pages/1_📈_Tips.py /app/pages
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "streamlit", "run", "Apple-stock.py" ]
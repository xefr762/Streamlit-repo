FROM python:3.10-slim

WORKDIR /app
COPY .gitignore Apple-stock.py requirements.txt /app/
COPY pages/tips.py /app/pages
RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Apple-stock.py"]
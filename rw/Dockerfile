FROM python:3.12.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN git config --global user.email "francisduvivier+agent@gmail.com"
RUN git config --global user.name "Agentic Francis Duvivier"
CMD ["python", "agent.py"]
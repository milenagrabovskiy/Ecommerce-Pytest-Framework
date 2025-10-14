FROM python:3.11

# EST timezone
RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
RUN echo "America/New_York" > /etc/timezone

# Create working directory inside container
RUN mkdir /demostore
WORKDIR /demostore

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Copy the entire project
COPY . .

# Set PYTHONPATH to the project root so Python can find demostore_automation
ENV PYTHONPATH=/demostore

# Run pytest from project root
WORKDIR /demostore
ENTRYPOINT ["python3", "-m", "pytest", "demostore_automation/tests/backend"]


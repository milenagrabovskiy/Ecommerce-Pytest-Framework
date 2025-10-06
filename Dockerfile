FROM python:3.11

# EST timezone
RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
RUN echo "America/New_York" > /etc/timezone

RUN mkdir /automation

# Option 1
#COPY requirements.txt /automation
#RUN python3 -m pip install -r /automation/requirements.txt

# Option 2
WORKDIR /automation
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

WORKDIR /automation/demostore_automation
ENTRYPOINT ["python3", "-m", "pytest", "tests", "tests/backend"]

#CMD []
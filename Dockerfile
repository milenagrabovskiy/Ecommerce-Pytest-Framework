FROM python:3.11

RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
RUN echo "America/Los_Angeles" > /etc/timezone

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
ENTRYPOINT ["python3", "-m", "pytest", "tests"]

#CMD []
#pip install pipreqs
#pipreqs requirements.txt
FROM python:3.10.2-slim-buster

RUN mkdir /config  && apt-get update && apt-get -y install ffmpeg gcc apt-transport-https ca-certificates libnss3 xvfb gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils  && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN pip3 --no-cache-dir install --user -r /app/requirements.txt

WORKDIR /app
# -u print打印出来
CMD ["python3", "-u", "pornbot.py"]

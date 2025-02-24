FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip nmap git

RUN git clone https://github.com/scipag/vulscan

RUN mv vulscan /usr/share/nmap/scripts

COPY resource/update_cve.csv /usr/share/nmap/scripts

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8080
EXPOSE 51000

#CMD ["python3", "djnagoPRC/djangoRPC/manage.py", "runserver", "0.0.0.0:8080"]
RUN chmod +x ./start.sh

CMD ["sh", "./start.sh"]


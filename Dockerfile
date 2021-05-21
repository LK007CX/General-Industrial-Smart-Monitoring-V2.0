FROM gism-dev-jp441:v2.0.6
WORKDIR /root/app
COPY . /root/app

RUN locale-gen zh_CN.UTF-8 &&\
  DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8 
ENV LANGUAGE zh_CN:zh 
ENV LC_ALL zh_CN.UTF-8
COPY font/msyh.ttc /usr/share/fonts/msyh.ttc

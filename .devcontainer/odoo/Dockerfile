## See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.163.0/containers/python-3/.devcontainer/base.Dockerfile
## Available image variants: https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Optional] Allow the vscode user to pip install globally w/o sudo
RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade pip
ENV PIP_TARGET=/usr/local/pip-global
#ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PYTHONPATH=${PIP_TARGET}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN if ! cat /etc/group | grep -e "^pip-global:" > /dev/null 2>&1; then groupadd -r pip-global; fi \
    && usermod -a -G pip-global vscode \
    && umask 0002 && mkdir -p ${PIP_TARGET} \
    && chown :pip-global ${PIP_TARGET} \
    && ( [ ! -f "/etc/profile.d/00-restore-env.sh" ] || sed -i -e "s/export PATH=/export PATH=\/usr\/local\/pip-global:/" /etc/profile.d/00-restore-env.sh )

# [Option] Install Node.js
# ARG INSTALL_NODE="true"
# ARG NODE_VERSION="lts/*"
# RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# Create directory and set permission
RUN mkdir /opt/odoo && chown -R vscode:vscode /opt/odoo
RUN mkdir /opt/odoo/repos && chown -R vscode:vscode /opt/odoo/repos

WORKDIR /opt/odoo/repos

# Install Odoo
ENV PYTHONPATH=/opt/odoo/repos/odoo:${PYTHONPATH}
USER vscode
ARG ODOO_VERSION="master"
RUN git clone --branch=${ODOO_VERSION} --depth=1 https://github.com/odoo/odoo.git odoo
USER root

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
# https://github.com/odoo/docker/blob/master/14.0/Dockerfile
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        build-essential fonts-noto-cjk libldap2-dev libsasl2-dev \
        postgresql-client \
        python3-dev python3-lxml python3-num2words python3-pdfminer python3-phonenumbers python3-pip \
        python3-pyldap python3-qrcode python3-renderpm python3-setuptools python3-slugify \
        python3-vobject python3-watchdog python3-xlrd python3-xlwt

# Update specific package versions in the requirements file to avoid build errors
ARG AVOID_BUILD_ERRORS="true"
RUN if [ "${AVOID_BUILD_ERRORS}" = "true" ]; then \
    cp odoo/requirements.txt odoo/requirements.txt.org \
    && sed -i -e "s/gevent==21.8.0/gevent==22.10.2/g" \
              -e "s/greenlet==1.1.2/greenlet==2.0.2/g" \
              odoo/requirements.txt; \
    fi

# Install dependencies
RUN pip3 --disable-pip-version-check --no-cache-dir install -r odoo/requirements.txt

# Install wkhtmltopdf
# See also: https://www.odoo.com/documentation/master/administration/install/install.html#dependencies
# > Important
# > wkhtmltopdf is not installed through pip and must be installed manually in version 0.12.5 for it to support headers and footers.
# > See our wiki for more details on the various versions. 
# > [version 0.12.5] https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.5
# > [our wiki] https://github.com/odoo/odoo/wiki/Wkhtmltopdf
RUN curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
    && echo 'ea8277df4297afc507c61122f3c349af142f31e5 wkhtmltox.deb' | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Right-to-left interface support
# See also: https://www.odoo.com/documentation/master/administration/install/install.html#dependencies
ARG SUPPORT_RTLCSS="true"
RUN if [ "${SUPPORT_RTLCSS}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install lts/* && npm install -g rtlcss 2>&1"; fi

# Install pylint odoo plugin https://github.com/OCA/pylint-odoo
# See also: https://odoo-development.readthedocs.io/en/latest/ide/emacs/pylint.html
# RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade git+https://github.com/oca/pylint-odoo.git
RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade --pre pylint-odoo

# Install bobtemplates.odoo.
# See also: https://github.com/acsone/bobtemplates.odoo
RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade bobtemplates.odoo

# Create directories and set permissions
RUN mkdir /opt/odoo/.vscode /opt/odoo/custom_addons /opt/odoo/data /opt/odoo/scripts /opt/odoo/templates \
    && chown vscode:vscode /opt/odoo/.vscode /opt/odoo/custom_addons /opt/odoo/data /opt/odoo/scripts /opt/odoo/templates
RUN mkdir /etc/odoo
RUN mkdir /home/vscode/.vscode-server \
    && chown vscode:vscode /home/vscode/.vscode-server
ENV CUSTOM_ADDONS=/opt/odoo/custom_addons

# odoo server configuration environment files
ENV ODOO_RC=/etc/odoo/odoo.conf
ENV PATH=/opt/odoo/scripts:${PATH}

# Expose Odoo services
EXPOSE 8069 8071 8072

ENTRYPOINT ["/opt/odoo/entrypoint.sh"]
CMD ["odoo"]

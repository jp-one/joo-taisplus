# See here for image contents: https://github.com/devcontainers/images/tree/main/src/python
# Available image variants: https://github.com/devcontainers/templates/blob/main/src/python/devcontainer-template.json
ARG VARIANT="3"
FROM mcr.microsoft.com/devcontainers/python:1-${VARIANT}-bookworm
ARG PYTHONPATH=""

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

# Install dev requirements
COPY ./odoo/requirements_dev.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade -r /tmp/pip-tmp/requirements_dev.txt \
   && rm -rf /tmp/pip-tmp

# Create directory and set permission
RUN mkdir /opt/odoo && chown -R vscode:vscode /opt/odoo
RUN mkdir /opt/odoo/repos && chown -R vscode:vscode /opt/odoo/repos

WORKDIR /opt/odoo/repos

# Install Odoo
ENV PYTHONPATH=/opt/odoo/repos/odoo${PYTHONPATH:+:$(PYTHONPATH)}
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
ARG AVOID_BUILD_ERRORS="false"
RUN if [ "${AVOID_BUILD_ERRORS}" = "true" ]; then \
    cp odoo/requirements.txt odoo/requirements.txt.org \
    && sed -i -e "s/gevent==21.8.0/gevent==22.10.2/g" \
              -e "s/greenlet==1.1.2/greenlet==2.0.2/g" \
              odoo/requirements.txt; \
    fi

# Install dependencies
RUN pip3 --disable-pip-version-check --no-cache-dir install --upgrade -r odoo/requirements.txt

# Install wkhtmltopdf, bookworm_amd64 version
# https://www.odoo.com/documentation/master/administration/on_premise/source.html#dependencies
# > Warning
# > wkhtmltopdf is not installed through pip and must be installed manually in version 0.12.6 for it to support headers and footers.
# > Check out the wkhtmltopdf wiki for more details on the various versions.
# > [version 0.12.6] https://github.com/wkhtmltopdf/packaging/releases/tag/0.12.6.1-3
# > [the wkhtmltopdf wiki] https://github.com/odoo/odoo/wiki/Wkhtmltopdf
RUN curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && echo 'e9f95436298c77cc9406bd4bbd242f4771d0a4b2 wkhtmltox.deb' | sha1sum -c - \
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
ENV CUSTOM_ADDONS=/opt/odoo/custom_addons

# odoo server configuration environment files
ENV ODOO_RC=/etc/odoo/odoo.conf
ENV PATH=/opt/odoo/scripts:${PATH}

# Expose Odoo services
EXPOSE 8069 8071 8072

USER vscode
ENTRYPOINT ["/opt/odoo/entrypoint.sh"]
CMD ["odoo"]

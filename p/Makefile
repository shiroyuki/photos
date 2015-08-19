PYI=python
SERVICE_FLAG=
SCSS_PATH=static/scss
CSS_PATH=static/css

default:
	@echo 'Read the Makefile for options.'

# For Debian
prep_d: prep
	@apt-get install -y mongodb-dev
	@pip install --upgrade --force-reinstall pymongo

# For Ubuntu
prep_u: prep
	@apt-get install -y libmongo-client-dev
	@pip install --upgrade --force-reinstall pymongo

prep:
	@apt-get install -y python-dev python-pip python-pillow
	@apt-get install -y libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
	@pip install --upgrade --force-reinstall tori imagination kotoba tornado flask jinja2 pillow

	# SQLAlchemy and SQLite 3
	@apt-get install -y libsqlite3-0 libsqlite3-dev
	@pip install --upgrade --force-reinstall sqlalchemy

	# Ruby and SCSS
	@apt-get install -y rubygems
	@gem install sass

	# Node.js and Bower
	@apt-get install -y npm
	@npm install -g bower

	# MongoDB Server
	@apt-get install -y mongodb-clients mongodb-server

service: css
	@$(PYI) server.py $(SERVICE_FLAG)

css:
	@sass --update $(SCSS_PATH):$(CSS_PATH) --style compressed

css_live:
	@sass --watch $(SCSS_PATH):$(CSS_PATH) --style compressed

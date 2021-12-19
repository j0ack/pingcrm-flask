# Ping CRM

A demo application to illustrate how Inertia.js works with [Flask](http://flask.pocoo.org/)
and [Vue 3](https://v3.vuejs.org/).

![](https://raw.githubusercontent.com/inertiajs/pingcrm/master/screenshot.png)

> This is a port of the original [Ping CRM](https://github.com/inertiajs/pingcrm)
> written in Laravel and Vue.

# Installation

Clone the repo locally:

```
git clone https://github.com/j0ack/pingcrm-flask.git
cd pingcrm-flask
```

Install dependencies:

```
python3 -m venv venv
source ./venv/bin/activate
make init
```

Run database seeder:

```
make seed
```

Run dev server:

```
make dev
```

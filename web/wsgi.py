#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ziwu.app import create_app

application = create_app()

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=int(app.config['PORT']),
            debug=app.config['DEBUG'])

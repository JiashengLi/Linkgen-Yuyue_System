#!/usr/bin/env python
# -*- coding:utf-8 -*-

import qrcode
img = qrcode.make('simpleqrcode')
img.save('qrcode.jpg')

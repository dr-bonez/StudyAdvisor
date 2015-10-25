#!/bin/bash

mysql -u root -ppassword --execute="use study; $1"

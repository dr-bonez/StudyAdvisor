#!/bin/bash

mysql -u root -p password --execute="use study; $1"

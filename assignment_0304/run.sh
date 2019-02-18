#!/bin/bash

(cd server && ./run.sh) &
(cd client && ./run.sh)
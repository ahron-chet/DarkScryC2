#!/bin/sh

if [ "$DARKSCRY_DEBUG" = "true" ] || [ "$DARKSCRY_DEBUG" = "True" ]; then
  npm run dev
else
  npm run start
fi

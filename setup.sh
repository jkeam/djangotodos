#!/bin/bash

echo "DB Client URL:"
echo "  https://$(oc get $(oc get routes -o name | grep adminer) -o jsonpath={.spec.host})"
web="$(oc get $(oc get routes -o name | grep django) -o jsonpath={.spec.host})"
sed "s/*/$web/g" .env.template > .env

#!/bin/sh
git pull
cd ../
# This should be a API call to duggout service
RAILS_ENV=production rake duggout:clear_oc_cache
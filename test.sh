#!/usr/bin/env bash

clean_up() {
    set +e
    echo "Cleaning testing environment..."
    #docker-compose down -v
}
trap clean_up EXIT

# Export variables define in .env file
#export $(grep -v '^#' default.env | xargs)

# Start services
#docker-compose up -d

PYTHONPATH=$PWD:$PWD/tests/test_lib/sources/
export PYTHONPATH


# Wait for services up
#sleep 3

# Run tests and  export coverage
pytest --cov ./ --cov-report xml:coverage.xml --cov-report term --cov-config=.coveragerc --cov-branch -ra $@

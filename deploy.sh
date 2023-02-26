function main() {
    if test ! -e .env; then
        echo "[ERROR] .env file not found."
        return
    fi

    echo "your gcp project id:"
    read project_id

    if [ "$project_id" = "" ]; then
        echo "[ERROR] invalid project id."
        return
    fi

    echo "[INFO] creating requirements.txt"
    pipenv run pip freeze >requirements.txt

    echo "[INFO] deploy to functions"
    gcloud functions deploy mfgpt \
        --runtime=python310 \
        --region=asia-southeast1 \
        --source=. \
        --entry-point=hello_http \
        --trigger-http \
        --project=$project_id \
        --memory=256MB \
        --timeout=60 \
        --max-instances=1 \
        --gen2
}

main

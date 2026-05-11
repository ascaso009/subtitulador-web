#!/bin/bash
export ARGOS_PACKAGES_DIR=/models/translation
export ARGOS_INDEX_DIR=/models/translation

if [ $# -gt 0 ]; then
    exec python3 app/subtools.py "$@"
else
    exec streamlit run app/webui.py --server.port=8501 --server.address=0.0.0.0
fi

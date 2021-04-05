#!/bin/bash
cd "$TLUSTY"/io_folder/
for FOLDER in */ ; do
    if [[ -d "$FOLDER" && "$FOLDER" != "data/" ]]; then
        while IFS=$'\r\n' read -r line; do
            read -r -a arr <<< $line
            prog=${arr[0]}
            if [[ "${#arr[@]}" == 2 ]]; then
                "$TLUSTY"/RTlusty "$TLUSTY"/io_folder/"$FOLDER${arr[1]}"
            fi
            if [[ "${#arr[@]}" == 3 ]]; then
                "$TLUSTY"/RTlusty "$TLUSTY"/io_folder/"$FOLDER${arr[1]}" "$TLUSTY"/io_folder/"$FOLDER${arr[2]}"
            fi
            if [[ "${#arr[@]}" == 4 ]]; then
                "$TLUSTY"/RSynspec "$TLUSTY"/io_folder/"$FOLDER${arr[1]}" "$TLUSTY"/io_folder/"$FOLDER${arr[2]}" "$TLUSTY"/io_folder/"$FOLDER${arr[3]}"
            fi
        done < $FOLDER/run.list
        python3.8 "$TLUSTY"/plot_spec.py "$FOLDER"
    fi
done
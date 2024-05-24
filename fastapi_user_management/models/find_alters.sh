#!/bin/bash

# Define the directory where Python files are located
MIGRATION_DIR="/home/mehdi/Projects/cs7/fastapi_user_management/models"

# Check if the directory exists
if [ ! -d "$MIGRATION_DIR" ]; then
    echo "Directory $MIGRATION_DIR does not exist."
    exit 1
fi

# Initialize a variable to store all schema-related changes
ALL_COLUMNS=""

# Loop through each Python file in the directory
for FILE in "$MIGRATION_DIR"/*.py; do
    # Check if the file is a regular file
    if [ -f "$FILE" ]; then
        # Check if there are uncommitted changes
        if ! git diff --quiet "$FILE" ; then
            echo "Uncommitted changes found in $FILE"
            # Extract the model column changes from the diff
            COLUMNS=$(git diff --no-color "$FILE"  | grep -iE '^[+-].*mapped_column.*$')
            if [ -n "$COLUMNS" ]; then
                echo "Schema-related changes found in $FILE"
                ALL_COLUMNS+="$COLUMNS"
            else
                echo "No schema-related changes found in uncommitted changes."
            fi
        else
            echo "No uncommitted changes found in $FILE"
        fi
    fi
done

# Echo the final schema-related changes
echo "$ALL_COLUMNS"

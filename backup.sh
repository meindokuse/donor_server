#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

source .env

pg_dump -h db -U $DB_USER $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_FILE"
else
    echo "Backup failed" >&2
    exit 1
fi

# Удаление старых бэкапов (оставляем только последние 7)
find $BACKUP_DIR -type f -mtime +7 -name "*.sql" -exec rm {} \;

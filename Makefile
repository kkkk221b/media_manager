# Установите папку для очистки и максимальный возраст файлов (в секундах)
CLEAN_FOLDER := local_disk/files
MAX_FILE_AGE := 604800  # 7 дней в секундах

.PHONY: help clean_old_files setup_cron

# Основная цель makefile — выводить справочную информацию
help:
	@echo "Используйте 'make <command>' для выполнения команд:"
	@echo "  clean_old_files - Удалить файлы старше заданного возраста из ${CLEAN_FOLDER}"
	@echo "  setup_cron      - Настроить крон-задачу для регулярной очистки старых файлов"

# Задача для очистки старых файлов
clean_old_files:
	@echo "Очистка файлов старше $(MAX_FILE_AGE) секунд из папки $(CLEAN_FOLDER)"
	@find $(CLEAN_FOLDER) -type f -mtime +$(shell echo $(MAX_FILE_AGE)/86400 | bc) -exec rm -f {} \;
	@echo "Очистка завершена."

# Задача для настройки крон-задачи
setup_cron:
	@echo "Добавление крон-задачи для очистки старых файлов..."
	@{ crontab -l 2>/dev/null; echo "0 3 * * * cd $(shell pwd) && make clean_old_files"; } | crontab -
	@echo "Крон-задача настроена."

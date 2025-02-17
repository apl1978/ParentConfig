# Parent Configurations

Скрипт для анализа конфигураций поставщиков и правил поддержки объектов решений на
платформе [1С:Предприятие 8](https://v8.1c.ru/platforma/)

Скрипт читает файл ParentConfigurations.bin, собирает данные о найденных конфигурациях поставщиков
в словарь dict_configs. Для каждой конфигурации поставщика записывается ее идентификатор,
название, поставщик и версия. В зависимости от установленного правила, объекты конфигурации поставщика
разносятся по трем спискам:

- locked_list - объекты не редактируются
- editable_list - объекты редактируются с сохранением поддержки
- removed_list - снятые с поддержки объекты

Из файла ConfigDumpInfo.xml по guid подбирается имя объекта.

Далее, в готовом словаре можно посмотреть объекты конфигурации поставщика с нужным правилом поддержки.

Идея написания скрипта возникла при очередном обновлении переписанной конфигурации 1С ERP Управление Холдингом,
в которой много объектов снято с поддержки. Такие объекты надо найти, проанализировать, и, по возможности, вернуть на
поддержку для последующего обновления. В окне настройки поддержки никаких фильтров нет, приходится проверять каждый
объект вручную.

Для работы скрипта, надо выгрузить конфигурацию в файлы средствами конфигуратора.
Файлы ParentConfigurations.bin и ConfigDumpInfo.xml скопировать в папку со скриптом.

Версия Python - 3.11. Проект не использует сторонние бибилиотеки.

Регулярное выражение для разбора файла ParentConfigurations.bin и алгоритм чтения
взят [здесь](https://github.com/1c-syntax/supportconf/tree/develop), спасибо автору.
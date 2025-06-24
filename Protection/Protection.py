


# Защита проектной работы (автотестирование Таблиц данных платформы Knowledge space)

@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Отображение объектов в качестве строк')
@testit.displayName('Отображение объектов в качестве строк')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Отображение объектов в качестве строк',
    'login_type': 'admin'
})])
def test_check_displaying_object_as_string(login_driver, parameters):
    table_page = TablePage(login_driver)

    model_name = "autotest_new_model"
    table_name = 'autotest_dos_table'
    expected_value = 'auto_obj01'
    expected_value_2 = 'auto_obj02'

    with testit.step(f'Создать таблицу в модели "{model_name}"'):
        table_page.tree.select_node_object(model_name, "auto-test-table")
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Построить таблицу в новом конструкторе'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=[expected_value])

        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset01")
        time.sleep(2)

    with testit.step('Перейти на вкладку "Таблица" и проверить отображение объектов в строках'):
        table_page.open_tab('Таблица')
        value = table_page.get_header_cell_value(2)

        assert value == expected_value, "Корректность отображения объекта!"

    with testit.step('Перейти на вкладку конструктор'):
        table_page.open_tab('Конструктор')

    with testit.step('Изменение структуры объектов "По классу"'):
        table_page.set_object(obj_names=[expected_value_2])

    with testit.step('Проверить что объекты добавились в таблицу'):
        table_page.open_tab('Таблица')
        assert table_page.get_header_cell_value(2) == expected_value_2, "Некорректное отображение объекта!"

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)



@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Отображение объектов по цепочке связей')
@testit.displayName('Отображение объектов по цепочке связей')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Отображение объектов по цепочке связей',
    'login_type': 'admin'
})])
def test_check_displaying_object_links(login_driver, parameters):
    table_page = TablePage(login_driver)

    model_name = "autotest_new_model"
    table_name = 'autotest_links_table'
    expected_table_titles = ''

    with testit.step(f'Создать таблицу в модели "{model_name}"'):
        table_page.tree.select_node_object(model_name, "auto-test-table")
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Построение структуры таблицы для объектов "По классу"'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["autotest_class4"], object_type='По классу')
        time.sleep(2)
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset01")
        table_page.select_entity('Объекты')

    with testit.step('Включение свитчера "Настройка цепочки объектов"'):
        table_page.switch_toggle(switcher_name="Настройка цепочки объектов", turn_on=True)

    with testit.step('Выбор связи для класса "autotest_class"'):
        table_page.set_object(obj_names=['1', 'autotest_class'], object_type='По связи')

    with testit.step('Включение свитчера "Отображать полную цепочку объектов"'):
        table_page.switch_toggle(switcher_name="Отображать полную цепочку объектов", turn_on=True)
        table_page.refresh_page()

    with testit.step('Перейти на вкладку "Таблица" и проверить отображение объектов по цепочке связей'):
        table_page.open_tab('Таблица')
        time.sleep(3)

        assert table_page.get_table_rows_titles() == expected_table_titles, \
            "Ошибка! Ожидаемый результат не совпадает с фактическим"

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Отображение объектов по цепочке связей "По классу"(обратная)')
@testit.displayName('Отображение объектов по цепочке связей "По классу"(обратная)')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Отображение объектов по цепочке связей(обратная)',
    'login_type': 'admin'
})])
def test_relation_object(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'relation_table'
    model_name = 'autotest_new_constructor'
    expected_value = ['dataset_2', 'obj_1', '1:obj_1_obj_3', 'obj_3', '1:obj_1_obj_3', 'obj_1', '1:obj_2_obj_3',
                      'obj_2',
                      'obj_2', '1:obj_2_obj_3', 'obj_3', '1:obj_1_obj_3', 'obj_1', '1:obj_2_obj_3', 'obj_2']

    with testit.step(f'Создать таблицу"{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Добавление сущностей в структуру таблицы '):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["autotest_class"], object_type='По классу')
        time.sleep(3)
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset_2")

    with testit.step('Переход в конструкторе к "Объектам"'):
        table_page.select_entity('Объекты')

    with testit.step('Включение свитчера "Настройка цепочки объектов"'):
        table_page.switch_toggle(switcher_name="Настройка цепочки объектов", turn_on=True)

    with testit.step('Выбор связи для класса "autotest_class"'):
        table_page.set_object(obj_names=['1', 'autotest_class2', '1', 'autotest_class'], object_type='По связи')

    with testit.step('Включение свитчера "Отображать полную цепочку объектов"'):
        table_page.switch_toggle(switcher_name="Отображать полную цепочку объектов", turn_on=True)

    with testit.step('Переход на таблицу и проверка отображения таблицы'):
        table_page.open_tab('Таблица')
        assert expected_value == table_page.get_table_data_list_with_headers(15, 1, only_header=True)

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)



@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Отображения всех наборов данных в качестве столбцов таблицы')
@testit.displayName('Отображения всех наборов данных в качестве столбцов таблицы')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Отображения всех наборов данных в качестве столбцов таблицы',
    'login_type': 'admin'
})])
def test_dataset_display(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'dataset_table'
    model_name = 'autotest_new_constructor'
    expected_value = ['dataset_2', 'dataset_1']

    with testit.step(f'Создать таблицу"{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Добавление сущностей в структуру таблицы '):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1"], object_type='Объекты')
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset('Выбрать все')

    with testit.step('Переход на таблицу и проверка отображения таблицы'):
        table_page.open_tab('Таблица')
        assert expected_value == table_page.get_table_data_list_with_headers(2, 3, only_header=True)

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Проверка что ячейки не заполнены в таблице')
@testit.displayName('Проверка что ячейки не заполнены в таблице')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Проверка что ячейки не заполнены в таблице',
    'login_type': 'admin'
})])
def test_cell_not_filled(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'cells not filled'
    model_name = 'autotest_new_constructor'
    get_cell_value = ''

    with testit.step(f'Создать таблицу"{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Добавление сущностей в структуру таблицы '):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1"], object_type='Объекты')
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset('Выбрать все')

    with testit.step('Переход на таблицу и проверка отображения таблицы'):
        table_page.open_tab('Таблица')
        for n in range(1, 1):
            assert table_page.get_cell_value(1, n) == get_cell_value

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Заполнение ячеек тестовыми данными')
@testit.displayName('Заполнение ячеек тестовыми данными')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Заполнение ячеек тестовыми данными',
    'login_type': 'admin'
})])
def test_fill_in_the_fields(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'fill in the fields of the table'
    model_name = 'autotest_new_constructor'

    with testit.step(f'Создать таблицу"{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Добавление сущностей в структуру таблицы '):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1"], object_type='Объекты')
        table_page.add_nested_entity("Показатели", struct_type="Строки")
        table_page.set_entity_new(["indicator_1", "indicator_2"])
        time.sleep(2)
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset('dataset_1')

    with testit.step('Переход на таблицу и проверка отображения таблицы'):  # Диме: описание шага не соответствует его наполнению, нужно переделать/изменить кол-во шагов
        table_page.open_tab('Таблица')
        table_page.input_cell_value(2, 1, 100)
        table_page.input_cell_value(3, 1, 1000)
        time.sleep(2)
        assert table_page.get_cell_value(2, 1) == '100', "Значение корректное" # Диме: после запятой указывется сообщение в случае ошибки, переделать
        assert table_page.get_cell_value(3, 1) == '1000', "Значение корректное"

    with testit.step('Удалить таблицу'):
        table_page.drop_data_table(table_name)


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Переименование таблицы в дереве модели')
@testit.displayName('Переименование таблицы в дереве модели')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Переименование таблицы в дереве модели',
    'login_type': 'admin'
})])
def test_rename_table_to_tree(login_driver, aaa, parameters):
    table_page = TablePage(login_driver)
    object_page = ObjectPage(login_driver)

    table_name = 'table_kd'
    new_table_name = 'table_kd_new'
    model_name = 'autotest_model'

    with testit.step(f'Выбрать таблицу "{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.tree.select_node_object(table_name, expand_node_name=model_name)

    with testit.step(f'Переименовать таблицу "{table_name}" на "{new_table_name}" в дереве'):
        time.sleep(1)
        table_page.tree.rename_node(table_name, new_table_name)
        time.sleep(1)

    with testit.step("Проверить переименование"):
        assert table_page.tree.get_selected_node_name() == new_table_name

    with testit.step(f"Переименовать таблицу в карточке объекта {new_table_name} на {table_name}"):
        object_page.rename_title(table_name)
        time.sleep(1)

    with testit.step("Проверить переименование"):
        assert table_page.tree.get_selected_node_name() == table_name


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Переключение в режим конструктора и очистка таблицы')
@testit.displayName('Переключение в режим конструктора и очистка таблицы')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Переключение в режим конструктора и очистка таблицы',
    'login_type': 'admin'
})])
def test_switching_to_the_design_mode_and_clearing_the_table(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'table_kd_new'
    model_name = 'autotest_model'

    with testit.step(f'Выбрать таблицу "{table_name}"'):
        table_page.tree.select_node_object(model_name, expand_node_name='auto-test-table')
        table_page.tree.select_node_object(table_name, expand_node_name=model_name)

    with testit.step('Построить таблицу в конструкторе'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1"])
        table_page.add_nested_entity("Наборы данных", struct_type="Строки")
        table_page.set_dataset("dataset_1")

        table_page.add_entity_to_table("Показатели", struct_type="Столбцы")
        table_page.set_entity_new(["indicator_1"])
        time.sleep(2)

    with testit.step('Перейти в таблицу и проверить что она построилась'):
        table_page.open_tab('Таблица')
        table_page.check_table_is_set()

    with testit.step('Перейти обратно в конструктор'):
        table_page.open_tab('Конструктор')
        time.sleep(2)

    with testit.step('Очистка структуры в конструкторе'):
        table_page.clear_structure()
        time.sleep(1)

    with testit.step('Нажать на кнопку "Принять" в появившемся модальном окне'):
        table_page.modal.accept_button_click()

    with testit.step('Проверка на очищенную структуру таблицы'):
        assert table_page.check_structure_element_not_exists()


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Построение таблицы при включенной опции "Скрывать, если один"')
@testit.displayName('Построение таблицы при включенной опции "Скрывать, если один"')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Построение таблицы при включенной опции "Скрывать, если один"',
    'login_type': 'admin'
})])
def test_hide_if_one_option_enabled(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'hide_if_one_option_enabled'
    model_name = 'autotest_model'
    indicator_name = 'indicator_1'

    with testit.step(f'Найти модель "{model_name}"'):
        table_page.tree.search_node(model_name)

    with testit.step(f'Создать таблицу в модели "{model_name}"'):
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Построить таблицу в конструкторе'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1"])
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset_1")

        table_page.add_nested_entity("Показатели", struct_type="Столбцы")
        table_page.set_entity_new(["indicator_1"])
        time.sleep(2)

    with testit.step('Настроить режим отображения показателей на "Скрывать, если один"'):
        table_page.set_additional_option_display_mode("Показатели", "Видимость", "Скрывать, если один")

    with testit.step('Переход на таблицу и проверка отображения таблицы с скрытием показателя'):
        table_page.open_tab('Таблица')
        assert indicator_name not in table_page.get_table_data_list_with_headers(2, 2)


@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Построение таблицы при включенной опции "Группировка по умолчанию"')
@testit.displayName('Построение таблицы при включенной опции "Группировка по умолчанию"')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Построение таблицы при включенной опции "Группировка по умолчанию"',
    'login_type': 'admin'
})])
def test_default_grouping(login_driver, parameters):
    table_page = TablePage(login_driver)

    table_name = 'default_grouping'
    model_name = 'autotest_model'
    indicator_names = ["indicator_1", "indicator_2"]

    with testit.step(f'Найти модель "{model_name}"'):
        table_page.tree.search_node(model_name)

    with testit.step(f'Создать таблицу в модели "{model_name}"'):
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Построить таблицу в конструкторе'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object(obj_names=["obj_1", "obj_2"])
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset_1")

        table_page.add_nested_entity("Показатели", struct_type="Столбцы")
        table_page.set_entity_new(indicator_names)
        time.sleep(2)

    with testit.step('Настроить режим отображения набора данных на "Свернуть"'):
        table_page.set_additional_option_display_mode("Наборы данных", "Группировка по умолчанию", "Свернуть")

    with testit.step('Переход на таблицу и проверка отображения таблицы с скрытием показателя'):
        table_page.open_tab('Таблица')
        for indicator in indicator_names:
            assert indicator not in table_page.get_table_headers_data_list(2), f"Индикатор {indicator} отображается в " \
                                                                               f"заголовках, хотя не должен."




@testit.nameSpace('Таблицы данных')
@testit.className('Дерево моделей')
@testit.externalId('Построение таблицы при включенной опции "Переносить заголовки"')
@testit.displayName('Построение таблицы при включенной опции "Переносить заголовки"')
@pytest.mark.red_label
@pytest.mark.regression
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Модели',
    'name': 'Построение таблицы при включенной опции "Переносить заголовки"',
    'login_type': 'admin'
})])
def test_transfer_values(login_driver, parameters):
    table_page = TablePage(login_driver)
    table_name = 'transfer_values'
    model_name = 'autotest_model'

    transfer_off_size = 31
    transfer_on_size = 42

    with testit.step(f'Найти модель "{model_name}"'):
        table_page.tree.search_node(model_name)

    with testit.step(f'Создать таблицу в модели "{model_name}"'):
        table_page.create_data_table(model_name, table_name, auto_garbage_collect=True)

    with testit.step('Построить таблицу в конструкторе'):
        table_page.add_entity_to_table("Объекты", struct_type="Строки")
        table_page.set_object("obj_1")  # ошибка, исправить Диме
        time.sleep(1)
        table_page.add_entity_to_table("Наборы данных", struct_type="Столбцы")
        table_page.set_dataset("dataset_is_a_line_for_checking_the_transfer_of_headings")
        time.sleep(1)
        table_page.add_nested_entity("Показатели", struct_type="Столбцы")
        table_page.set_entity_new(["indicator_is_a_line_for_checking_the_transfer_of_headings"])
        time.sleep(1)

    with testit.step('Перейти во вкладку "Таблица" и проверить что перенос заголовков выключен'):
        table_page.open_tab('Таблица')
        value_1 = table_page.get_cell_size(1, is_header=True)

        table_page.open_tab('Таблица')

    with testit.step('Включить опцию "Переносить заголовки"'):
        table_page.open_tab('Настройки')
        table_page.set_table_settings("Переносить заголовки")

    with testit.step('Перейти во вкладку "Таблица" и проверить корректность опции "Переносить заголовки"'):
        table_page.open_tab('Таблица')
        time.sleep(2)
        value_1 = table_page.get_cell_size(1, is_header=True)
        value_2 = table_page.get_cell_size(2, is_header=True)

        for value in [value_1, value_2]:
            assert value['height'] == transfer_on_size, "Некорректный размер ячейки таблицы при включенном переносе " \
                                                    "заголовков!"
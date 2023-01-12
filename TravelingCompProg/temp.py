path_to_db = "data/tours.db"
table_names_rus = {"hotels": "Отели",
                   "points": "Населенные пункты",
                   "tour_types": "Типы туров",
                   "transport_types": "Типы транспорта"
                   }

table_names_eng = {v: k for k, v in table_names_rus.items()}
cols_names_rus = {"hotel_id": "Номер отеля",
                  "point_id": "Название города",
                  "tour_id": "Номер тура",
                  "name": "Наименование",
                  "stars": "Количество звезд",
                  "point_name": "Название города",
                  "tour_type": "Тип тура",
                  "list_id": "Номер списка",
                  "start_date": "Дата начала",
                  "finish_date": "Дата окончания",
                  "price": "Стоимость",
                  "string_id": "Номер строки",
                  "type_name": "Название типа",
                  "type_id": "Номер типа",
                  "tour_name": "Название тура",
                  "departure_point": "Место отправления",
                  "transport_type": "Тип транспорта",
                  "orders_amount": "Количество заказов"
                  }
cols_names_eng = {v: k for k, v in cols_names_rus.items()}

info_note = "\n\n\nВы работаете с сетью туристического бюро \"У Вереса\"\n" \
            "Нас можно найти по адресу: ул. Войкова 18/211\n" \
            "Контактное лицо: Верес федор Степанович\n" \
            "Телефон: +375445437828\n"
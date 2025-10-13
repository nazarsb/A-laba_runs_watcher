start_message = 📝 Какое событие запланировать?
planned_events = <u><b>📆 Запланированые события:</b></u>\n
no_events_planned = <b>В А-лабе всё спокойно.\nЗапланированных событий нет. 😴</b>\n

new_run_instruments = На каком <b>приборе</b> запускаемся?
new_run_start_date = Дата <b>НАЧАЛА</b> запуска
new_run_reagent_kit = Какой <b>набор</b> будем использовать?

<i>на основании этого бот сам посчитает длительность запуска 🤓</i>
new_run_duration = Введите длительность запуска <u><b>в часах</b></u>.

summary_pretext = 📝 Краткое описание события,
                    Если все <b>ОК</b>, жмите <b>"Завершить"</b>.
                    {""}

new_run_summary = <b>Запланированное событие:</b> { $event_type },
                    <b>Инструмент:</b> { $instrument }
                    <b>Дата запуска:</b> { $run_start_date }
                    
new_run_duration = <b>Длительность запуска:</b> { $qitan_time } ч.
new_run_reagent = <b>Реагент:</b> { $reagent }

calendar_warning = { $selected_date } уже в прошлом. 
                    Сегодня { $today }.
                    Выберете актуальную дату.
wrong_end_date = Ход времени не изменить. { $selected_date } было до { $start_date }. 
                Выберете актуальную дату.

wrong_duration_frmt = Вы ввели некорректный формат длительности. Просто напишите число - сколько часов будет длиться запуск?

wrong_time_format = Вы ввели некорректный формат времени. Попробуйте еще раз.

new_run_planned_notification = 🚀 Запланирован новый <b>запуск</b> на <b>{ $run_start_date } - { $run_end_date } </b>.
                                Просмотр событий _ по команде 
                                <b>/show_events</b>

electro_start_date = ⏳ В какой день <b>начало</b> отключения?

electro_end_date =  ⏳ <b>Начало отключения</b>: { $event_start_date },
                    ⌛️ А в какой <b>ВЕРНУТ</b> электричество?

do_enter_time = 🗓 Отключение будет в дни: 
                <b>{ $event_start_date } - { $event_end_date }</b>,
                <i>Хотите указать конкретное время отключения?</i>

elcetro_start_time = 🗓 Отключение будет в дни: <b>{ $event_start_date } - { $event_end_date }</b>,
                    Введите время <b>НАЧАЛА</b> отключения,
                    <b><i>Формат - ЧЧ:ММ</i></b>

electro_end_time = 🗓 Отключение будет в дни: <b>{ $event_start_date } - { $event_end_date }</b>,
                    Время начала отключения: <b>{ $time1 }</b>
                    В какое время <b>ОКОНЧАНИЯ</b> отключения?
                    <b><i>Формат - ЧЧ:ММ</i></b>

electro_summary_with_time = <b>Тип события:</b> { $event_type }
                            <b>Начало отключения:</b> { $event_start_date } в { $time1 },
                            <b>Конец отключения:</b> { $event_end_date } в { $time2 }

                            Все верно?

electro_summary_wo_time =   <b>Тип события:</b> { $event_type }
                            <b>Начало отключения:</b> { $event_start_date },
                            <b>Конец отключения:</b> { $event_end_date }

                            Все верно?

electro_planned_notification = ⚠️ Запланировано отключение электичества на <b>{ $event_start_date } - { $event_end_date }</b>.
                                Просмотр событий - по команде 
                                <b>/show_events</b>
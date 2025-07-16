# Импорт библиотеки Flet для построения UI
import flet as ft

# Импорт базового класса представления
from .base_view import BaseView

# Импорт модуля для отслеживания и вывода ошибок
import traceback

# Представление заявок, наследуется от BaseView
class TicketsView(BaseView):
    # Метод построения представления (UI)
    def build(self):
        try:
            # Получение информации об организации пользователя по его Telegram ID
            org_info = self.user_service.get_company_info(self.tg_id)
            # Если информации нет — используем заглушки
            org_name, org_address, org_phone = org_info if org_info else ("Не указано", "Не указано", "Не указано")

            # Получаем список заявок в работе и завершённых по названию компании
            all_tickets_in_progress = self.ticket_service.get_ticket_by_status_and_company("В работе", org_name)
            company_closed_tickets = self.ticket_service.get_ticket_by_status_and_company("Завершена", org_name)

            # Подсчёт заявок
            total_open_tickets = len(all_tickets_in_progress)
            total_closed_tickets = len(company_closed_tickets)

            # Установка верхней панели с названием компании
            self.page.appbar = ft.CupertinoAppBar(
                leading=ft.Icon(name=ft.icons.WORK, color="White", size=28),
                bgcolor=ft.colors.BLUE_500,
                trailing=ft.Icon(name=ft.icons.WORK, color="White", size=28),
                middle=ft.Text(f"{org_name}", color="White"),
            )

            # Создание круговой диаграммы (pie chart)
            chart = self._create_tickets_chart(total_open_tickets, total_closed_tickets)

            # Создание списка заявок
            ticket_list = ft.ListView(spacing=10, padding=20, first_item_prototype=True)
            self._populate_ticket_list(ticket_list, all_tickets_in_progress + company_closed_tickets)

            # Возвращаем список UI-компонентов для отображения
            return [
                ft.Container(chart),  # Диаграмма
                ft.Text(              # Контактная информация и статистика
                    f"Контактный номер: {org_phone}\nАдрес: {org_address}\n\n"
                    f"Открытых заявок {total_open_tickets}\nЗакрытых заявок: {total_closed_tickets}\n",
                    size=18
                ),
                ft.Container(ft.Text("Заявки", size=18)),  # Заголовок
                ft.Icon(name=ft.icons.ARROW_DOWNWARD, color=ft.colors.BLUE_ACCENT_700),  # Иконка
                ft.Container(ticket_list, margin=0, width=self.page.width)  # Список заявок
            ]
        except Exception as e:
            # В случае ошибки — выводим текст ошибки на экран
            traceback.print_exc()
            return ft.Text(f"Ошибка: {str(e)}", color="red")

    # Метод создания круговой диаграммы по открытым/закрытым заявкам
    def _create_tickets_chart(self, open_tickets, closed_tickets):
        # Стиль обычного и наведённого состояния заголовков на секциях диаграммы
        normal_title_style = ft.TextStyle(size=15, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
        hover_title_style = ft.TextStyle(size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                                         shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54))

        # Обработчик события наведения на сектор диаграммы
        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart_tickets.sections):
                if idx == e.section_index:
                    section.radius = self.hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = self.normal_radius
                    section.title_style = normal_title_style
            chart_tickets.update()  # Обновляем диаграмму

        # Сама диаграмма
        chart_tickets = ft.PieChart(
            sections=[
                ft.PieChartSection(  # Сектор с завершёнными заявками
                    closed_tickets,
                    title=f"C: {closed_tickets}",
                    title_style=normal_title_style,
                    color=ft.colors.BLUE_400,
                    radius=self.normal_radius,
                ),
                ft.PieChartSection(  # Сектор с заявками в работе
                    open_tickets,
                    title=f"O: {open_tickets}",
                    title_style=normal_title_style,
                    color=ft.colors.BLUE_200,
                    radius=self.normal_radius,
                ),
            ],
            sections_space=5,
            center_space_radius=65,
            on_chart_event=on_chart_event,
            expand=False,
        )
        return chart_tickets

    # Метод заполняет список заявок (ticket_list) на основе переданных данных
    def _populate_ticket_list(self, ticket_list, tickets):
        # Функция вызывается при клике по заявке
        def tile_clicked(ticket_id, e):
            ticket_info = self.ticket_service.get_ticket_info(ticket_id)
            if not ticket_info: return

            # Формируем текст с полной информацией по заявке
            ticket_txt = (
                f"Детали заявки: #{ticket_info[0]}\n\n"
                f"ID пользователя: {ticket_info[1]}\nОрганизация: {ticket_info[2]}\n"
                f"Адрес: {ticket_info[3]}\n\nСообщение: - {ticket_info[4]}\n\n"
                f"Время создания: {ticket_info[5]}\nСтатус: {ticket_info[6]}\n\n"
            )

            # Показываем диалоговое окно с информацией
            self.page.dialog = ft.AlertDialog(
                title=ft.Text(ticket_txt, size=16),
                on_dismiss=lambda e: print("Dialog dismissed!")
            )
            self.page.dialog.open = True
            self.page.update()

        # Для каждой заявки создаём интерактивную плитку и добавляем в список
        for ticket in tickets:
            # Выбираем иконку в зависимости от статуса
            icon = ft.icons.HELP_OUTLINE if ticket.state_ticket == "В работе" else ft.icons.CHECK
            # Добавляем строку со стилем и кликом
            ticket_list.controls.append(
                ft.Row([ft.CupertinoListTile(
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Icon(name=icon),
                    title=ft.Text(f"Заявка: {ticket.number_ticket}"),
                    subtitle=ft.Text(f"{ticket.state_ticket}"),
                    bgcolor=ft.colors.BLUE_ACCENT_700,
                    on_click=lambda e, tid=ticket.number_ticket: tile_clicked(tid, e)
                )])
            )

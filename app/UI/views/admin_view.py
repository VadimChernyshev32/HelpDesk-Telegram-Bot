import flet as ft
from .base_view import BaseView
import traceback

# Класс представления панели администратора, наследуется от BaseView
class AdminView(BaseView):
    def build(self):
        try:
            # Получение статистики
            all_users = len(self.user_service.get_all_users())  # Кол-во всех пользователей
            all_company = len(self.company_service.get_all_companies())  # Кол-во всех компаний
            all_tickets = len(self.ticket_service.get_all_tickets())  # Кол-во всех заявок
            all_closed_tickets = len(self.ticket_service.get_ticket_by_status("Завершена"))  # Заявки завершены
            all_open_ticket = len(self.ticket_service.get_ticket_by_status("В работе"))  # Заявки в работе

            # Расчёт процента завершённых заявок
            ticket_stat = round((all_closed_tickets / all_tickets) * 100) if all_tickets > 0 else 0

            # Получение списка людей в компаниях с ролями
            rendered_people = self.company_service.get_rendered_people_for_admin()

            # Фильтрация по ролям
            total_all_directors = [p for p in rendered_people if "Директор" in p[0]]
            total_all_managers = [p for p in rendered_people if "Менеджер" in p[0]]
            total_all_workers = [p for p in rendered_people if "Сотрудник" in p[0]]
            total_all_potential = [p for p in rendered_people if "Ожидаем входа" in p[0]]

            # Словарь с количеством пользователей по ролям
            counts = {
                "director": len(total_all_directors),
                "manager": len(total_all_managers),
                "worker": len(total_all_workers),
                "potential": len(total_all_potential),
                "total": len(total_all_workers) + len(total_all_managers) + len(total_all_directors)
            }

            # Установка верхней панели приложения (AppBar)
            self.page.appbar = ft.CupertinoAppBar(
                leading=ft.Icon(name=ft.icons.ADMIN_PANEL_SETTINGS, color="White", size=28),
                bgcolor=ft.colors.PURPLE_500,
                trailing=ft.Icon(name=ft.icons.ADMIN_PANEL_SETTINGS, color="White", size=28),
                middle=ft.Text("Админ панель", color="White"),
            )

            # Создание круговой диаграммы заявок
            chart = self._create_admin_chart(all_open_ticket, all_closed_tickets)

            # Список сотрудников
            worker_list = ft.ListView(spacing=10, padding=20, first_item_prototype=True)

            # Заполнение списка сотрудников
            self._populate_worker_list(worker_list, total_all_directors + total_all_managers + total_all_workers + total_all_potential)

            # Возвращаем виджеты на экран
            return [
                ft.Container(chart, margin=0, padding=0),
                ft.Container(
                    ft.Text(
                        f"Всего пользователей: {all_users}\n"
                        f"Всего компаний: {all_company}\n"
                        f"Всего заявок: {all_tickets}\n"
                        f"{ticket_stat}% заявок выполнено",
                        size=18
                    ),
                    margin=0,
                    padding=0
                ),
                ft.Container(worker_list, margin=0, width=self.page.width)
            ]

        except Exception as e:
            # Обработка ошибок при построении админ-панели
            traceback.print_exc()
            return ft.Text(f"Ошибка при построении админ-панели: {str(e)}", color="red", size=20)

    # Метод для создания круговой диаграммы (PieChart)
    def _create_admin_chart(self, all_open_tickets, all_closed_tickets):
        # Стили текста
        normal_title_style = ft.TextStyle(size=15, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
        hover_title_style = ft.TextStyle(size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                                         shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54))

        # Обработчик событий диаграммы (наведение на сегмент)
        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart_tickets.sections):
                if idx == e.section_index:
                    section.radius = self.hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = self.normal_radius
                    section.title_style = normal_title_style
            chart_tickets.update()

        # Создание диаграммы
        chart_tickets = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    all_closed_tickets,
                    title=f"C: {all_closed_tickets}",
                    title_style=normal_title_style,
                    color=ft.colors.PURPLE_400,
                    radius=self.normal_radius,
                ),
                ft.PieChartSection(
                    all_open_tickets,
                    title=f"O: {all_open_tickets}",
                    title_style=normal_title_style,
                    color=ft.colors.PURPLE_200,
                    radius=self.normal_radius,
                ),
            ],
            sections_space=5,
            center_space_radius=65,
            on_chart_event=on_chart_event,
            expand=False,
        )
        return chart_tickets

    # Метод для заполнения списка работников
    def _populate_worker_list(self, worker_list, people):
        # Обработчик клика по сотруднику
        def tile_clicked(worker_id, e):
            try:
                user_id = int(worker_id.split('_')[1])
                worker_info = self.user_service.get_user_info_by_id(user_id)

                # Формирование текста с информацией
                text = (f"Номер сотрудника: {worker_info.phone_user}\n"
                        f"Организация: {worker_info.organization_user}\n"
                        f"Права: {worker_info.status}\n") if worker_info else "Информация не найдена"
            except Exception as ex:
                text = f"❌ Ошибка: {ex}"

            # Показываем диалог с информацией
            self.page.dialog = ft.AlertDialog(
                title=ft.Text(text, size=16),
                on_dismiss=lambda e: print("Dialog dismissed!")
            )
            self.page.dialog.open = True
            self.page.update()

        # Обработка каждого работника
        for label, worker_id in people:
            # Назначение иконки и цвета в зависимости от роли
            icon_color = {
                "Директор": (ft.icons.MANAGE_ACCOUNTS_OUTLINED, ft.colors.PURPLE_400),
                "Менеджер": (ft.icons.MANAGE_ACCOUNTS_OUTLINED, ft.colors.PURPLE_300),
                "Сотрудник": (ft.cupertino_icons.PERSON, ft.colors.PURPLE_200),
                "Ожидаем": (ft.cupertino_icons.ALARM, ft.colors.PURPLE_100),
            }

            icon_name, color = next(
                ((ic, clr) for key, (ic, clr) in icon_color.items() if key in label),
                (ft.cupertino_icons.PERSON, ft.colors.ORANGE_600)  # Значения по умолчанию
            )

            # Определение роли по тексту метки
            role = next(
                (r for r in ["Директор", "Менеджер", "Сотрудник", "Ожидаем"] if r in label),
                "Сотрудник"
            )

            # Создание плитки (элемента списка)
            tile = ft.CupertinoListTile(
                bgcolor_activated=ft.colors.AMBER_ACCENT,
                leading=ft.Icon(name=icon_name, color=color),
                title=ft.Text(label),
                subtitle=ft.Text(role),
                bgcolor=color,
                on_click=lambda e, wid=worker_id: tile_clicked(wid, e) if "wait_" not in wid else None
            )

            # Добавление плитки в список
            worker_list.controls.append(ft.Row([tile]))

        return worker_list

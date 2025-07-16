import flet as ft
from .base_view import BaseView
import traceback

class WorkersView(BaseView):
    def build(self):
        try:
            # Получаем информацию о компании пользователя по его tg_id
            org_info = self.user_service.get_company_info(self.tg_id)
            # Название организации или "Не указано", если информации нет
            org_name = org_info[0] if org_info else "Не указано"

            # Получаем список сотрудников с ролью и id
            rendered_people = self.company_service.get_rendered_people(org_name)
            # Фильтруем сотрудников по ролям
            directors = [p for p in rendered_people if "Директор" in p[0]]
            managers = [p for p in rendered_people if "Менеджер" in p[0]]
            workers = [p for p in rendered_people if "Сотрудник" in p[0]]
            potential = [p for p in rendered_people if "Ожидаем входа" in p[0]]

            # Считаем количество сотрудников по категориям и общее количество
            counts = {
                "director": len(directors),
                "manager": len(managers),
                "worker": len(workers),
                "potential": len(potential),
                "total": len(workers) + len(managers) + len(directors)
            }

            # Настраиваем верхнюю панель (appbar) с названием компании
            self.page.appbar = ft.CupertinoAppBar(
                leading=ft.Icon(name=ft.icons.WORK, color="White", size=28),
                bgcolor=ft.colors.ORANGE_500,
                trailing=ft.Icon(name=ft.icons.WORK, color="White", size=28),
                middle=ft.Text(f"{org_name}", color="White"),
            )

            # Создаем круговую диаграмму с данными о сотрудниках
            chart = self._create_workers_chart(counts)
            # Создаем список для отображения сотрудников
            worker_list = ft.ListView(spacing=10, padding=20, first_item_prototype=True)
            # Заполняем список сотрудниками всех ролей
            self._populate_worker_list(worker_list, directors + managers + workers + potential)

            # Возвращаем список элементов интерфейса:
            # диаграмма, текст с числом сотрудников и список
            return [
                ft.Container(chart, margin=0, padding=0),
                ft.Container(
                    ft.Text(
                        f"В компании сейчас: {counts['total']} сотрудников\n"
                        f"Ожидаем {counts['potential']} сотрудника",
                        size=18
                    ), margin=0, padding=0
                ),
                ft.Container(worker_list, margin=0, width=self.page.width)
            ]
        except Exception as e:
            # Если что-то пошло не так, выводим стек ошибки и текст ошибки на экран
            traceback.print_exc()
            return ft.Text(f"Ошибка: {str(e)}", color="red")

    def _create_workers_chart(self, counts):
        # Стили текста для диаграммы: нормальный и при наведении
        normal_title_style = ft.TextStyle(size=15, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
        hover_title_style = ft.TextStyle(size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                                       shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54))

        # Вспомогательная функция для создания иконок-беджей на диаграмме
        def badge(icon, color):
            return ft.Container(ft.Icon(icon, color="White", size=35), width=55, height=55)

        # Обработчик событий диаграммы — изменение стиля выделенного сектора при наведении
        def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart_workers.sections):
                if idx == e.section_index:
                    section.radius = self.hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = self.normal_radius
                    section.title_style = normal_title_style
            chart_workers.update()

        # Создаем саму круговую диаграмму с секторами для разных ролей
        chart_workers = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    counts['director'] + counts['manager'],  # объединяем директора и менеджера
                    title_style=normal_title_style,
                    badge=badge(ft.icons.MANAGE_ACCOUNTS_OUTLINED, ft.colors.DEEP_ORANGE),
                    badge_position=0.50,
                    color=ft.colors.DEEP_ORANGE,
                    radius=self.normal_radius,
                ),
                ft.PieChartSection(
                    counts['worker'],
                    title_style=normal_title_style,
                    badge=badge(ft.icons.PERSON, ft.colors.ORANGE_600),
                    badge_position=0.50,
                    color=ft.colors.ORANGE_500,
                    radius=self.normal_radius,
                ),
                ft.PieChartSection(
                    counts['potential'],
                    title_style=normal_title_style,
                    badge=badge(ft.icons.ALARM, ft.colors.ORANGE_300),
                    badge_position=0.50,
                    color=ft.colors.ORANGE_300,
                    radius=self.normal_radius,
                ),
            ],
            sections_space=5,            # расстояние между секторами
            center_space_radius=65,      # радиус пустого пространства в центре
            on_chart_event=on_chart_event,
            expand=False,
        )
        return chart_workers

    def _populate_worker_list(self, worker_list, people):
        # Обработчик клика по элементу списка сотрудника
        def tile_clicked(worker_id, e):
            try:
                # Извлекаем id пользователя из worker_id
                user_id = int(worker_id.split('_')[1])
                # Получаем информацию о пользователе по id
                worker_info = self.user_service.get_user_info_by_id(user_id)

                # Формируем текст с подробной информацией о сотруднике
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

        # Проходим по всем сотрудникам и создаем для каждого элемент списка
        for label, worker_id in people:
            # Определяем иконку и цвет в зависимости от роли сотрудника
            icon_color = {
                "Директор": (ft.icons.MANAGE_ACCOUNTS_OUTLINED, ft.colors.DEEP_ORANGE_ACCENT_700),
                "Менеджер": (ft.icons.MANAGE_ACCOUNTS_OUTLINED, ft.colors.ORANGE_600),
                "Сотрудник": (ft.cupertino_icons.PERSON, ft.colors.ORANGE_600),
                "Ожидаем": (ft.cupertino_icons.ALARM, ft.colors.ORANGE_300),
            }

            # Выбираем иконку и цвет по ключевому слову из label
            icon_name, color = next(
                ((ic, clr) for key, (ic, clr) in icon_color.items() if key in label),
                (ft.cupertino_icons.PERSON, ft.colors.ORANGE_600)  # значение по умолчанию
            )

            # Определяем роль для отображения в subtitle
            role = next(
                (r for r in ["Директор", "Менеджер", "Сотрудник", "Ожидаем"] if r in label),
                "Сотрудник"
            )

            # Создаем плитку сотрудника с цветом, иконкой, заголовком и подзаголовком
            tile = ft.CupertinoListTile(
                bgcolor_activated=ft.colors.AMBER_ACCENT,
                leading=ft.Icon(name=icon_name, color=color),
                title=ft.Text(label),
                subtitle=ft.Text(role),
                bgcolor=color,
                # Обработка клика по плитке — открываем диалог, если это не "ожидающий" сотрудник
                on_click=lambda e, wid=worker_id: tile_clicked(wid, e) if "wait_" not in wid else None
            )
            # Добавляем плитку в список (в отдельной строке)
            worker_list.controls.append(ft.Row([tile]))

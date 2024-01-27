import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QSizePolicy, QMessageBox, QDialog, QHeaderView, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook

class RegistrationWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.setWindowTitle("Регистрация")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.label_username = QLabel("Имя пользователя:")
        self.label_password = QLabel("Пароль:")

        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)

        self.button_register = QPushButton("Зарегистрироваться")
        self.button_register.clicked.connect(self.register_user)

        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

    def register_user(self):
        # Получаем данные из полей ввода
        username = self.entry_username.text()
        password = self.entry_password.text()

        # Подключение к базе данных
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            # Проверка, не существует ли уже пользователь с таким именем
            check_query = "SELECT * FROM authentication_user WHERE username = %s"
            cursor.execute(check_query, (username,))
            result = cursor.fetchone()

            if result:
                QMessageBox.warning(self, "Пользователь уже существует",
                                    "Пользователь с таким именем уже зарегистрирован.")
            else:
                # Регистрация нового пользователя
                insert_query = "INSERT INTO authentication_user (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (username, password))
                connection.commit()

                QMessageBox.information(self, "Регистрация успешна", "Вы успешно зарегистрированы.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", "Ошибка при подключении к базе данных:\n{}".format(err))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.label_username = QLabel("Имя пользователя:")
        self.label_password = QLabel("Пароль:")

        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.authenticate_user)

        self.button_register = QPushButton("Зарегистрироваться")
        self.button_register.clicked.connect(self.show_registration_window)

        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

        self.registration_window = RegistrationWindow(self)
        self.main_menu = None  # Создаем переменную для главного меню, чтобы иметь к ней доступ

    def authenticate_user(self, is_admin):
        # Получаем данные из полей ввода
        username = self.entry_username.text()
        password = self.entry_password.text()

        # Подключение к базе данных
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            # Проверка наличия пользователя в базе данных
            query = "SELECT * FROM authentication_user WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, "Авторизация успешна", "Добро пожаловать, {}!".format(username))
                # При успешной авторизации открываем главное меню
                self.open_main_menu(username == 'admin')
            else:
                QMessageBox.critical(self, "Ошибка авторизации", "Неправильное имя пользователя или пароль")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", "Ошибка при подключении к базе данных:\n{}".format(err))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        self.close()

    def show_registration_window(self):
        self.registration_window.show()

    def open_main_menu(self, is_admin):
        if not self.main_menu:
            self.main_menu = MainMenu(is_admin)
        self.main_menu.show()


class RegistrationDialog(QDialog):
    def __init__(self, tournament_name, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Регистрация на турнир")
        self.setGeometry(300, 300, 300, 200)

        self.tournament_name = tournament_name

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Виджеты для ввода данных команды
        self.label_team_name = QLabel("Название команды:")
        self.entry_team_name = QLineEdit()

        self.label_player1 = QLabel("Игрок 1:")
        self.entry_player1 = QLineEdit()

        self.label_player2 = QLabel("Игрок 2:")
        self.entry_player2 = QLineEdit()

        self.label_player3 = QLabel("Игрок 3:")
        self.entry_player3 = QLineEdit()

        self.label_player4 = QLabel("Игрок 4:")
        self.entry_player4 = QLineEdit()

        self.label_player5 = QLabel("Игрок 5:")
        self.entry_player5 = QLineEdit()

        # Кнопка для регистрации команды
        self.button_register = QPushButton("Зарегистрироваться")
        self.button_register.clicked.connect(self.register_team)

        # Виджет для отображения списка зарегистрированных команд на турнире
        self.label_registered_teams = QLabel("Список зарегистрированных команд на турнире:")
        self.list_registered_teams = QListWidget()

        layout.addWidget(self.label_team_name)
        layout.addWidget(self.entry_team_name)
        layout.addWidget(self.label_player1)
        layout.addWidget(self.entry_player1)
        layout.addWidget(self.label_player2)
        layout.addWidget(self.entry_player2)
        layout.addWidget(self.label_player3)
        layout.addWidget(self.entry_player3)
        layout.addWidget(self.label_player4)
        layout.addWidget(self.entry_player4)
        layout.addWidget(self.label_player5)
        layout.addWidget(self.entry_player5)
        layout.addWidget(self.button_register)
        layout.addWidget(self.label_registered_teams)
        layout.addWidget(self.list_registered_teams)

        self.setLayout(layout)

    def register_team(self):
        team_name = self.entry_team_name.text()
        player1 = self.entry_player1.text()
        player2 = self.entry_player2.text()
        player3 = self.entry_player3.text()
        player4 = self.entry_player4.text()
        player5 = self.entry_player5.text()

        # Проверка, чтобы все поля были заполнены
        if not team_name or not player1 or not player2 or not player3 or not player4 or not player5:
            QMessageBox.warning(self, "Неполные данные", "Пожалуйста, заполните все поля.")
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            # Проверка, не зарегистрирована ли команда уже на данный турнир
            check_team_query = "SELECT * FROM team WHERE team_name = %s AND tournament_id = (SELECT id FROM tournament WHERE tournament_name = %s)"

            cursor.execute(check_team_query, (team_name, self.tournament_name))
            team_result = cursor.fetchone()

            if team_result:
                QMessageBox.warning(self, "Команда уже зарегистрирована", "Команда уже участвует в этом турнире.")
            else:
                # Регистрация команды на турнире
                insert_team_query = "INSERT INTO team (tournament_id, team_name, player1, player2, player3, player4, player5) " \
                                    "VALUES ((SELECT id FROM tournament WHERE tournament_name = %s), %s, %s, %s, %s, %s, %s)"

                cursor.execute(insert_team_query,
                               (self.tournament_name, team_name, player1, player2, player3, player4, player5))
                connection.commit()

                QMessageBox.information(self, "Регистрация успешна",
                                        f"Команда {team_name} зарегистрирована на турнире {self.tournament_name}.")

                # Обновление списка зарегистрированных команд после успешной регистрации
                self.update_registered_teams()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", "Ошибка при подключении к базе данных:\n{}".format(err))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                self.accept()  # Закрываем окно после успешной регистрации



    def update_registered_teams(self):
        # Получите и отобразите список зарегистрированных команд для выбранного турнира
        registered_teams = self.get_registered_teams(self.tournament_name)
        self.display_registered_teams(registered_teams)

    def get_registered_teams(self, tournament_name):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            query = "SELECT team_name FROM team WHERE tournament_id = (SELECT id FROM tournament WHERE tournament_name = %s)"
            cursor.execute(query, (tournament_name,))
            result = cursor.fetchall()

            if result:
                return [team[0] for team in result]
            else:
                return []

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", "Ошибка при подключении к базе данных:\n{}".format(err))
            return []

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def display_registered_teams(self, registered_teams):
        self.list_registered_teams.clear()
        self.list_registered_teams.addItems(registered_teams)

    def mousePressEvent(self, event):
        # При нажатии мыши на метку со списком зарегистрированных команд,
        # выделяем цветом и выводим данные
        if self.label_registered_teams.underMouse():
            self.update_registered_teams()
            self.list_registered_teams.setVisible(True)
        else:
            self.list_registered_teams.setVisible(False)

    def showEvent(self, event):
        # При отображении диалога, скрываем список зарегистрированных команд
        self.list_registered_teams.setVisible(False)


class MainMenu(QWidget):
    def __init__(self, is_admin):
        super().__init__()
        self.is_admin = is_admin
        self.setWindowTitle("Главное меню")
        self.setGeometry(300, 300, 800, 600)

        self.button_create_tournament = QPushButton("Создать турнир", self)
        self.button_create_tournament.clicked.connect(self.show_create_tournament_dialog)
        self.button_create_tournament.setVisible(is_admin)

        layout = QVBoxLayout()

        # Добавляем QTableWidget для отображения турнирных данных
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(5)  # Добавляем еще одну колонку для кнопок


        layout.addWidget(self.table_widget)

        self.button_participate = QPushButton("График регистраций на турниры", self)
        self.button_participate.clicked.connect(self.participate_in_tournament)

        layout.addWidget(self.button_participate)

        self.setLayout(layout)
        self.button_export_excel = QPushButton("Получить отчет в Excel", self)
        self.button_export_excel.clicked.connect(self.export_to_excel)
        self.button_export_excel.setVisible(is_admin)
        layout.addWidget(self.button_export_excel)


        layout.addWidget(self.button_create_tournament)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.load_tournaments_from_database()

    def export_to_excel(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Отказано в доступе", "Только администраторы могут экспортировать данные.")
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            query = """
            SELECT t.tournament_name, te.team_name, te.player1, te.player2, te.player3, te.player4, te.player5
            FROM tournament t
            LEFT JOIN team te ON t.id = te.tournament_id
            ORDER BY t.tournament_name
            """
            cursor.execute(query)
            data = cursor.fetchall()

            # Создаем DataFrame из данных запроса
            df = pd.DataFrame(data,
                              columns=["Турнир", "Команда", "Игрок 1", "Игрок 2", "Игрок 3", "Игрок 4", "Игрок 5"])

            # Создаем Excel-файл
            excel_file = "турниры_и_участники.xlsx"
            df.to_excel(excel_file, index=False, sheet_name="Лист1")

            QMessageBox.information(self, "Экспорт в Excel", f"Данные успешно экспортированы в {excel_file}")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке данных для экспорта: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    def show_registration_chart(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            query = """
            SELECT t.tournament_name, COALESCE(COUNT(te.team_name), 0) as registrations
            FROM tournament t
            LEFT JOIN team te ON t.id = te.tournament_id
            GROUP BY t.tournament_name
            """
            cursor.execute(query)
            data = cursor.fetchall()

            tournament_names = [item[0] for item in data]
            registrations = [item[1] for item in data]

            # Отображение графика
            plt.bar(tournament_names, registrations)
            plt.xlabel('Турнир')
            plt.ylabel('Количество зарегистрированных команд')
            plt.title('Статистика регистраций на турнирах')
            plt.xticks(rotation=45, ha="right")
            plt.show()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке статистики регистраций: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_tournaments_from_database(self):
        # Очистите таблицу перед загрузкой
        self.table_widget.setRowCount(0)

        # Подключение к базе данных
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            query = "SELECT tournament_name, date, prize FROM tournament"
            cursor.execute(query)
            tournaments = cursor.fetchall()

            for tournament in tournaments:
                tournament_name, date, prize = tournament
                self.add_tournament_data(self.table_widget, tournament_name, date, prize, "")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке турниров: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_tournament_list(self):
        # Очистите таблицу перед обновлением
        self.table_widget.setRowCount(0)
        # Загрузите турниры заново из базы данных и обновите таблицу
        self.load_tournaments_from_database()

    def show_create_tournament_dialog(self):
        create_tournament_dialog = CreateTournamentDialog(self)
        create_tournament_dialog.exec_()

    def add_tournament_data(self, table_widget, tournament, date, prize, image_path):
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)

        table_widget.setItem(row_position, 0, QTableWidgetItem(tournament))
        table_widget.setItem(row_position, 1, QTableWidgetItem(date))
        table_widget.setItem(row_position, 2, QTableWidgetItem(prize))

        participate_button = QPushButton("Принять участие", self)
        participate_button.clicked.connect(lambda state, row=row_position: self.show_registration_dialog(row))

        participate_button.setFixedSize(120, 30)
        layout = QHBoxLayout()
        layout.addWidget(participate_button)
        layout.setAlignment(Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        table_widget.setCellWidget(row_position, 3, widget)
        self.table_widget.setHorizontalHeaderLabels(["Название", "Дата", "Приз", "", ""])

        participate_button = QPushButton("Принять участие", self)
        participate_button.clicked.connect(lambda state, row=row_position: self.show_registration_dialog(row))

        participate_button.setFixedSize(120, 30)
        layout = QHBoxLayout()
        layout.addWidget(participate_button)
        layout.setAlignment(Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        table_widget.setCellWidget(row_position, 4, widget)
        delete_button = QPushButton("Удалить турнир", self)
        delete_button.clicked.connect(lambda state, row=row_position: self.delete_tournament(row))
        delete_button.setFixedSize(120, 30)
        layout_delete = QHBoxLayout()
        layout_delete.addWidget(delete_button)
        layout_delete.setAlignment(Qt.AlignCenter)
        widget_delete = QWidget()
        widget_delete.setLayout(layout_delete)
        table_widget.setCellWidget(row_position, 4, widget_delete)
    def resize_table_columns(self):
        # Установка фиксированной ширины для столбца с изображениями
        self.table_widget.setColumnWidth(3, 120)
        # Автоматическое изменение размеров остальных столбцов
        self.table_widget.resizeColumnsToContents()

    def delete_tournament(self, row):
        if row == -1:
            QMessageBox.warning(self, "Выберите турнир", "Пожалуйста, выберите турнир для удаления.")
            return

        tournament_name = self.table_widget.item(row, 0).text()
        tournament_id = self.get_tournament_id(tournament_name)

        # Проверка, является ли текущий пользователь администратором
        if not self.is_admin:
            QMessageBox.warning(self, "Отказано в доступе", "Только администраторы могут удалять турниры.")
            return

        # Подключение к базе данных
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            delete_query = "DELETE FROM tournament WHERE id = %s"
            cursor.execute(delete_query, (tournament_id,))
            connection.commit()

            QMessageBox.information(self, "Успешно", f"Турнир {tournament_name} удален из базы данных.")
            self.update_tournament_list()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при удалении турнира: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def participate_in_tournament(self):
        self.show_registration_chart()


    def show_registration_dialog(self, row):
        if row == -1:
            QMessageBox.warning(self, "Выберите турнир", "Пожалуйста, выберите турнир для регистрации команды.")
            return

        tournament_name = self.table_widget.item(row, 0).text()
        tournament_id = self.get_tournament_id(tournament_name)

        registration_dialog = RegistrationDialog(tournament_name, self)
        registration_dialog.exec_()

    def get_tournament_id(self, tournament_name):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            query = "SELECT id FROM tournament WHERE tournament_name = %s"
            cursor.execute(query, (tournament_name,))
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return None

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", "Ошибка при подключении к базе данных:\n{}".format(err))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class CreateTournamentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Создать турнир")
        self.setGeometry(300, 300, 400, 200)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label_tournament_name = QLabel("Название турнира:")
        self.entry_tournament_name = QLineEdit()

        self.label_date = QLabel("Дата:")
        self.entry_date = QLineEdit()

        self.label_prize = QLabel("Призовые:")
        self.entry_prize = QLineEdit()

        self.button_create = QPushButton("Создать")
        self.button_create.clicked.connect(self.create_tournament)

        layout.addWidget(self.label_tournament_name)
        layout.addWidget(self.entry_tournament_name)
        layout.addWidget(self.label_date)
        layout.addWidget(self.entry_date)
        layout.addWidget(self.label_prize)
        layout.addWidget(self.entry_prize)
        layout.addWidget(self.button_create)

        self.setLayout(layout)

    def create_tournament(self):
        tournament_name = self.entry_tournament_name.text()
        date = self.entry_date.text()
        prize = self.entry_prize.text()

        # Подключение к базе данных
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='authentication'
            )
            cursor = connection.cursor()

            # Проверка наличия турнира с таким же названием
            check_query = "SELECT * FROM tournament WHERE tournament_name = %s"
            cursor.execute(check_query, (tournament_name,))
            existing_tournament = cursor.fetchone()

            if existing_tournament:
                QMessageBox.warning(self, "Турнир уже существует", "Турнир с таким названием уже существует.")
            else:
                # Турнира с таким названием нет, выполняем вставку
                insert_query = "INSERT INTO tournament (tournament_name, date, prize) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (tournament_name, date, prize))
                connection.commit()

                QMessageBox.information(self, "Успешно", f"Турнир {tournament_name} создан и добавлен в базу данных.")
                self.accept()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при создании турнира: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        if self.parent():
            self.parent().update_tournament_list()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
           QWidget {
               background-color: #f0f0f0;
           }
           QLineEdit {
               padding: 5px;
               border: 1px solid #ccc;
               border-radius: 3px;
           }
           QPushButton {
               background-color: #4CAF50;
               color: white;
               border: 1px solid #4CAF50;
               padding: 5px 10px;
               border-radius: 3px;
           }
           QLabel {
               font-size: 14px;
           }
       """)
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
